#!/usr/bin/env python3
"""Hyprland ATTENTION widget - displays persistent reminders with state machine."""

import sqlite3
import os

DB_PATH = os.path.expanduser("~/.hermes/cache/scratch/adhd_tasks.db")


def get_persistent_reminders():
    """Get reminders that need attention (not completed)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT id, title, due_at, status, snooze_until, estimated_duration, attention_state
        FROM tasks
        WHERE status != 'completed'
        AND (snooze_until IS NOT NULL OR attention_state != 'pending')
        ORDER BY COALESCE(due_at, '9999-99-99T23:59:59') ASC
        LIMIT 10
    """)

    reminders = []
    for row in c.fetchall():
        task_id, title, due_at, status, snooze_until, est_dur, attention_state = row
        reminders.append({
            'id': task_id,
            'title': title or 'Untitled',
            'due_at': due_at,
            'status': status or 'pending',
            'snooze_until': snooze_until,
            'estimated_duration': est_dur or 0,
            'attention_state': attention_state or 'pending',
        })

    conn.close()
    return reminders


def get_state_label(state):
    """Convert attention state to a human-readable label."""
    labels = {
        'pending': 'Active',
        'acknowledged': 'Noted',
        'snoozed': 'Snoozed',
        'completed': 'Done',
        'rescheduled': 'Rescheduled',
        'blocked': 'Blocked',
    }
    return labels.get(state, state)


def format_time(due_str):
    """Format due time as a simple string."""
    if not due_str:
        return "no deadline"
    try:
        from datetime import datetime, timezone, timedelta
        due = datetime.fromisoformat(due_str)
        now = datetime.now(timezone.utc)
        delta = due - now
        if delta.days > 0:
            return f"due in {delta.days}d"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"due in {hours}h"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"due in {minutes}m"
        else:
            return "due now"
    except Exception:
        return "date error"


def attention_widget():
    """Generate the ATTENTION widget display."""
    reminders = get_persistent_reminders()

    lines = []
    lines.append("╭──── ATTENTION ─────╮")

    if reminders:
        for r in reminders[:3]:  # Show top 3
            state_label = get_state_label(r['attention_state'])
            due = format_time(r['due_at']) if r['due_at'] else "no deadline"
            duration = f"{r['estimated_duration']} min" if r['estimated_duration'] else ""
            snooze = f"snoozed until: {r['snooze_until']}" if r['snooze_until'] else ""

            # Build each line manually
            title_line = r['title'][:48] if r['title'] else "Untitled"

            line_parts = [f"│ {title_line} │"]
            lines.append(line_parts[0])

            state_line = f"│ state: {state_label} │"
            lines.append(state_line)

            due_line = f"│ due: {due:22} │"
            lines.append(due_line)

            if duration:
                dur_line = f"│ duration: {duration:24} │"
                lines.append(dur_line)

            if snooze:
                snooze_line = f"│ snoozed until: {snooze:28} │"
                lines.append(snooze_line)

            action_line = "│ [DONE] [REMIND AGAIN] │"
            lines.append(action_line)

            # Separator
            lines.append("├─────────────────────┤")
    else:
        lines.append("│ No persistent reminders │")
        lines.append("│ All clear!          │")

    lines.append("╰─────────────────────╯")
    return "\n".join(lines)


if __name__ == "__main__":
    print(attention_widget())