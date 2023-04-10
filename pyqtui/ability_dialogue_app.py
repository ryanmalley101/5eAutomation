from PyQt6.QtWidgets import QDialog
from pyqtui.ability_dialogue_ui import Ui_AbilityDialogueUi
from srd.srd_datastructs import AbilityDescription


class AbilityDialog(QDialog, Ui_AbilityDialogueUi):
    def __init__(self, ability: AbilityDescription, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.delete_ability = False

        # connect button signals to slots
        self.delete_ability_pushbutton.clicked.connect(self.on_delete_button_clicked)
        self.apply_ability_pushbutton.clicked.connect(self.on_apply_button_clicked)
        self.cancel_ability_pushbutton.clicked.connect(self.reject)
        # if an ability is provided, populate the input fields
        if ability is not None:
            self.ability = ability
        else:
            self.ability = AbilityDescription()

        self.ability_name_edit.setText(ability.name)
        self.ability_description_edit.setPlainText(ability.description)

        # set the focus to the name edit widget
        self.ability_name_edit.setFocus()

    def on_delete_button_clicked(self):
        self.delete_ability = True
        self.ability = AbilityDescription(name=self.ability_name_edit.text(),
                                          description=self.ability_description_edit.toPlainText())
        self.accept()

    def on_apply_button_clicked(self):
        # populate self.ability_info with user input
        self.ability = AbilityDescription(name=self.ability_name_edit.text(),
                                          description=self.ability_description_edit.toPlainText())
        self.accept()
