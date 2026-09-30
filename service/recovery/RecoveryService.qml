/* Recovery Service
   After meaningful inactivity or context switching
   "WELCOME BACK" card with last work + next action
   Research: KDE Activities, KWin session restoration, recent-document APIs
   Do not fake unsupported functionality
   Integration with KDE Activities and session management
*/

import QtQuick 2.15
import org.kde.kirigami 2.0

/* Check if KDE Activities QML module is available at runtime */
hasActivities: hasQmlModule("org.kde.activities")

ServiceView {
    id: recoveryService

    /* Trigger conditions:
     * - Meaningful inactivity (configurable threshold, default 15 min)
     * - Context switch detection (window change, task change)
     * - Session restore on reboot (SQLite recovery record)
     * - KDE Activities changed (checked at runtime)
     */

    /* Output:
     * WELCOME BACK
     * You were working on: KindCue - Fix schedule builder
     * Last active: 42 min ago
     * Next action: Fix spacing beneath schedule cards
     * [RESUME]
     *
     * State restoration:
     * - Read last active task from SQLite
     * - Restore task state (what was the user doing)
     * - Offer [RESUME] to return to that task
     * - Offer [NEW TASK] to capture something new
     * - Do not fake unsupported functionality
     *   - If hasActivities: use Activities.api.currentActivity()
     *   - If KWin session restoration available: leverage it
     *   - Otherwise: graceful degradation with local state only
     */

    /* Core methods:
     * - checkInactivity(seconds) — returns true if threshold exceeded
     * - detectContextSwitch() — window title/task change analysis
     * - saveCurrentState() — persist what user was working on
     * - restoreLastState() — offer to resume last task
     * - clearRecoveryState() — after user acts
     * - setInactivityThreshold(seconds) — configurable, default 15 min
     * - getLastActiveInfo() — {task, project, minutesAgo}
     * - isActivitiesAvailable() — runtime check, true if hasActivities
     * - getCurrentActivity() — {id, name, summary} from Activities.api
     */
}