/* Attention Service
   Manages persistent reminder state with full state machine:
   - States: pending, acknowledged, snoozed, completed, rescheduled, blocked
   - Persistence: SQLite (survives reboot)
   - "Closing notification ≠ completion" contract
   - Escalation intervals, snooze presets, quiet hours
*/

import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.Kirigami 2.0

ServiceView {
    id: attentionService
    
    /* SQLite-backed reminder model */
    /* Columns:
     * id, title, description, created_at, updated_at,
     * status: {pending, acknowledged, snoozed, completed, rescheduled, blocked},
     * snooze_until, quiet_until, escalation_count,
     * last_notified_at, quiet_hours_start, quiet_hours_end
     */
     
    /* State machine transitions:
     * pending → acknowledged (on view)
     * pending → snoozed (on snooze)
     * pending → rescheduled (user request)
     * any → completed (on DONE action)
     * snoozed → pending (when snooze_until reached)
     * blocked → pending (block resolved)
     */
     
    /* Core methods:
     * - addReminder(title, opts)
     * - getPending()
     * - getById(id)
     * - transitionTo(id, newState)
     * - snooze(id, presetOrDuration)
     * - complete(id)
     * - checkEscalation() — called periodically
     * - setQuietHours(start, end)
     */
     
    /* Snooze presets: 5min, 15min, 30min, 1hour, 2hours, custom */
    /* Escalation: configurable intervals, respect quiet hours */
    /* Quiet hours: user-configurable, suppress non-urgent reminders */
}