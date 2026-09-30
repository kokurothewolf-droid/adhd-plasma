import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.kirigami.addons 2.0

/* NOW plasmoid - Primary desktop card
   Shows only the current and immediate next action
*/

Kirigami.AbstractCard {
    title: i18n("Now")

    // Phase 1: local/fake data
    // Later: dynamic from Kalendar/Akonadi/CalDAV

    // Current action
    Kirigami.FlexColumn {
        Kirigami.Label {
            text: i18n("Fix schedule builder layout")
            font.pixelSize: 28
            font.weight: Qt.Bold
        }
        Kirigami.Label {
            text: i18n("KindCue")
           .textColor: Kirigami.Theme.textMuted
        }
        Kirigami.Label {
            text: i18n("18 min active")
            .textColor: Kirigami.Theme.textMuted
        }
    }

    // Actions row
    Kirigami.Row {
        Kirigami.Button {
            text: i18n("CONTINUE")
            .flat: true
        }
        Kirigami.Button {
            text: i18n("I'M STUCK")
            .flat: true
        }
    }
}