from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from pyqtui.attack_dialogue_ui import Ui_AttackDialogue
from srd.srd_datastructs import BaseAttack, MeleeWeaponAttack, MeleeSpellAttack, RangedWeaponAttack, RangedSpellAttack

class AttackDialog(QDialog, Ui_AttackDialogue):
    def __init__(self, attack:BaseAttack=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # connect button signals to slots
        self.delete_attack_pushbutton.clicked.connect(self.on_delete_button_clicked)
        self.apply_attack_pushbutton.clicked.connect(self.on_apply_button_clicked)
        self.cancel_attack_pushbutton.clicked.connect(self.reject)
        # if an ability is provided, populate the input fields
        if attack is not None:
            self.ability = attack
        else:
            self.ability = BaseAttack()

        self.setup_comboboxes()

        self.attack_name_edit.setText(attack.name)

        self.attack_description_edit.setPlainText(attack.description)

         # set the focus to the name edit widget
        self.attack_name_edit.setFocus()

    # def setup_checkboxes(self):


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

