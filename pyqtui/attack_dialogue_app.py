from pathlib import Path
from attack_dialogue_ui import Ui_AttackDialogue
from srd.srd_datastructs import BaseAttack, MeleeWeaponAttack, MeleeSpellAttack, RangedWeaponAttack, \
    RangedSpellAttack, AbilityScore, DamageType
from PyQt6.QtWidgets import QApplication, QDialog, QComboBox, QTableWidgetItem, QWidget
from srd.srd_generator import generate_test_melee_attack
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
CURRENT_DIRECTORY = Path(__file__).resolve().parent


class AttackDialog(QDialog, Ui_AttackDialogue):
    def __init__(self, attack=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        if attack is None:
            self.attack = MeleeWeaponAttack()
        else:
            self.attack = attack

        self.delete_attack = False

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
        for widget in self.groupBox.findChildren(QWidget):
            widget.blockSignals(True)
        self.attack_name_edit.setText(self.attack.name)
        set_combo_box_selected_item(self.attack_type_combobox, self.attack.type.value)
        set_combo_box_selected_item(self.attack_modifier_combobox, self.attack.attack_mod.value)
        self.targets_edit.setText(self.attack.targets)
        self.attack_description_edit.setPlainText(self.attack.description)
        print(f"Damage String {self.attack.damage_dice}")
        for i, damagedice in enumerate(self.attack.damage_dice):
            dicestring = damagedice['dicestring']
            damagetype = damagedice['damagetype'].value
            print(f'Damage Dice {dicestring} {damagetype}')
            self.damage_tablewidget.setItem(i, 0, QTableWidgetItem(dicestring))
            set_combo_box_selected_item(self.damage_tablewidget.cellWidget(i, 1), damagetype)
        if self.attack.type == BaseAttack.AttackType.MELEEWEAPON or \
                self.attack.type == BaseAttack.AttackType.MELEESPELL:
            self.reach_spinbox.setEnabled(True)
            self.range_spinbox.setEnabled(False)
            self.short_range_spinbox.setEnabled(False)
            self.long_range_spinbox.setEnabled(False)
            self.reach_spinbox.setValue(self.attack.reach)
        elif self.attack.type == BaseAttack.AttackType.RANGEDWEAPON:
            self.short_range_spinbox.setEnabled(True)
            self.long_range_spinbox.setEnabled(True)
            self.reach_spinbox.setEnabled(False)
            self.range_spinbox.setEnabled(False)
            self.short_range_spinbox.setValue(self.attack.short_range)
            self.long_range_spinbox.setValue(self.attack.long_range)
        elif self.attack.type == BaseAttack.AttackType.RANGEDSPELL:
            self.range_spinbox.setEnabled(True)
            self.reach_spinbox.setEnabled(False)
            self.short_range_spinbox.setEnabled(False)
            self.long_range_spinbox.setEnabled(False)
            self.range_spinbox.setValue(self.attack.range)
        else:
            raise TypeError("Invalid Attack Type for attack")
        for widget in self.groupBox.findChildren(QWidget):
            widget.blockSignals(False)

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
                                                attack_bonus=self.attack_bonus_spinbox.value(),
                                                damage_dice=self.get_damage_dice(),
                                                targets=self.targets_edit.text(),
                                                reach=self.reach_spinbox.value(),
                                                attack_mod=AbilityScore(self.attack_modifier_combobox.currentText()),
                                                description=self.attack_description_edit.toPlainText())
            elif attack_type == BaseAttack.AttackType.MELEESPELL:
                self.attack = MeleeSpellAttack(name=self.attack_name_edit.text(),
                                               attack_bonus=self.attack_bonus_spinbox.value(),
                                               damage_dice=self.get_damage_dice(),
                                               targets=self.targets_edit.text(),
                                               reach=self.reach_spinbox.value(),
                                               attack_mod=AbilityScore(self.attack_modifier_combobox.currentText()),
                                               description=self.attack_description_edit.toPlainText())
            elif attack_type == BaseAttack.AttackType.RANGEDWEAPON:
                self.attack = RangedWeaponAttack(name=self.attack_name_edit.text(),
                                                 attack_bonus=self.attack_bonus_spinbox.value(),
                                                 damage_dice=self.get_damage_dice(),
                                                 targets=self.targets_edit.text(),
                                                 short_range=self.short_range_spinbox.value(),
                                                 long_range=self.long_range_spinbox.value(),
                                                 attack_mod=AbilityScore(self.attack_modifier_combobox.currentText()),
                                                 description=self.attack_description_edit.toPlainText())
            elif attack_type == BaseAttack.AttackType.RANGEDSPELL:
                self.attack = RangedSpellAttack(name=self.attack_name_edit.text(),
                                                attack_bonus=self.attack_bonus_spinbox.value(),
                                                damage_dice=self.get_damage_dice(),
                                                targets=self.targets_edit.text(),
                                                range=self.range_spinbox.value(),
                                                attack_mod=AbilityScore(self.attack_modifier_combobox.currentText()),
                                                description=self.attack_description_edit.toPlainText())

            self.update_attack()

        self.attack_name_edit.editingFinished.connect(name_changed)
        self.attack_bonus_spinbox.valueChanged.connect(attack_bonus_changed)
        self.damage_tablewidget.cellChanged.connect(self.damage_dice_changed)
        self.targets_edit.editingFinished.connect(targets_changed)
        self.reach_spinbox.valueChanged.connect(reach_changed)
        self.range_spinbox.valueChanged.connect(range_changed)
        self.short_range_spinbox.valueChanged.connect(short_range_changed)
        self.long_range_spinbox.valueChanged.connect(long_range_changed)
        self.attack_modifier_combobox.currentIndexChanged.connect(attack_mod_changed)
        self.attack_type_combobox.currentIndexChanged.connect(attack_type_changed)
        self.attack_description_edit.textChanged.connect(attack_description_changed)
        self.apply_attack_pushbutton.pressed.connect(self.on_apply_button_clicked)
        self.delete_attack_pushbutton.pressed.connect(self.on_delete_button_clicked)
        self.cancel_attack_pushbutton.pressed.connect(self.reject)

    def damage_dice_changed(self):
        self.attack.damage_dice = self.get_damage_dice()
        self.update_attack()

    def get_damage_dice(self):
        dice_list = []
        for row in range(self.damage_tablewidget.rowCount()):
            if self.damage_tablewidget.item(row, 0) is not None and \
                    self.damage_tablewidget.cellWidget(row, 1).currentText() != '':
                dice_list.append({"dicestring": self.damage_tablewidget.item(row, 0).text(),
                                  "damagetype": DamageType(self.damage_tablewidget.cellWidget(row, 1).currentText())})
        return dice_list

    def on_delete_button_clicked(self):
        self.delete_attack = True
        self.accept()

    def on_apply_button_clicked(self):
        self.accept()


def set_combo_box_selected_item(combo_box, item):
    index = -1
    print(range(combo_box.count()))
    print(f"Setting {combo_box.currentText()} index {item}")
    for i in range(combo_box.count()):
        print(f"{combo_box.itemText(i)} {item}")
        if combo_box.itemText(i) == item:
            index = i
            break

    if index != combo_box.currentIndex():
        print(f"Changing combo box index {item}")
        combo_box.setCurrentIndex(index)
        print(combo_box.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AttackDialog(attack=generate_test_melee_attack())
    myWindow.show()
    app.exec()
