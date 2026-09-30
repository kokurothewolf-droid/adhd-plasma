/* Reminders Service
   Persistent reminder management
   - Configurable escalation intervals
   - Snooze presets (5 min, 15 min, 1 hour, etc.)
   - Quiet hours support
   - Persistence level configuration
   - Survives reboot
   - Integration with Attention Service state machine
*/

import QtQuick 2.15
import org.kde.kirigami 2.0

ServiceView {
    id: remindersService
    
    /* Core data model - linked to Attention Service SQLite */
    /* Fields:
     * id, title, description, created_at, updated_at,
     * status: {pending, acknowledged, snoozed, completed, rescheduled, blocked},
     * snooze_until, quiet_until, source: {local, caldav, akonadi},
     * remote_id, attention_service_id (link to AS state)
     */
     
    /* Core methods:
     * - createReminder(text, type, due_at, source)
     *   - type: {task, reminder, event, note, distraction}
     *   - source: {local, caldav, akonadi}
     * - snooze(id, presetOrDuration)
     *   - preset: {5min, 15min, 30min, 1hour, 2hours, custom}
     * - markCompleted(id)
     * - setQuietHours(start, end) — HH:mm format
     * - getActive() — returns pending + snoozed (not yet completed)
     * - syncWithAttentionService() — sync state with AS state machine
     * - applyEscalation() — if pending > escalation_interval, mark for escalation
     */
     
    /* Persistence configuration:
     * - localOnly: boolean — if true, no CalDAV sync
     * - defaultList: string — default CalDAV task list name
     * - escalationInterval: number — minutes before escalation
     * - snoozePresets: string[] — available snooze durations
     * - quietHours: {start: "HH:mm", end: "HH:mm"}
     */
}