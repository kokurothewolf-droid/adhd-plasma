# Technical Research: ADHD Plasma for KDE Plasma 6

## Plasma 6 Ecosystem Assessment

### Confirmed Available Components

**QML/Kirigami:**
- Kirigami 2 (org.kde.kirigami) — confirmed installed at `/usr/lib/qt6/qml/org/kde/kirigami/`
- Kirigami Controls: AboutItem, AboutPage, AbstractApplicationHeader, AbstractApplicationItem, AbstractApplicationWindow, AbstractCard, Action, ActionTextField, ActionToolBar, ApplicationItem, ApplicationWindow, Badge, Card, CardsLayout, CardsListView, Chip, ContextDrawer, ContextualHelpButton, FlexColumn, GlobalDrawer, Heading, InlineMessage, InlineViewHeader, LinkButton, ListItemDragHandle, ListSectionHeader, LoadingPlaceholder, NavigationTabBar, NavigationTabButton, OverlayDrawer, OverlaySheet, Page, PagePoolAction, PageRow, PasswordField, PlaceholderMessage, ScrollablePage, SearchField
- Kirigami Addons: Date/Time pickers, FloatingButton, FloatingToolBar, BottomDrawer, Banner, MessageDialog, RadioSelector, SearchPopupField, SegmentedButton
- QtQuick Controls 2 available through Kirigami

**KDE Frameworks 6:**
- Confirmed via `/usr/lib/qt6/qml/org/kde/` modules: activities, desktop, kaccounts, kcmutils, kdenlive, kholidays, ki18n, kirigami, kirigamiaddons, kitemmodels, kquickcontrols, kquickcontrolsaddons, ksvg, ksysguard, kwin, kwindowsystem, layershell, milou, networkmanager, notification, notificationmanager, pipewire, plasma, prison, private, purpose, qqc2desktopstyle, quickcharts, sonnet, taskmanager, userfeedback
- KF6 core addons: Archive, Bookmarks, Codecs, ConfigCore, ConfigGui, ConfigQml, CoreAddons, WidgetsAddons

**KWin 6:**
- KWin platform plugins confirmed: `plasma_session_shortcuts.so`, `plasma_accentcolor_service.so`
- KWin APIs accessible through Python/QML bindings

**Plasmoids/Plasmoidal architecture:**
- Plasma 6 version: 6.7.4 confirmed
- Package structure: `/usr/lib/qt6/plugins/kf6/packagestructure/plasma_applet.so`
- Containment actions available

### Akonadi Status

- `akonadictl` not found in PATH
- No `libKF5Akonadi` or `libKF6Akonadi` shared libraries found
- Akonadi likely not running or installed in minimal Plasma 6 setup
- Need to verify Akonadi availability through Plasma session

### Calendar/Task Components

- **korganizer**: Not found via `find`; KOrganizer traditional UI status unclear
- **kalendar**: Not found via `find`; Kalendar calendar component status unclear
- **KDE PIM**: Frameworks available but PIM-specific components need verification
- **Akonadi Browser/Resource**: Not confirmed present

### CalDAV/VTODO Ecosystem

- Python `caldav` 3.3.1 installed successfully
- Python `icalendar` 7.3.0 installed successfully
- No native KDE CalDAV bindings confirmed, but CalDAV over HTTP is a standard protocol
- Nextcloud Tasks CalDAV servers should work via standard CalDAV protocol

### Global Shortcuts & KWin

- `plasma_session_shortcuts.so` confirmed — KWin session shortcuts infrastructure exists
- Super+Q shortcut configuration should be achievable through KWin or KDE settings

### Packaging Reference

Plasma 6 plasmoid packaging follows:
- `.plasmoid` or `.kdeplugin` manifest files
- `metadata.desktop` with `X-KDE-PlasmaApiVersion` and `X-KDE-PluginInfo-Name`
- QML source files and resources
- Installation to `~/.local/share/plasma/plasmoids/` or system paths

## API Verification Status

| Component | Status | Notes |
|-----------|--------|-------|
| Kirigami 2 QML controls | ✅ Available | Full set confirmed |
| Plasma 6 shell | ✅ Available | 6.7.4 running |
| KWin shortcuts API | ✅ Available | via session_shortcuts plugin |
| Akonadi | ❓ Unknown | Need running session verification |
| KOrganizer | ❓ Unknown | Not located in standard paths |
| Kalendar | ❓ Unknown | Not located in standard paths |
| CalDAV client (Python) | ✅ Available | caldav 3.3.1, icalendar 7.3.0 |
| Natural-language date parsing | ❓ Needs research | Python dateutil available |

## Determined Next Steps

1. **Verify Akonadi availability** by checking Plasma session state
2. **Test CalDAV synchronization** against a local/test Nextcloud instance
3. **Map KDE PIM data models** to the ADHD Plasma data model
4. **Prototype TODAY/NOW plasmoids** using Kirigami QML with local/fake data
5. **Implement capture shortcut** (Super+Q) via KWin/shortcuts infrastructure
6. **Research natural-language date parsing** options (dateutil, parsedatetime, or custom)

## Recommendations

- **Use Kirigami 2** for all QML UIs — confirmed available and themable
- **Leverage KDE notifications** through standard KDE notification infrastructure
- **Use CalDAV via Python** for Nextcloud Tasks synchronization — no need for custom sync engine
- **Plan Akonadi integration** as optional layer if found available in user's Plasma session
- **Follow KDE human interface guidelines** — dark translucent surfaces, strong hierarchy, large click targets
- **Build as Plasmoid(s)** that install on existing Plasma 6 — not a new DE