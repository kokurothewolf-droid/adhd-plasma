import QtQuick 2.15
import org.kde.kirigami 2.0
import org.kde.kirigami.addons 2.0

/* CAPTURE plasmoid
   Global shortcut: Super+Q (configurable)
   Opens minimal capture field
   Types: task, reminder, event, note, distraction/idea
   NL date parsing: "remind me in 20 minutes to switch laundry"
*/

Kirigami.AbstractCard {
    title: i18n("Capture")

    // Phase 1: minimal capture field
    // Later: KalDAV add item, date parsing enhancement

    // Capture input
    Kirigami.InputField {
        id: captureField
        placeholderText: i18n("e.g. 'remind me in 20 minutes to switch laundry'")
        // Return key submits
    }

    // Quick presets row
    Kirigami.Row {
        Kirigami.Button {
            text: i18n("Switch laundry in 20 min")
            onClicked: {
                captureField.text = i18n("remind me in 20 minutes to switch laundry")
                captureField.accept()
            }
        }
        Kirigami.Button {
            text: i18n("Dentist tomorrow 10am")
            onClicked: {
                captureField.text = i18n("dentist tomorrow at 10")
                captureField.accept()
            }
        }
        Kirigami.Button {
            text: i18n("Buy cat litter")
            onClicked: {
                captureField.text = i18n("buy cat litter")
                captureField.accept()
            }
        }
    }

    // Capture action buttons
    Kirigami.Row {
        Kirigami.Button {
            text: i18n("Capture")
            .default: true
            onClicked: captureField.accept()
        }
        Kirigami.Button {
            text: i18n("Cancel")
            .flat: true
            onClicked: captureField.reject()
        }
    }
}