#!/usr/bin/env python3
"""
Hyprland TODAY widget

Reads from SQLite task cache and displays:
- NOW: current and immediate next action
- NEXT: upcoming event/task
- LATER: deferred items
- Time remaining/transition points
"""

import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/.hermes/cache/scratch/adhd_tasks.db")

def get_recent_tasks(days=1):
    """Get tasks from the last N days, sorted by due date."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get tasks that are not completed, ordered by due date
    c.execute("""
        SELECT id, title, due_at, status, priority, estimated_duration
        FROM tasks
        WHERE status != 'completed'
        ORDER BY COALESCE(due_at, '9999-99-99T23:59:59') ASC
        LIMIT 20
    """)
    
    tasks = []
    
    for row in c.fetchall():
        task_id, title, due_at, status, priority, est_dur = row
        tasks.append({
            'id': task_id,
            'title': title or 'Untitled',
            'due_at': due_at,
            'status': status or 'pending',
            'priority': priority or 0,
            'estimated_duration': est_dur or 0,
        })
    
    conn.close()
    return tasks

def get_now_info():
    """Get the current 'NOW' task - the one being worked on or most immediate."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Try to find a task with no due date (active work) or earliest due
    c.execute("""
        SELECT id, title, due_at, status, priority, estimated_duration
        FROM tasks
        WHERE status != 'completed'
        ORDER BY 
            CASE WHEN due_at IS NULL THEN 1 ELSE 0 END,
            COALESCE(due_at, '9999-99-99T23:59:59') ASC
        LIMIT 1
    """)
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'title': row[1] or 'Untitled',
            'due_at': row[2],
            'status': row[3] or 'pending',
            'priority': row[4] or 0,
            'estimated_duration': row[5] or 0,
        }
    return None

def format_time_remaining(due_str):
    """Format time remaining until a due time."""
    if not due_str:
        return "No deadline"
    
    try:
        from datetime import datetime, timezone, timedelta
        due = datetime.fromisoformat(due_str)
        now = datetime.now(timezone.utc)
        delta = due - now
        
        if delta.days > 0:
            return f"due in {delta.days} days"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"due in {hours}h {minutes}m"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"due in {minutes}m"
        else:
            return "due now"
    except Exception:
        return "date error"

def today_widget():
    """Generate the TODAY widget display."""
    tasks = get_recent_tasks(days=1)
    now_task = get_now_info()
    
    lines = []
    lines.append("╭──── TODAY ─────╮")
    
    # NOW section
    if now_task:
        due_info = format_time_remaining(now_task['due_at'])
        priority_str = f" [P{now_task['priority']}]" if now_task['priority'] else ""
        lines.append(f"│ NOW            │")
        lines.append(f"│ {now_task['title'][:50]:50}{priority_str} │")
        lines.append(f"│ {due_info:22} │")
    else:
        lines.append(f"│ NOW            │")
        lines.append(f"│ No active task │")
    
    lines.append(f"├────────────────┤")
    
    # NEXT section - upcoming tasks
    lines.append(f"│ NEXT           │")
    upcoming = [t for t in tasks if t['due_at'] and 
                datetime.fromisoformat(t['due_at']) > datetime.now(timezone.utc)]
    if upcoming:
        for t in upcoming[:3]:  # Show top 3
            due = format_time_remaining(t['due_at'])
            p = f" [P{t['priority']}]" if t['priority'] else ""
            lines.append(f"│ {t['title'][:48]:48}{p} │")
            lines.append(f"│   due: {due:20} │")
    else:
        lines.append(f"│ No upcoming tasks │")
    
    lines.append(f"╰────────────────╯")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(today_widget())
