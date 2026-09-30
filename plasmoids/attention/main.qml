import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.kirigami.addons 2.0

/* ATTENTION Queue plasmoid
   Persistent reminders that survive reboot
   States: pending, acknowledged, snoozed, completed, rescheduled, blocked
   Key contract: Closing notification ≠ completion
*/

Kirigami.AbstractCard {
    title: i18n("Attention")

    // Phase 1: local/fake data
    // Later: from CalDAV/Akonadi with ADHD-specific metadata

    // Persistent reminders list
    Kirigami.FlexColumn {
        Kirigami.Label {
            text: i18n("Laundry")
            .textColor: Kirigami.Theme.text
        }
        Kirigami.Label {
            text: i18n("Finished 28 min ago")
            .textColor: Kirigami.Theme.textMuted
        }
        // State actions
        Kirigami.Row {
            Kirigami.Button {
                text: i18n("DONE")
                .flat: true
            }
            Kirigami.Button {
                text: i18n("REMIND AGAIN")
                .flat: true
            }
        }
    }

    // Contract notice
    Kirigami.Label {
        text: i18n("Closing this notification does NOT mark it complete")
           .textColor: Kirigami.Theme.textMuted
           .fontPixelSize: 12
    }
}