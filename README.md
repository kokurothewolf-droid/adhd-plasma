# ADHD Plasma

A KDE Plasma 6 productivity and attention-management system designed to help people plan, focus, and recover from distraction without abandoning their current task.

ADHD Plasma combines a lightweight Python backend, CalDAV-compatible task synchronization, and a QML/Kirigami desktop experience to create a set of Plasma widgets and workflow tools for attention, time awareness, and quick capture.

## Why this project exists

The goal is not to replace the desktop, but to make the desktop more supportive:

- surface the most important task right now
- keep reminders persistent until acknowledged
- make quick capture fast and frictionless
- use calendar/task data from standard KDE and CalDAV sources
- reduce cognitive overhead when context shifts or attention drifts

## Core features

### Today / Now / Later awareness

A set of Plasma widgets can present task and time information in a way that helps users understand:

- what is happening now
- what is next
- what can wait

### Attention Queue

Persistent reminders and follow-up tasks that remain visible until they are acknowledged or resolved, rather than disappearing when a notification is closed.

### Quick Capture

A fast capture workflow for adding tasks, reminders, events, notes, or distractions without breaking flow.

### KDE integration

Built to work with the KDE Plasma ecosystem, including:

- Plasma 6 widgets
- QML/Kirigami UI components
- KDE notifications
- session shortcut support
- CalDAV-compatible task sources

## Architecture overview

This repo is organized around a few major layers:

- QML / Plasma UI components for desktop widgets and interaction
- Python backend logic for task/calendar access and processing
- CalDAV / VTODO synchronization with standard task sources
- local storage and configuration for preferences and reminders

High-level flow:

- KDE Plasma and KWin provide the desktop shell and system integration
- plasmoids provide the user-facing widgets and quick actions
- Python services handle synchronization and task logic
- CalDAV/Nextcloud-style task sources act as the shared source of truth

## Repository layout

```text
adhd-plasma/
├── backend/
│   └── caldav_backend.py
├── config/
│   └── adhd-plasma-config.ktl
├── docs/
│   ├── architecture.md
│   ├── architecture-review.md
│   ├── technical-research.md
│   └── ux-principles.md
├── hyprland/
├── integrations/
├── plasmoids/
├── service/
├── LICENSE
├── README.md
└── .gitignore
```

## Technology stack

- Python
- QML
- KDE Plasma 6
- Kirigami 2
- Qt Quick / Qt 6
- CalDAV / iCalendar-compatible task sync
- SQLite for local state

## Requirements

This project is designed for KDE Plasma 6 environments and is intended to run as a desktop integration rather than a generic web app.

Typical requirements include:

- KDE Plasma 6
- Qt 6 / KDE Frameworks 6
- QML/Kirigami support
- Python environment for backend logic
- CalDAV-compatible task source such as Nextcloud Tasks

## Installation

The project documentation describes installation as a Plasma plasmoid-style integration.

Typical approaches:

```bash
plasmapkg2 -i adhd-plasma/
```

or install manually by copying the package into your Plasma widgets directory:

```bash
cp -r adhd-plasma ~/.local/share/plasma/plasmoids/
```

## Configuration

Configuration is organized around a centralized config module and a task/calendar source model. Settings can cover:

- task and calendar sources
- default task list
- reminder and escalation behavior
- quiet hours
- quick capture shortcut
- time-awareness preferences
- appearance and accessibility options

Example config file:

- `config/adhd-plasma-config.ktl`

## Documentation

The project includes several design and architecture documents in the `docs/` folder:

- `docs/architecture.md` — architecture and component overview
- `docs/architecture-review.md` — review of the system structure
- `docs/technical-research.md` — environment and research notes
- `docs/ux-principles.md` — UX principles behind the design

These documents are useful if you want to understand the product intent or contribute to the project.

## Status

This project is actively being developed as a desktop productivity tool for KDE Plasma and is focused on a real-world workflow rather than a generic task manager.

The repo is best understood as a research-and-product prototype for attention-aware productivity tooling in the KDE desktop environment.

## Contributing

Contributions are welcome, especially in areas such as:

- Plasma widget UX
- task synchronization behavior
- calendaring integrations
- quick capture workflow
- accessibility and time-awareness features
- documentation improvements

If you want to help, start by reviewing the architecture docs and the app structure in `backend/`, `plasmoids/`, and `config/`.

## License

This project currently includes repository-level license metadata, and the actual license should be reviewed in the project root before redistribution or publishing.

## Project intent in one sentence

ADHD Plasma is a KDE Plasma productivity layer designed to reduce decision fatigue, improve task awareness, and make reminders and focus support feel native to the desktop.

---

If you want, I can also turn this into a more minimal GitHub-style README, a more polished product README, or a screenshot-ready landing page version with badges and installation sections.
