# UX Principles: ADHD Plasma for KDE Plasma 6

## Design Philosophy

### Calm, Non-Intrusive Interaction
The desktop should support executive function, not demand it. Interfaces minimize cognitive load and avoid asking "what now?" at every turn. Information is available when needed, not pushed constantly.

### Native KDE, Not Electron
- All QML/Kirigami — no Electron, no custom rendering pipeline
- KDE theme integration: surfaces respect `var(--foreground)`, `var(--muted-foreground)`, `var(--accent)`, `var(--border)`, `var(--card)`
- Dark translucent surfaces with subtle elevation (blur/opacity, not solid color)
- System fonts with good typography scale — respect KDE's font configuration

### Time Awareness as First-Class
Time is visualized concretely, never abstractly. The `1 PM ───●────────████── 3 PM` format is the model — users see what's remaining, what's transitioning, what's coming. "Focus until next event" is a first-class mode, not a hidden preference.

### Persistence Without Nagging
- Attention Queue state survives reboot
- Notifications are persistent but configurable
- "Closing a notification must NOT imply completion" is a hard contract
- Escalation intervals and quiet hours are configurable, not defaults-on

### Capture Frictionless, Review Later
- Super+Q (configurable) opens minimal field
- Natural-language date parsing: `remind me in 20 minutes to switch laundry`
- Distractions go to Parking Lot inbox, reviewable later
- Nothing is lost — everything lands in a reviewable location

### ADHD-Specific Considerations

#### Task Initiation Support
- "I'm stuck" menu produces next actionable step, not giant task tree
- Break large tasks into visible next actions
- Never generate overwhelming backlog displays

#### Transition Warnings
- Wrap-up periods configured by user
- Visual transition points in TODAY panel
- "Meeting in 5 minutes" → one-click join if URL present

#### Distraction Recovery
- "WELCOME BACK" after meaningful inactivity
- Last work + next action clearly presented
- RESUME action, not just information

### Interaction Patterns

#### Keyboard Navigation
- Full keyboard navigation through all plasmoids
- Strong focus states (contrasting, not just outline)
- Tab order logical and consistent
- Escape dismisses modals/returns to previous context

#### HiDPI Support
- All QML scales appropriately
- Touch-friendly hit targets (minimum 48dp)
- Text remains crisp at all scales
- No pixelated bitmaps

#### Reduced Motion
- Subtle only — respect `reduce-motion` system setting
- Animations are easing, not instant-disappear
- No motion for motion's sake

#### Accessible Contrast
- Minimum 4.5:1 contrast ratio
- KDE theme respects provide accessible color schemes
- Information not conveyed by color alone

## Information Hierarchy

### TODAY Panel (left side)
1. NOW — current action, time remaining (most important)
2. NEXT — next event, transition info
3. LATER — non-urgent items (laundry, dinner, medication)

### NOW Card (center/primary)
1. Current action title + context
2. "18 min active" or similar time indicator
3. [CONTINUE] [I'M STUCK] — always visible

### ATTENTION Queue
1. Persistent reminders with state indicators
2. [DONE] [REMIND AGAIN] per item
3. State: pending > acknowledged > snoozed > completed > rescheduled > blocked

### Capture Field
1. Single input line
2. Prompt text or empty for free-form
3. Quick presets or free-text

## Visual Design Language

### Surfaces
- Dark translucent: `background: rgba(0, 0, 0, 0.3)` over KDE theme
- Elevation: subtle shadow or blur, never heavy outlines
- Borders: `var(--border)` from KDE theme, 1px minimum
- Backgrounds respect system theme light/dark

### Color
- Accent from KDE theme `var(--accent)`
- Muted text `var(--muted-foreground)`
- Strong hierarchy: headings > body > metadata
- State colors: pending (calm), snoozed (warning), blocked (alert), completed (subtle check)

### Typography
- System sans-serif with KDE size scaling
- Headings heavier, body lighter
- Line height 1.4-1.6 for body
- Monospace for time/duration indicators

### Animation
- Subtle entrance/exit (0.2s ease)
- Hover/focus state changes (0.15s)
- No auto-scrolling marquees or blinking
- Respect system reduce-motion setting

### Empty States
- Calm, instructional, not apologetic
- Show what to do next, not what's missing
- Example: "No tasks yet — capture your first with Super+Q"

## Error UX

### Principle
Errors explain the action required, never just state a code.

### Examples (from spec)
- ❌ Instead of: `CalDAV Error 409`
- ✅ Use: `The server has a newer version of this task.`
- `[ KEEP LOCAL ] [ USE SERVER ]`

### General Pattern
```
[Problem statement]
[What you can do]
[Primary action] [Secondary action]
```

### Never
- Modal with OK only (unless truly fatal)
- Silent failure
- Technical jargon without explanation
- Auto-assuming user preference

## Accessibility

### Motor
- Minimum 48dp hit targets
- 2.5:1 minimum focus contrast
- Keyboard operable everywhere
- No timing-required interactions without extension

### Visual
- 4.5:1 minimum contrast for normal text
- 3:1 for UI components/incidental text
- Information not conveyed by color alone
- Text resize to 200% without loss of function

### Cognitive
- Consistent patterns across all plasmoids
- Clear language, no AI-isms or unclear abbreviations
- Logical tab order
- Instructions in plain language
- Options presented before required

## Privacy by Design

### Data Minimization
- Only what's needed for the functionality is stored
- No telemetry, no usage tracking
- No account required for core functionality

### Local-First
- All core functionality works offline
- Synchronization is opt-in, not required
- Local data stored in SQLite under user's home

### Transparent Sync
- User configures which sources are enabled
- Explicit "KEEP LOCAL / USE SERVER" for conflicts
- No hidden synchronization

### No Cloud Dependencies
- Core: local tasks, local reminders
- Optional: CalDAV/Nextcloud sync
- No Google/Microsoft mandatory integration
- All AI optional, never required

## Design Checklist (per plasmoid)

- [ ] Native KDE — Kirigami, QML, themed surfaces
- [ ] Dark translucent where appropriate
- [ ] Strong visual hierarchy
- [ ] Large click targets (48dp minimum)
- [ ] Keyboard navigable
- [ ] Accessible contrast
- [ ] Reduced motion respected
- [ ] No AI required for core function
- [ ] Privacy-first — no telemetry
- [ ] Works offline
- [ ] Error messages explain action required
- [ ] Consistent patterns with other ADHD Plasma plasmoids
- [ ] Follow KDE theme colors via vars