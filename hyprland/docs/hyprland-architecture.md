# ADHD Plasma for Hyprland

A Hyprland-oriented executive-function layer focused on:
- working/prospective memory
- task initiation  
- time awareness
- interruption management
- persistent reminders
- distraction recovery
- frictionless capture
- context restoration

## Architecture

```
┌─────────────────────────────────────────────┐
│  Google Calendar/Tasks API                │
│  (OAuth 2.0, rdunkle88@gmail.com)        │
│  Events/Tasks → SQLite Cache (readonly)   │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Hyprland Layer                           │
│  ├─ ~/.config/hypr/hyprland.conf          │
│  ├─ Bar widgets (hyprbar or custom)      │
│  │  ├─ TODAY: time awareness              │
│  │  ├─ NOW: current action                │
│  │  ├─ ATTENTION: persistent reminders    │
│  │  └─ CAPTURE: quick capture (Super+Q)  │
│  ├─ Keybindings for session switching     │
│  └─ Lock screen: Hyprlock (configurable) │
└─────────────────────────────────────────────┘
```

## Reused from KDE Plasma Build ✅

| Component | Source | Status |
|-----------|--------|--------|
| Google Calendar API | `caldav_backend.py` + OAuth flow | ✅ Working |
| Google Tasks API | Same OAuth flow, `tasks` scope | ✅ Working |
| SQLite Task Cache | `backend/caldav_backend.py` | ✅ Working |
| Version Vectors | Conflict resolution logic | ✅ Reusable |
| Attention State Machine | 6 states (pending→acknowledged→...) | ✅ Reusable |
| Data Model | id, title, description, created_at, updated_at, start_at, due_at, completed_at, status, priority, project, tags, reminders, snooze_until, estimated_duration, provider, remote_id, metadata | ✅ Reusable |
| Offline-First | Local SQLite, sync on reconnection | ✅ Reusable |
| Core Concepts | TODAY/NOW/ATTENTION/CAPTURE | ✅ Reusable framework |

## What Needs to Be Created ⚠️

| Item | Description | Effort |
|------|-------------|--------|
| `hyprland.conf` | Hyprland config with keybindings, bar setup | Low |
| `bar_scripts/` | Scripts that read SQLite cache, output Pango/PipeWire bar format | Medium |
| `widget_today.py` | TODAY display: NOW→NEXT→LATER, time remaining | Medium |
| `widget_now.py` | NOW display: current action, [CONTINUE] [I'M STUCK] | Medium |
| `widget_attention.py` | ATTENTION: persistent reminders with state machine | Medium |
| `widget_capture.py` | CAPTURE: Super+Q trigger, NL date parsing | Medium |
| `keybindings.ini` | Session switching, capture, attention actions | Low |
| `hyprlock.conf` | Configurable lock screen (not password-only loop) | Low |

## Google API Integration (Already Working)

The Google Calendar/Tasks backend is fully functional:

- **OAuth 2.0**: Completed for `rdunkle88@gmail.com`
- **Calendar API**: Events fetched successfully
- **Tasks API**: Task lists and tasks fetched
- **Token location**: `~/.config/google-oauth2/token.json`
- **Client location**: `~/.config/google-oauth2/client_secret.json`

Integration point: Same as KDE version — read from SQLite cache, no need to reimplement OAuth.

## Data Model (Reused)

```text
id | title | description | created_at | updated_at | start_at | due_at | completed_at | status | priority | project | tags | reminders | snooze_until | estimated_duration | provider | remote_id | metadata | attention_state
```

Plus ADHD-specific metadata tables (attention_state, snooze_until, version vectors for conflict resolution).

## Session Management (Hyprland vs SDDM)

| KDE Plasma (Current) | Hyprland (New) |
|---------------------|----------------|
| SDDM greeter → lock screen → password only | Boot to Hyprland directly |
| `omarchy system logout` → lock screen loop | Hyprland workspace switching |
| Lock screen: password-only (broken) | Hyprlock: configurable, full options |
| Session management through display manager | Session management through WM/bar |

The key fix: No display manager = no SDDM lock screen loop.
