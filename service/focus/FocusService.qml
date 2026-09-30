/* Focus Behavior
   Focus mode configuration
   "focus until next event"
   Transition warnings: wrap up in 20 min, meeting in 5 min
   One-click join for meeting URLs
   Integration with KDE calendar events and CalDAV backend
*/

import QtQuick 2.15
import org.kde.kirigami 2.0

ServiceView {
    id: focusService

    /* Focus mode configuration:
     * - focusMode: {untilNextEvent, timed, manual}
     *   untilNextEvent: auto-exit when next calendar event starts
     *   timed: auto-exit after configured duration
     *   manual: user controls exit
     * - transitionWarning: number — minutes before event to show wrap-up prompt
     * - meetingJoin: boolean — show one-click join for events with URLs
     * - focusTimer: number — minutes for timed mode (default 25 = Pomodoro)
     * - respectQuietHours: boolean — don't start focus during quiet hours
     * - calendarModel: model — provides {id, title, startAt, endAt} from CalDAV
     */

    /* Focus mode behavior:
     * - untilNextEvent: auto-exit when next calendar event starts
     *   - Polls calendarModel for next event start time
     *   - Shows "wrap up in N minutes" when event within threshold
     *   - Auto-exits when event start time reached
     * - timed: auto-exit after configured duration (focusTimer minutes)
     * - manual: user controls exit via stop() action
     */

    /* Transition warnings:
     * - "wrap up in 20 minutes" — configurable warning interval
     * - "meeting in 5 minutes" — from calendar event, shown in TODAY/NOW
     * - Escalate to ATTENTION queue if user ignores warning
     * - Dismissible with "Snooze for 10 min" action
     */

    /* One-click join:
     * - If calendar event has a meeting URL (Jitsi, Zoom, Teams, or custom)
     * - Expose in notification and NOW card
     * - Single click opens URL in default browser
     * - Fallback: copy URL to clipboard
     * - Shows "join in 5 min" before event start
     */

    /* Core methods:
     * - start(mode, durationMinutes) — begins focus session
     * - stop() — ends focus session
     * - getStatus() — returns {mode, remaining, nextEvent}
     * - setTransitionWarning(minutes) — warning interval before event
     * - setFocusTimer(minutes) — Pomodoro duration
     * - setMeetingJoinEnabled(enabled) — show join buttons
     * - isActive() — true if focus session running
     * - getNextEvent() — {title, startAt, minutesUntilStart} from calendar
     */
}
}