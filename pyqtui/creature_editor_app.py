import os
import sys
from pathlib import Path
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from creatures import creature_datastructs
from srd.srd_datastructs import AbilityScore, Size, Skill, Condition, DamageType, proficiency_bonus, score_to_mod, BaseAttack

from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QListView, QSizePolicy, QComboBox, QPushButton, QCheckBox, QTextEdit, QTableWidgetItem
)

from srd_gui_objects import AbilityButton, AbilityDescription, AttackButton
from PyQt6 import QtCore

from creature_editor_ui import Ui_Form
from creatures.creature_generator import generate_test_creature

CURRENT_DIRECTORY = Path(__file__).resolve().parent


class MonsterEditorForm(QDialog, Ui_Form):
    def __init__(self, creature_block: creature_datastructs.MonsterStatblock, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        QtCore.QDir.addSearchPath('images', os.fspath(CURRENT_DIRECTORY / "images"))
        self.creature_block = creature_block
        self.setup_comboboxes()
        self.set_stylesheet()
        self.setup_checkbox_signals()
        self.setup_label_signals()
        self.update_creature_data()

    def set_stylesheet(self):
        # Sets the stylesheet for derived elements like hit die size and prof bonus
        def set_derived_styles():
            derived_stylesheet = 'background-color: rgb(235, 146, 52); font: 16pt "Cambria";'
            self.proficiency_bonus_calculation_label.setStyleSheet(derived_stylesheet)
            self.hit_die_calculation_label.setStyleSheet(derived_stylesheet)
            self.str_mod_label.setStyleSheet(derived_stylesheet)
            self.dex_mod_label.setStyleSheet(derived_stylesheet)
            self.con_mod_label.setStyleSheet(derived_stylesheet)
            self.int_mod_label.setStyleSheet(derived_stylesheet)
            self.wis_mod_label.setStyleSheet(derived_stylesheet)
            self.cha_mod_label.setStyleSheet(derived_stylesheet)

        self.setStyleSheet('QWidget{font: 12pt "Cambria"}')
        self.topframe.setStyleSheet('#topframe{background-image: url(images:papyrusbackground.jpg)}')
        self.scrollArea.setStyleSheet('#scrollArea{background-image: url(images:papyrusbackground.jpg)}')
        self.scrollAreaWidgetContents.setStyleSheet('#scrollAreaWidgetContents{background-image: url(images:papyrusbackground.jpg)}')
        for widget in self.topframe.findChildren((QLabel, QListView, QLineEdit, QComboBox, QPushButton, QCheckBox, QTextEdit)):
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; color: rgb(166, 60, 6); font: 16pt "Cambria";}}')
                widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
            elif isinstance(widget, QListView) or isinstance(widget, QTextEdit):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
            elif isinstance(widget, QLineEdit):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
            elif isinstance(widget, QComboBox):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
            elif isinstance(widget, QPushButton):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: rgb(111, 115, 47); color: white; font: 12pt "Cambria";}}')
            elif isinstance(widget, QCheckBox):
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: rgb(111, 115, 47); color: white; font: 12pt "Cambria";}}')
        self.abilities_list_groupbox.setStyleSheet(f'#{self.abilities_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.actions_list_groupbox.setStyleSheet(f'#{self.actions_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.bonus_actions_list_groupbox.setStyleSheet(f'#{self.abilities_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.reactions_list_groupbox.setStyleSheet(f'#{self.reactions_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.bonus_actions_list_groupbox.setStyleSheet(f'#{self.bonus_actions_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.legendary_actions_list_groupbox.setStyleSheet(f'#{self.legendary_actions_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')
        self.mythic_actions_list_groupbox.setStyleSheet(f'#{self.mythic_actions_list_groupbox.objectName()}{{background-image: none; background-color: white; color: black; font: 12pt "Cambria";}}')


        set_derived_styles()
        return None

    def setup_comboboxes(self):
        # Size combobox
        self.size_combobox.clear()
        for size in creature_datastructs.Size:
            self.size_combobox.addItem(size.name)
        for cr in creature_datastructs.CR_TO_XP_TABLE:
            self.challenge_rating_combobox.addItem(str(cr))
        for save in creature_datastructs.AbilityScore:
            self.saving_throws_combobox.addItem(save.value)
        for skill in Skill:
            self.skills_combobox.addItem(skill.value)
        for condition in Condition:
            self.conditions_combobox.addItem(condition.value)
        for damage in DamageType:
            self.damage_combobox.addItem(damage.value)
        return True

    def setup_checkbox_signals(self):
        def toggle_container_visibility(checkbox, container):
            checkbox_checked = checkbox.isChecked()
            print(f"Toggling {container} visibility to {checkbox_checked}")
            container.setVisible(True if checkbox_checked else False)
            checkbox.setText("Enabled" if checkbox_checked else "Disabled")

        self.reactions_enable_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(self.reactions_enable_checkbox, self.reactions_container))
        self.reactions_container.setVisible(False)

        self.bonus_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(self.bonus_actions_enabled_checkbox, self.bonus_actions_container))
        self.bonus_actions_container.setVisible(False)

        self.legendary_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(self.legendary_actions_enabled_checkbox, self.legendary_actions_container))
        self.legendary_actions_container.setVisible(False)

        self.mythic_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(self.mythic_actions_enabled_checkbox, self.mythic_actions_container))
        self.mythic_actions_container.setVisible(False)

    def setup_pushbutton_signals(self):
        self.save_button.pressed.connect(self.add_save_proficiency)

    def add_save_proficiency(self):
        selected_save = AbilityScore(self.saving_throws_combobox.currentText())
        if selected_save not in self.creature_block.saving_throws:
            self.creature_block.saving_throws.add(selected_save)
        self.update_creature_data()

    # def add_skill_proficiency(self):
    #     selected_skill = AbilityScores(self.saving_throws_combobox.currentText())
    #     if selected_save not in self.creature_block.saving_throws:
    #         self.creature_block.saving_throws.add(selected_save)
    #     self.update_creature_data()

    def setup_label_signals(self):
        self.str_edit.editingFinished.connect(lambda: update_modifier(self.str_edit.text(), self.str_mod_label))
        self.dex_edit.editingFinished.connect(lambda: update_modifier(self.dex_edit.text(), self.dex_mod_label))
        self.con_edit.editingFinished.connect(lambda: update_modifier(self.con_edit.text(), self.con_mod_label))
        self.int_edit.editingFinished.connect(lambda: update_modifier(self.int_edit.text(), self.int_mod_label))
        self.wis_edit.editingFinished.connect(lambda: update_modifier(self.wis_edit.text(), self.wis_mod_label))
        self.cha_edit.editingFinished.connect(lambda: update_modifier(self.cha_edit.text(), self.cha_mod_label))
        self.size_combobox.currentIndexChanged.connect(lambda text: update_hitdice(Size(text), self.hit_die_calculation_label))
        self.challenge_rating_combobox.currentIndexChanged.connect(lambda text: update_prof_bonus(text, self.proficiency_bonus_calculation_label))

    def update_creature_data(self):
        def initsaves():
            for save in self.creature_block.saving_throws:
                self.save_listwidget.addItem(save.value)

        def initskills():
            for skill in self.creature_block.skills.keys():
                self.skills_listwidget.addItem(skill)

        def initconditions():
            for condition in self.creature_block.conditionimmunities:
                self.condition_listwidget.addItem(condition.value)

        def initdamage():
            def insert_damage_row(damagetype, modifier):
                self.damage_tablewidget.insertRow(self.damage_tablewidget.rowCount())
                self.damage_tablewidget.setItem(self.damage_tablewidget.rowCount() - 1, 0, QTableWidgetItem(damagetype))
                self.damage_tablewidget.setItem(self.damage_tablewidget.rowCount() - 1, 1, QTableWidgetItem(modifier))

            for damage in self.creature_block.damagevulnerabilities:
                insert_damage_row(damage, 'vulnerable')
            for damage in self.creature_block.damageresistances:
                insert_damage_row(damage, 'resistant')
            for damage in self.creature_block.damageimmunities:
                insert_damage_row(damage, 'immune')

        def insert_ability(layout, ability):
            new_ability = AbilityButton(ability)
            layout.addWidget(new_ability)

        def insert_attack(layout, attack):
            new_attack = AttackButton(attack, self.creature_block)
            print(new_attack.text())
            layout.addWidget(new_attack)

        def initabilities():
            for ability in self.creature_block.abilities:
                insert_ability(self.abilities_list_layout, ability)

        def initactions():
            for action in self.creature_block.actions:
                if isinstance(action, AbilityDescription):
                    print("Adding ability action")
                    insert_ability(self.actions_list_layout, action)
                elif isinstance(action, BaseAttack):
                    print("Adding attack action")
                    insert_attack(self.actions_list_layout, action)
                else:
                    print("Invalid action")

        def initreactions():
            for reaction in self.creature_block.reactions:
                insert_ability(self.reactions_list_layout, reaction)

        def initbonusactions():
            for bonusactions in self.creature_block.bonusactions:
                insert_ability(self.bonus_actions_list_layout, bonusactions)

        def initlegendaryactions():
            for legendaryactions in self.creature_block.legendaryactions:
                insert_ability(self.legendary_actions_list_layout, legendaryactions)

        def initmythicactions():
            for mythicactions in self.creature_block.mythicactions:
                insert_ability(self.mythic_actions_list_layout, mythicactions)


        print(self.creature_block.name)
        self.name_edit.setText(self.creature_block.name)
        set_combo_box_selected_item(self.size_combobox, self.creature_block.size.name)
        self.type_edit.setText(self.creature_block.type)
        self.tag_edit.setText(self.creature_block.tag)
        self.alignment_edit.setText(self.creature_block.alignment)
        self.proficiency_bonus_calculation_label.setText(str(proficiency_bonus(self.creature_block.challengerating)))
        set_combo_box_selected_item(self.challenge_rating_combobox, str(self.creature_block.challengerating))
        self.xp_calculation_label.setText(str(
            creature_datastructs.CR_TO_XP_TABLE[self.creature_block.challengerating]))
        self.proficiency_bonus_calculation_label.setText(str(
            creature_datastructs.proficiency_bonus(self.creature_block.challengerating)))
        self.hit_points_edit.setText(str(self.creature_block.hitpoints))
        self.max_hit_dice_edit.setText(self.creature_block.hitdice)
        self.hit_die_calculation_label.setText(f"d{creature_datastructs.Size.hitdice(self.creature_block.size)}")
        self.ac_bonus_edit.setText(str(self.creature_block.acbonus))
        self.armor_type_edit.setText(self.creature_block.acdesc)
        self.senses_edit.setText(self.creature_block.senses)
        self.speeds_edit.setText(self.creature_block.speed)
        self.str_edit.setText(str(self.creature_block.ability_scores[AbilityScore.STRENGTH]))
        update_modifier(self.str_edit.text(), self.str_mod_label)
        self.dex_edit.setText(str(self.creature_block.ability_scores[AbilityScore.DEXTERITY]))
        update_modifier(self.dex_edit.text(), self.dex_mod_label)
        self.con_edit.setText(str(self.creature_block.ability_scores[AbilityScore.CONSTITUTION]))
        update_modifier(self.con_edit.text(), self.con_mod_label)
        self.int_edit.setText(str(self.creature_block.ability_scores[AbilityScore.INTELLIGENCE]))
        update_modifier(self.int_edit.text(), self.int_mod_label)
        self.wis_edit.setText(str(self.creature_block.ability_scores[AbilityScore.WISDOM]))
        update_modifier(self.wis_edit.text(), self.wis_mod_label)
        self.cha_edit.setText(str(self.creature_block.ability_scores[AbilityScore.CHARISMA]))
        update_modifier(self.cha_edit.text(), self.cha_mod_label)
        initsaves()
        initskills()
        initconditions()
        initdamage()
        initabilities()
        initactions()
        initbonusactions()
        initreactions()
        initlegendaryactions()
        initmythicactions()

def set_combo_box_selected_item(combo_box, item):
    index = -1
    for i in range(combo_box.count()):
        print(f"{combo_box.itemText(i)} {item}" )
        if combo_box.itemText(i) == item:
            index = i
            break

    combo_box.setCurrentIndex(index)
    print(combo_box.currentText())


def update_modifier(score, modifier_label):
    if score.isdigit():
        mod = score_to_mod(int(score))
        modstr = f'+{mod}' if mod >= 0 else f'{mod}'
        modifier_label.setText(modstr)
    else:
        raise TypeError("Tried to update a score modifier with a non integer value")


def update_hitdice(size, modifier_label):
    if isinstance(size, Size):
        modifier_label.setText(str(f"d{Size.hitdice(size)}"))
    else:
        raise TypeError("Tried to enter a non-Size value to calculate hitdice")


def update_prof_bonus(cr, modifier_label):
    modifier_label.setText(f'+{proficiency_bonus(cr)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MonsterEditorForm(creature_block=generate_test_creature(), parent=None)
    myWindow.show()
    app.exec()