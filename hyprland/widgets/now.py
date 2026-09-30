#!/usr/bin/env python3
"""Hyprland NOW widget - displays current action with [CONTINUE] [I'M STUCK] options."""

import sqlite3
import os

DB_PATH = os.path.expanduser("~/.hermes/cache/scratch/adhd_tasks.db")


def get_current_task():
    """Get the current/active task - the one being worked on."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get task with no due date (active work) or earliest due and not completed
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


def format_duration(minutes):
    """Format estimated duration in minutes."""
    if not minutes:
        return ""
    if minutes < 60:
        return f"{minutes} min active"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m active"


def now_widget():
    """Generate the NOW widget display based on KDE Plasma mockup."""
    task = get_current_task()

    # Build lines manually to avoid f-string box-drawing issues
    title = task['title'][:50] if task['title'] else "Untitled"
    priority_str = f"[P{priority}]" if task['priority'] else ""
    duration = format_duration(task['estimated_duration'])

    lines = []
    lines.append("╭──── NOW ─────╮")
    lines.append(f"│ {title}{priority_str} │")
    lines.append(f"│ {duration:18} │")
    lines.append(f"│ [CONTINUE] [I'M STUCK] │")
    lines.append(f"╰────────────────╯")

    return "\n".join(lines)


if __name__ == "__main__":
    print(now_widget())