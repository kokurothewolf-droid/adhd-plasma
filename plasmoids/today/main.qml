import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.kirigami.addons 2.0

/* TODAY plasmoid - Left-side time awareness panel
   Shows NOW → NEXT → LATER merged from calendar/task sources
*/

import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.kirigami.addons 2.0

Kirigami.AbstractCard {
    title: i18n("Today")

    // Fake/local data model - Phase 1
    // Later: merge from Akonadi/CalDAV
    property stringList nowActions: ["Fix schedule builder layout"]
    property stringList nextEvents: ["3:00 Team Meeting - Wrap up at 2:40"]
    property stringList laterItems: ["Laundry", "Dinner", "Medication"]

    // Activities integration flag
    property bool hasActivities: false /* Set at runtime from RecoveryService */

    // NOW section
    Kirigami.FlexColumn {
        Kirigami.Label {
            text: i18n("NOW")
            font.pixelSize: 24
            font.weight: Qt.Bold
        }
        Kirigami.Label {
            text: i18n("Fix schedule builder layout")
            font.pixelSize: 28
            font.weight: Qt.Bold
        }
        Kirigami.Label {
            text: i18n("27 min remaining")
            .textColor: Kirigami.Theme.textMuted
        }
    }

    // NEXT section with calendar event awareness
    Kirigami.FlexColumn {
        Kirigami.Label {
            text: i18n("NEXT")
            font.pixelSize: 24
            font.weight: Qt.Bold
        }
        // Show next event from calendar
        Kirigami.Label {
            text: i18n("3:00 Team Meeting")
            font.pixelSize: 24
        }
        // Transition warning
        Kirigami.Label {
            text: i18n("Wrap up at 2:40\nJoin link ready")
            .textColor: Kirigami.Theme.textMuted
            .wrapMode: Text.Wrap
        }
        // Activity awareness
        if (hasActivities) {
            Kirigami.Label {
                text: i18n("Active in: KindCue")
                .textColor: Kirigami.Theme.accent
                .fontPixelSize: 12
            }
        }
    }

    // LATER section
    Kirigami.FlexColumn {
        Kirigami.Label {
            text: i18n("LATER")
            font.pixelSize: 24
            font.weight: Qt.Bold
        }
        Kirigami.Label { text: i18n("Laundry") }
        Kirigami.Label { text: i18n("Dinner") }
        Kirigami.Label { text: i18n("Medication") }
    }
}