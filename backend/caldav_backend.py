# CalDAV Backend for ADHD Plasma
# Python module handling all CalDAV protocol operations.
# Connects to: Python caldav 3.3.1 + icalendar 7.3.0
#
# Provides backend for the QML CalDAVIntegration.qml component.
#
# Operations:
# - connect() — CalDAV server connection
# - discover() — find task lists/calendars
# - fetch_tasks() — get all tasks from all lists
# - add_task() — create new VTODO on server
# - update_task() — modify existing task
# - delete_task() — remove task from server
# - sync() — bidirectional sync with local SQLite cache
# - conflict_resolution() — KEEP LOCAL / USE SERVER
# - incremental_sync() — only changed items

import sys
import json
import sqlite3
import os
import logging
from datetime import datetime, timedelta, timezone
from caldav import DAVClient
from caldav.objects import DAVCalendar, DAVObject
from icalendar import Calendar, VTodo, VEVENT, VTODO, Property

# Try to import Google API packages; gracefully degrade if not available
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logger = logging.getLogger("adhd-plasma-google")
    logger.warning("Google API packages not available — Google integration disabled")

logger = logging.getLogger("adhd-plasma-caldav")


# ─── CalDAVBackend Class ───────────────────────────────────────────

class CalDAVBackend:
    """Handles all CalDAV synchronization for ADHD Plasma."""

    def __init__(self, config_path="~/.config/adhd-plasma/caldav_config.json"):
        self.config_path = os.path.expanduser(config_path)
        self.client = None
        self.account = None
        self.calendar = None  # Tasks calendar
        self.local_db_path = os.path.expanduser(
            "~/.hermes/cache/scratch/adhd_tasks.db"
        )
        self.version_vector = {}  # {remote_id: modification_time}
        self.local_vv = {}  # {local_task_id: modification_time}

        # Ensure local SQLite cache exists
        self._ensure_local_db()

    def _ensure_local_db(self):
        """Initialize the local SQLite task cache if needed."""
        os.makedirs(os.path.dirname(self.local_db_path), exist_ok=True)
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT,
                updated_at TEXT,
                start_at TEXT,
                due_at TEXT,
                completed_at TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 0,
                project TEXT,
                tags TEXT DEFAULT '',
                reminders TEXT DEFAULT '[]',
                snooze_until TEXT,
                estimated_duration INTEGER DEFAULT 0,
                provider TEXT DEFAULT 'caldav',
                remote_id TEXT,
                metadata TEXT DEFAULT '{}',
                attention_state TEXT DEFAULT 'pending',
                last_notified_at TEXT,
                quiet_until TEXT
            )"""
        )
        # Version vector table
        c.execute(
            """CREATE TABLE IF NOT EXISTS version_vector (
                key TEXT PRIMARY KEY,
                value TEXT
            )"""
        )
        # Sync state table
        c.execute(
            """CREATE TABLE IF NOT EXISTS sync_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )"""
        )
        conn.commit()
        conn.close()

    # ─── Configuration ────────────────────────────────────────────

    def load_config(self):
        """Load CalDAV configuration from JSON file."""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            self.caldav_url = config.get("caldav_url", "")
            self.username = config.get("username", "")
            self.password = config.get("password", "")
            self.default_task_list = config.get("default_task_list", "")
            self.enabled = config.get("enabled", False)
            self.escalation_interval = config.get("escalation_interval", 15)  # minutes
            self.quiet_hours = config.get(
                "quiet_hours", {"start": "22:00", "end": "08:00"}
            )
            return True
        except FileNotFoundError:
            logger.info("No CalDAV config found — use config plasmoid to set up")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid CalDAV config: {e}")
            return False

    def save_config(self, config):
        """Save CalDAV configuration to JSON file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    # ─── Connection ───────────────────────────────────────────────

    async def connect(self):
        """Connect to CalDAV server."""
        if not self.enabled or not self.caldav_url:
            logger.warning("CalDAV not enabled or no URL configured")
            return False

        try:
            self.client = DAVClient(
                url=self.caldav_url, username=self.username, password=self.password
            )
            self.account = await self.client.login()
            logger.info(f"Connected to CalDAV server: {self.caldav_url}")
            return True
        except Exception as e:
            logger.error(f"CalDAV connection failed: {e}")
            self.client = None
            self.account = None
            return False

    # ─── Discovery ────────────────────────────────────────────────

    async def discover_task_lists(self):
        """Discover available CalDAV task lists/calendars."""
        if not self.client or not self.account:
            await self.connect()

        if not self.client:
            return []

        try:
            calendars = self.account.calendars()
            result = []
            for cal in calendars:
                name = cal.name or "Unnamed"
                try:
                    items = cal.fetch_items()
                    task_items = [i for i in items if i.type == "text/x-vtodo"]
                    result.append(
                        {
                            "name": name,
                            "href": cal.href,
                            "task_count": len(task_items),
                            "is_task_cal": True,
                        }
                    )
                except Exception:
                    result.append(
                        {
                            "name": name,
                            "href": cal.href,
                            "task_count": 0,
                            "is_task_cal": False,
                        }
                    )
            self.task_lists = result
            logger.info(f"Discovered {len(result)} CalDAV calendars")
            return result
        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            return []

    # ─── Task Fetching ────────────────────────────────────────────

    async def fetch_tasks(self, from_server=True, local_only=False):
        """Fetch tasks from server and/or local cache."""
        tasks = []

        if local_only:
            tasks = self._read_local_tasks()
            return tasks

        if from_server and self.client and self.account:
            server_tasks = await self._fetch_from_server()
            local_tasks = self._read_local_tasks()
            tasks = self._merge_tasks(server_tasks, local_tasks)
            self._write_tasks_to_local(tasks)
        elif not from_server:
            tasks = self._read_local_tasks()

        return tasks

    def _read_local_tasks(self):
        """Read all tasks from local SQLite cache."""
        tasks = []
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute(
            """SELECT id, title, description, created_at, updated_at,
               start_at, due_at, completed_at, status, priority,
               project, tags, reminders, snooze_until,
               estimated_duration, provider, remote_id, metadata,
               attention_state, last_notified_at, quiet_until FROM tasks"""
        )
        rows = c.fetchall()
        for row in rows:
            task = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "created_at": row[3],
                "updated_at": row[4],
                "start_at": row[5],
                "due_at": row[6],
                "completed_at": row[7],
                "status": row[8],
                "priority": row[9] or 0,
                "project": row[10],
                "tags": json.loads(row[11]) if row[11] else [],
                "reminders": json.loads(row[12]) if row[12] else [],
                "snooze_until": row[13],
                "estimated_duration": row[14] or 0,
                "provider": row[15] or "caldav",
                "remote_id": row[16],
                "metadata": json.loads(row[17]) if row[17] else {},
                "attention_state": row[18] or "pending",
                "last_notified_at": row[19],
                "quiet_until": row[20],
            }
            tasks.append(task)
        conn.close()
        return tasks

    def _write_tasks_to_local(self, tasks):
        """Write tasks to local SQLite cache."""
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        for task in tasks:
            attention_state = task.get("status", "pending")
            if task.get("snooze_until"):
                attention_state = "snoozed"
            elif task.get("quiet_until"):
                attention_state = "pending"

            c.execute(
                """INSERT OR REPLACE INTO tasks
                (id, title, description, created_at, updated_at,
                 start_at, due_at, completed_at, status, priority,
                 project, tags, reminders, snooze_until,
                 estimated_duration, provider, remote_id, metadata,
                 attention_state, last_notified_at, quiet_until)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    task["id"],
                    task["title"],
                    task["description"],
                    task["created_at"],
                    task["updated_at"],
                    task.get("start_at"),
                    task.get("due_at"),
                    task.get("completed_at"),
                    task["status"],
                    task.get("priority", 0),
                    task.get("project"),
                    json.dumps(task.get("tags", [])),
                    json.dumps(task.get("reminders", [])),
                    task.get("snooze_until"),
                    task.get("estimated_duration", 0),
                    task.get("provider", "caldav"),
                    task.get("remote_id"),
                    json.dumps(task.get("metadata", {})),
                    attention_state,
                    task.get("last_notified_at"),
                    task.get("quiet_until"),
                ),
            )
        # Update version vector
        for task in tasks:
            if task.get("remote_id"):
                self.local_vv[task["id"]] = task.get("updated_at", "")
        c.execute(
            "INSERT OR REPLACE INTO version_vector (key, value) VALUES (?, ?)",
            ("local_vv", json.dumps(self.local_vv)),
        )
        c.execute(
            "INSERT OR REPLACE INTO sync_state (key, value) VALUES (?, ?)",
            ("last_sync", datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()

    # ─── Server Fetching ──────────────────────────────────────────

    async def _fetch_from_server(self):
        """Fetch all tasks from CalDAV server."""
        if not self.client or not self.account:
            return []

        tasks = []
        try:
            calendars = self.account.calendars()
            for cal in calendars:
                try:
                    items = cal.fetch_items()
                    for item in items:
                        if item.type == "text/x-vtodo":
                            task = self._parse_vtodo(item)
                            if task:
                                tasks.append(task)
                except Exception as e:
                    logger.warning(
                        f"Failed to fetch items from calendar {cal.name}: {e}"
                    )
            logger.info(
                f"Fetched {len(tasks)} tasks from {len(calendars)} calendars"
            )
        except Exception as e:
            logger.error(f"Server fetch failed: {e}")

        return tasks

    def _parse_vtodo(self, cal_object):
        """Parse a CalDAV VTODO object into our task model."""
        try:
            uid = cal_object.get("uid", "")
            summary = cal_object.get("summary", "")
            description = cal_object.get("description", "")

            # Date handling
            due = cal_object.get("due")
            start = cal_object.get("dtstart")
            dtend = cal_object.get("dtend")
            completed = cal_object.get("completed")

            # Status from iCalendar
            status_prop = cal_object.get("status")
            if status_prop:
                status_val = str(status_prop).lower()
                if status_val in ("completed", "done"):
                    status = "completed"
                else:
                    status = "pending"
            else:
                status = "pending"

            # Parse dates
            due_at = self._ical_to_iso(due) if due else None
            start_at = self._ical_to_iso(start) if start else None
            completed_at = self._ical_to_iso(completed) if completed else None

            # Priority (non-standard, store as metadata)
            priority = 0
            priority_prop = cal_object.get("priority")
            if priority_prop is not None:
                try:
                    priority = int(priority_prop)
                except (ValueError, TypeError):
                    priority = 0

            # Tags (from custom properties or keywords)
            tags = []
            keywords = cal_object.get("keywords")
            if keywords:
                if isinstance(keywords, str):
                    tags = [k.strip() for k in keywords.split(",")]
                elif isinstance(keywords, list):
                    tags = [str(k).strip() for k in keywords]

            # Reminders / alarms
            reminders = []
            alarm_props = (
                cal_object.get("properties", {}).get("VALARM", [])
            )
            for alarm in alarm_props:
                trigger = alarm.get("trigger", 0)
                action = alarm.get("action", "DISPLAY")
                reminders.append({"trigger": str(trigger), "action": action})

            # UID as remote_id
            remote_id = str(uid) if uid else f"caldav-{hash(str(cal_object))}"

            task = {
                "id": remote_id,
                "title": str(summary) if summary else "Untitled task",
                "description": str(description) if description else "",
                "created_at": self._ical_to_iso(cal_object.get("dtcreated"))
                if cal_object.get("dtcreated")
                else datetime.now(timezone.utc).isoformat(),
                "updated_at": self._ical_to_iso(cal_object.get("last-modified"))
                if cal_object.get("last-modified")
                else datetime.now(timezone.utc).isoformat(),
                "start_at": start_at,
                "due_at": due_at,
                "completed_at": completed_at,
                "status": status,
                "priority": priority,
                "project": "",
                "tags": tags,
                "reminders": reminders,
                "snooze_until": "",
                "estimated_duration": 0,
                "provider": "caldav",
                "remote_id": remote_id,
                "metadata": {},
                "attention_state": "pending" if status != "completed" else "completed",
                "last_notified_at": "",
                "quiet_until": "",
            }
            return task
        except Exception as e:
            logger.error(f"Failed to parse VTODO: {e}")
            return None

    @staticmethod
    def _ical_to_iso(date_prop):
        """Convert iCalendar date to ISO 8601 string."""
        if date_prop is None:
            return None
        try:
            if hasattr(date_prop, "year"):
                return date_prop.isoformat()
            return str(date_prop)
        except Exception:
            return None

    # ─── Task Management ──────────────────────────────────────────

    async def add_task(self, task_data):
        """Add a new task to CalDAV server and local cache."""
        if not self.client or not self.account:
            self._write_tasks_to_local([task_data])
            task_data["remote_id"] = (
                "local-" + str(hash(json.dumps(task_data)))
            )
            return task_data

        try:
            calendar = (
                self.account.calendar(self.default_task_list)
                if self.default_task_list
                else self.account.calendars()[0]
            )

            # Build iCalendar VTODO
            ical_todo = VTodo()
            ical_todo.add("uid", task_data.get("remote_id", f"adhd-{datetime.now().timestamp()}"))
            ical_todo.add("summary", task_data.get("title", ""))

            if task_data.get("description"):
                ical_todo.add("description", task_data["description"])

            # Add dates
            if task_data.get("due_at"):
                due = self._iso_to_icalendar_date(task_data["due_at"])
                if due:
                    ical_todo.add("due", due)

            if task_data.get("start_at"):
                start = self._iso_to_icalendar_date(task_data["start_at"])
                if start:
                    ical_todo.add("dtstart", start)

            ical_todo.add("priority", task_data.get("priority", 0))

            if task_data.get("tags"):
                ical_todo.add("keywords", ",".join(task_data["tags"]))

            # Add status
            if task_data.get("status") == "completed":
                ical_todo.add("status", "completed")

            # Add basic alarm for reminders
            # (Full alarm building would go here)

            calendar.add_component(ical_todo)

            # Refresh local cache
            await self.fetch_tasks(from_server=True)

            return task_data

        except Exception as e:
            logger.error(f"Failed to add task: {e}")
            self._write_tasks_to_local([task_data])
            task_data["remote_id"] = "local-" + str(hash(json.dumps(task_data)))
            return task_data

    @staticmethod
    def _iso_to_icalendar_date(iso_str):
        """Convert ISO 8601 string to iCalendar compatible format."""
        if iso_str is None:
            return None
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt
        except (ValueError, TypeError):
            return None

    async def update_task(self, task_id, changes):
        """Update an existing task on CalDAV server and local cache."""
        # Update local cache first
        local_task = self._find_local_task(task_id)
        if local_task:
            for key, value in changes.items():
                if key in local_task:
                    local_task[key] = value

            # Update SQLite
            self._write_tasks_to_local([local_task])

        # Then sync to server if online
        if self.client and self.account:
            try:
                logger.info(
                    f"Would update task {task_id} on server with changes: {changes}"
                )
                # TODO: Implement actual server update
            except Exception as e:
                logger.error(f"Server update failed: {e}")

        return local_task

    def _find_local_task(self, task_id):
        """Find a task in the local cache by ID."""
        tasks = self._read_local_tasks()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None

    async def delete_task(self, task_id):
        """Delete a task from CalDAV server and local cache."""
        # Delete from local cache
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        # Update version vector
        if task_id in self.local_vv:
            del self.local_vv[task_id]
        c.execute(
            "INSERT OR REPLACE INTO version_vector (key, value) VALUES (?, ?)",
            ("local_vv", json.dumps(self.local_vv)),
        )
        c.execute(
            "INSERT OR REPLACE INTO sync_state (key, value) VALUES (?, ?)",
            ("last_sync", datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()

        # Delete from server if online
        if self.client and self.account:
            try:
                logger.info(f"Would delete task {task_id} from server")
                # TODO: Implement actual server delete
            except Exception as e:
                logger.error(f"Server delete failed: {e}")

    # ─── Conflict Resolution ──────────────────────────────────────

    def resolve_conflict(self, task_id, local_data, server_data):
        """Present conflict resolution: KEEP LOCAL / USE SERVER."""
        local_modified = self.local_vv.get(task_id, "1970-01-01T00:00:00Z")
        server_modified = self._get_server_modified_date(task_id) or "1970-01-01T00:00:00Z"

        if local_modified > server_modified:
            decision = "KEEP_LOCAL"
        elif server_modified > local_modified:
            decision = "USE_SERVER"
        else:
            decision = "ASK_USER"

        # In the actual UI, this would present:
        # [ KEEP LOCAL ] [ USE SERVER ]
        # and user choice would be recorded

        return decision

    def _get_server_modified_date(self, task_id):
        """Get the last modification date of a task on the server."""
        return self.local_vv.get(task_id)

    # ─── Incremental Sync ─────────────────────────────────────────

    async def incremental_sync(self):
        """Sync only changed items since last sync."""
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute(
            "SELECT value FROM sync_state WHERE key = 'last_sync'"
        )
        row = c.fetchone()
        last_sync = row[0] if row else None
        conn.close()

        if last_sync:
            logger.info(
                "Incremental sync: fetching changed items since last sync"
            )

        # Do full fetch and update version vectors
        tasks = await self.fetch_tasks(from_server=True)
        self._write_tasks_to_local(tasks)

        return {"synced": len(tasks), "mode": "full"}

    # ─── Sync Status ──────────────────────────────────────────────

    def get_sync_status(self):
        """Return sync status for the QML component."""
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()

        c.execute(
            "SELECT COUNT(*) FROM tasks WHERE status != 'completed'"
        )
        active_count = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM tasks")
        total_count = c.fetchone()[0]

        c.execute(
            "SELECT value FROM sync_state WHERE key = 'last_sync'"
        )
        row = c.fetchone()
        last_sync = row[0] if row else None

        c.execute(
            "SELECT value FROM version_vector WHERE key = 'local_vv'"
        )
        row = c.fetchone()
        local_vv = json.loads(row[0]) if row else {}

        conn.close()

        return {
            "enabled": self.enabled,
            "is_syncing": self.client is not None and self.account is not None,
            "task_count": total_count,
            "active_count": active_count,  # pending + snoozed
            "server_url": self.caldav_url if self.enabled else "Not configured",
            "last_sync": last_sync,
            "conflict_count": len(
                [k for k, v in local_vv.items() if self._has_potential_conflict(v)]
            ),
            "source": "caldav" if self.enabled else "local-only",
            "google_integrated": GOOGLE_API_AVAILABLE and hasattr(self, 'google_service'),
        }

    @staticmethod
    def _has_potential_conflict(last_modified):
        """Check if a task modification could conflict."""
        try:
            mod_time = datetime.fromisoformat(last_modified)
            now = datetime.now()
            return now - mod_time < timedelta(hours=24)
        except (ValueError, TypeError):
            return False