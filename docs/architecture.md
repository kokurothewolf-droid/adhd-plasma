# Architecture: ADHD Plasma for KDE Plasma 6

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Plasma 6 Desktop                            │
│  (KWin, shell, widgets, notifications, shortcuts)              │
├─────────────────────────────────────────────────────────────────┤
│                    ADHD Plasmoids                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ TODAY   │  │   NOW   │  │ATTENTION│  │  CAPTURE│             │
│  │ Panel   │  │ Card    │  │ Queue   │  │ Field   │             │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                    KDE PIM Layer                                 │
│  ┌─────────┐  ┌─────────┐  ┌────────────────────┐                │
│  │ Akonadi │  │ KOrganizer│  │ Kalendar/Merkuro   │ │
│  └─────────┘  └─────────┘  └────────────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│                    Synchronization                               │
│  ┌──────────────────────────────────────────────────────┐        │
│  │ CalDAV/VTODO → Nextcloud Tasks ← mobile clients      │        │
│  └──────────────────────────────────────────────────────┘        │
├─────────────────────────────────────────────────────────────────┤
│                    Local Storage                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐                │
│  │ SQLite (tasks.db)   │  │ JSON preferences    │                │
│  └─────────────────────┘  └─────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### 1. TODAY Plasmoid (Left-side panel)
- **Purpose**: Time awareness panel showing NOW → NEXT → LATER
- **Data sources**: Merged calendar/tasks from Akonadi/CalDAV
- **Displays**:
  - NOW: Current action, time remaining
  - NEXT: Next event/meeting, transition info
  - LATER: Non-urgent items (laundry, dinner, medication)
- **Updates**: Event-driven through KDE calendars/alarms

### 2. NOW Plasmoid (Primary desktop card)
- **Purpose**: Show current and immediate next action
- **Data**: Single current task + immediate next
- **Actions**: [CONTINUE] [I'M STUCK]
- **Behavior**: Dynamic update based on time/state

### 3. ATTENTION Queue
- **Purpose**: Persistent reminders that survive reboot
- **States**: pending, acknowledged, snoozed, completed, rescheduled, blocked
- **Key contract**: Closing notification ≠ completion
- **Escalation**: Configurable intervals, snooze presets, quiet hours
- **Storage**: SQLite + reboot-persistent JSON

### 4. CAPTURE (Quick Capture)
- **Global shortcut**: Super+Q (configurable)
- **Input**: Minimal field for NL date parsing
- **Types**: task, reminder, event, note, distraction/idea
- **Output**: Inbox item that can be reviewed/processed
- **Implementation**: KWin global shortcut → QML dialog

### 5. DISTRACTION PARKING LOT
- **Purpose**: Save intrusive ideas without abandoning task
- **Inbox**: Reviewable later
- **Sync**: Same CalDAV channel as tasks

### 6. RECOVERY
- **Trigger**: Meaningful inactivity or context switch
- **Output**: "WELCOME BACK" card with last work + next action
- **Research**: KDE Activities, KWin session restoration, recent-document APIs
- **Contract**: Do not fake unsupported functionality

### 7. Time Awareness
- **Visual**: `1 PM ───●────────████── 3 PM` format
- **Transitions**: wrap up in 20 min, meeting in 5 min, join meeting
- **One-click join**: If event has meeting URL

### 8. Synchronization Layer
- **Primary**: CalDAV/VTODO → Nextcloud Tasks
- **Architecture**: KDE UI → KDE PIM/Akonadi → CalDAV → Nextcloud → mobile clients
- **Bidirectional**: desktop ↔ server ↔ mobile
- **Conflict handling**: "Server has newer version" KEEP LOCAL / USE SERVER
- **Do NOT**: Run competing sync engines if KDE already manages account

## Data Model

### Interoperable Task/Calendar Data (sync layer)
```
id, title, description, created_at, updated_at,
start_at, due_at, completed_at, status, priority,
project, tags, reminders, snooze_until,
estimated_duration, provider, remote_id, metadata
```

### ADHD Plasma-Specific Metadata
```
attention_state: {pending, acknowledged, snoozed, completed, rescheduled, blocked}
last_notified_at, quiet_until, escalation_count,
distraction_origin, capture_source
```

### Synchronization Strategy

**Single source of truth**: CalDAV server (Nextcloud Tasks)
- Desktop reads/writes through CalDAV
- Offline cache in SQLite
- Version vectors for conflict detection
- On reconnection, sync pending changes

**Akonadi role**: Optional — if Akonadi is available in the user's Plasma session, use it as a local cache/translation layer over CalDAV. If not, use direct CalDAV Python client.

**Never run competing sync engine**: If user has KDE accounts configured, use those rather than creating parallel infrastructure.

## Integration Points with KDE

### KWin Integration
- Global shortcuts (Super+Q capture)
- Notification management (ATQ states)
- Session management/restoration
- Activities awareness

### KDE Notifications
- Standard KDE notification framework
- Persistent reminders as high-priority notifications
- Snooze/reschedule from notification action menu
- "Closing ≠ completion" contract enforced by app, notifier relays state

### KRunner
- Plugin for quick capture: `super+q` → type task
- Activity-based filtering

### Activities
- Per-activity task lists / contexts
- Session restoration per-activity

### System Settings
- Centralized configuration module for:
  - Task/calendar sources
  - Default task list
  - Reminders/Attention Queue settings
  - Quiet hours
  - Escalation behavior
  - Quick Capture shortcut
  - Time awareness preferences
  - Appearance/accessibility

## Packaging

### Plasma 6 Plasmoid Package
```
adhd-plasma/
├── metadata.desktop          # Plugin manifest
├── contents/
│   └── qml/
│       └── Main.qml         # Main UI entry point
├── config/
│   └── defaults.conf        # Default settings
├── init/
│   └── init.js              # Plasmoid initialization
├── ../today/                # TODAY plasmoid
├── ../now/                  # NOW plasmoid
├── ../attention/            # ATTENTION Queue plasmoid
└── ../capture/              # CAPTURE plasmoid
```

### Installation
- `plasmapkg2 -i adhd-plasma/` or drag-and-drop to Plasma Add Widgets → Get New Widgets
- Or `cp -r` to `~/.local/share/plasma/plasmoids/`
- Dependencies: KDE Frameworks 6, Qt 6, Kirigami 2

## Dependency Summary

| Category | Packages/Modules | Status |
|----------|-----------------|--------|
| QML UI | Kirigami 2, QtQuick Controls 2 | ✅ Available |
| KDE Integration | KWin, KDE Frameworks 6 | ✅ Confirmed |
| CalDAV Sync | Python caldav/icalendar | ✅ Installable |
| Local Storage | SQLite (built-in) | ✅ Available |
| Natural Language | Python dateutil | ✅ Available |
| Date Parsing | Custom / parsedatetime | ⬜ To research |
| Notifications | KDE Notification Framework | ✅ Available |
| Global Shortcuts | KWin shortcuts | ✅ Available |

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Akonadi not available | Fall back to direct CalDAV; make Akonadi optional |
| CalDAV server limitations | Implement standard CalDAV; test against Nextcloud, other CalDAV servers |
| Notification fatigue | Configurable escalation, quiet hours, snooze presets; "closing ≠ completion" contract |
| Sync conflicts | Version vectors; explicit "KEEP LOCAL / USE SERVER" prompt |
| Custom sync engine overhead | Use CalDAV only; no competing engine; leverage KDE account infrastructure |
| Date parsing edge cases | Start with deterministic open-source parser; AI optional later |
| KWin global shortcut conflicts | Configurable shortcut; default Super+Q with override option |