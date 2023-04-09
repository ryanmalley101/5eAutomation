from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
import sys
from attack_dialogue_ui import Ui_AttackDialogue
from srd.srd_datastructs import BaseAttack, MeleeWeaponAttack, MeleeSpellAttack, RangedWeaponAttack, RangedSpellAttack, AbilityScore, DamageType
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QListView, QSizePolicy, QComboBox, QPushButton, QCheckBox, QTextEdit, QTableWidgetItem, QWidget, QMainWindow
)
import os


class AttackDialog(QDialog, Ui_AttackDialogue):
    def __init__(self, attack=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        if attack is None:
            self.attack = MeleeWeaponAttack()
        else:
            self.attack = attack

        # connect button signals to slots
        self.delete_attack_pushbutton.clicked.connect(self.on_delete_button_clicked)
        self.apply_attack_pushbutton.clicked.connect(self.on_apply_button_clicked)
        self.cancel_attack_pushbutton.clicked.connect(self.reject)

        self.setup_comboboxes()
        self.update_attack()
        self.setup_signals()
        self.attack_name_edit.setFocus()

    def setup_comboboxes(self):
        self.attack_type_combobox.clear()
        for attack in BaseAttack.AttackType:
            self.attack_type_combobox.addItem(attack.value)
        for score in AbilityScore:
            self.attack_modifier_combobox.addItem(score.value)
        for row in range(self.damage_tablewidget.rowCount()):
            damage_combobox = QComboBox()
            damage_combobox.addItems([damage.value for damage in DamageType])
            # damage_combobox.currentTextChanged.connect(self.damage_dice_changed())
            self.damage_tablewidget.setCellWidget(row, 1, damage_combobox)

    def update_attack(self):
        self.attack_name_edit.setText(self.attack.name)
        set_combo_box_selected_item(self.attack_type_combobox, self.attack.type.value)
        set_combo_box_selected_item(self.attack_modifier_combobox, self.attack.attack_mod.value)
        self.targets_edit.setText(self.attack.targets)
        self.attack_description_edit.setPlainText(self.attack.description)
        for i, (dicestring, damagetype) in enumerate(self.attack.damage_dice):
            self.damage_tablewidget.setItem(i, 0, dicestring)
            self.damage_tablewidget.item(i, 1).setCurrentText(damagetype.value)
        if self.attack.type == BaseAttack.AttackType.MELEEWEAPON or self.attack.type == BaseAttack.AttackType.MELEESPELL:
            self.reach_spinbox.setValue(self.attack.reach)
            self.range_spinbox.setEnabled(False)
            self.short_range_spinbox.setEnabled(False)
            self.long_range_spinbox.setEnabled(False)
        elif self.attack.type == BaseAttack.AttackType.RANGEDWEAPON:
            self.short_range_spinbox.setValue(self.attack.short_range)
            self.long_range_spinbox.setValue(self.attack.long_range)
            self.reach_spinbox.setEnabled(False)
            self.range_spinbox.setEnabled(False)
        elif self.attack.type == BaseAttack.AttackType.RANGEDSPELL:
            self.range_edit.setText(self.attack.reach)
            self.reach_spinbox.setEnabled(False)
            self.short_range_spinbox.setEnabled(False)
            self.long_range_spinbox.setEnabled(False)
        else:
            raise TypeError("Invalid Attack Type for attack")

    def setup_signals(self):
        def name_changed():
            self.attack.name = self.attack_name_edit.text()
            self.update_attack()

        def attack_bonus_changed():
            self.attack.attack_bonus = self.attack_bonus_spinbox.value()
            self.update_attack()

        def targets_changed():
            self.attack.targets = self.targets_edit.text()
            self.update_attack()

        def reach_changed():
            self.attack.reach = self.reach_spinbox.value()
            self.update_attack()

        def range_changed():
            self.attack.range = self.range_spinbox.value()
            self.update_attack()

        def short_range_changed():
            self.attack.short_range = self.short_range_spinbox.value()
            self.update_attack()

        def long_range_changed():
            self.attack.long_range = self.long_range_spinbox.value()
            self.update_attack()

        def attack_mod_changed():
            self.attack.attack_mod = AbilityScore(self.attack_modifier_combobox.currentText())
            self.update_attack()

        def attack_description_changed():
            self.attack.description = self.attack_description_edit.toPlainText()
            self.update_attack()

        def attack_type_changed():
            attack_type = BaseAttack.AttackType(self.attack_type_combobox.currentText())
            if attack_type == BaseAttack.AttackType.MELEEWEAPON:
                self.attack = MeleeWeaponAttack(name=self.attack_name_edit.text(),
                                                type=BaseAttack.AttackType.MELEEWEAPON,
                                                attack_bonus=self.attack_bonus_spinbox.value(),
                                                damage_dice= self.get_damage_dice(),
                                                targets=self.targets_edit.text(),
                                                reach=self.reach_spinbox.value(),
                                                attack_mod=AbilityScore(self.attack_modifier_combobox.currentText()),
                                                description=self.attack_description_edit.toPlainText())


        self.attack_name_edit.editingFinished.connect(name_changed)
        self.attack_bonus_spinbox.valueChanged.connect(attack_bonus_changed)
        self.damage_tablewidget.cellChanged.connect(self.damage_dice_changed)
        self.targets_edit.editingFinished.connect(targets_changed)
        self.reach_spinbox.valueChanged.connect(reach_changed)
        self.range_spinbox.valueChanged.connect(range_changed)
        self.short_range_spinbox.valueChanged.connect(short_range_changed)
        self.long_range_spinbox.valueChanged.connect(long_range_changed)
        self.attack_modifier_combobox.currentTextChanged.connect(attack_mod_changed)
        self.attack_type_combobox.currentTextChanged.connect(attack_type_changed)
        self.attack_description_edit.textChanged.connect(attack_description_changed)

    def damage_dice_changed(self):
        self.attack.damage_dice = self.get_damage_dice()
        self.update_attack()

    def get_damage_dice(self):
        dice_list = []
        for row in self.damage_tablewidget.rowCount():
            dice_list.append((self.damage_tablewidget.item(row, 0), DamageType(self.damage_tablewidget.item(row, 1).currentText())))
        return dice_list


    def on_delete_button_clicked(self):
        self.delete_attack = True
        self.accept()

    def on_apply_button_clicked(self):
        self.accept()


def set_combo_box_selected_item(combo_box, item):
    index = -1
    for i in range(combo_box.count()):
        print(f"{combo_box.itemText(i)} {item}" )
        if combo_box.itemText(i) == item:
            index = i
            break

    combo_box.setCurrentIndex(index)
    print(combo_box.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AttackDialog(attack=None)
    myWindow.show()
    app.exec()
