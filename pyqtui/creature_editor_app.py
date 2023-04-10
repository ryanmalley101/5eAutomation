from pathlib import Path
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QListView, QSizePolicy, QComboBox, QPushButton, QCheckBox, QTextEdit,
    QTableWidgetItem, QWidget, QSpinBox, QFileDialog
)
from pyqtui.srd_gui_objects import AbilityButton, AbilityDescription, AttackButton
from pyqtui.designer_ui.creature_editor_ui import Ui_Form
from pyqtui.ability_dialogue_app import AbilityDialog
from pyqtui.attack_dialogue_app import AttackDialog
from pyqtui.gmbinder_convert_window import GMBinderConvertWindow

from creatures import creature_datastructs
from srd.srd_datastructs import AbilityScore, Size, Skill, Condition, DamageType, proficiency_bonus, score_to_mod, \
    BaseAttack, PROFICIENT, EXPERT, DamageModifier, MeleeWeaponAttack
from creatures.creature_generator import generate_test_monster
from gmbinderconvert.convert_creature import convert_monster

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
CURRENT_DIRECTORY = Path(__file__).resolve().parent


class MonsterEditorForm(QWidget, Ui_Form):
    def __init__(self, creature_block: creature_datastructs.MonsterStatblock, parent=None):
        super().__init__()
        self.setupUi(self)
        QtCore.QDir.addSearchPath('images', os.fspath(CURRENT_DIRECTORY / "images"))
        self.creature_block = creature_block
        self.setup_comboboxes()
        self.set_stylesheet()
        self.update_creature_data()
        self.setup_checkbox_signals()
        self.setup_spinbox_signals()
        self.setup_combobox_signals()
        self.setup_pushbutton_signals()
        if self.creature_block.bonusactions:
            self.bonus_actions_enabled_checkbox.setChecked(True)
        if self.creature_block.reactions:
            self.reactions_enable_checkbox.setChecked(True)
        if self.creature_block.legendaryactions:
            self.legendary_actions_enabled_checkbox.setChecked(True)
        if self.creature_block.mythicactions:
            self.mythic_actions_enabled_checkbox.setChecked(True)

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

        papyrus_background_stylesheet = '{background-image: url(images:papyrusbackground.jpg)}'
        plain_text_stylesheet = f'{{background-image: none; background-color: white; ' \
                                f'color: black; font: 12pt "Cambria";}}'
        modal_stylesheet = '{{background-image: none; background-color: rgb(111, 115, 47); ' \
                           'color: white; font: 12pt "Cambria";}}'
        label_stylesheet = '{{background-image: none; color: rgb(166, 60, 6); font: 16pt "Cambria";}}'

        self.setStyleSheet('QWidget{font: 12pt "Cambria"}')
        self.topframe.setStyleSheet(f'#topframe{papyrus_background_stylesheet}')
        self.scrollArea.setStyleSheet(f'#scrollArea{papyrus_background_stylesheet}')
        self.scrollAreaWidgetContents.setStyleSheet(f'#scrollAreaWidgetContents{papyrus_background_stylesheet}')
        for widget in self.topframe.findChildren((QLabel, QListView, QLineEdit, QComboBox,
                                                  QPushButton, QCheckBox, QTextEdit, QComboBox)):
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f'#{widget.objectName()}{label_stylesheet}')
                widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
            elif isinstance(widget, QListView) or isinstance(widget, QTextEdit):
                widget.setStyleSheet(f'#{widget.objectName()}{plain_text_stylesheet}')
            elif isinstance(widget, QLineEdit):
                widget.setStyleSheet(f'#{widget.objectName()}{plain_text_stylesheet}')
            elif isinstance(widget, QComboBox):
                widget.setStyleSheet(f'#{widget.objectName()}{plain_text_stylesheet}')
            elif isinstance(widget, QSpinBox):
                widget.setStyleSheet(f'#{widget.objectName()}{plain_text_stylesheet}')
            elif isinstance(widget, QPushButton):
                widget.setStyleSheet(f'#{widget.objectName()}{modal_stylesheet}')
            elif isinstance(widget, QCheckBox):
                widget.setStyleSheet(f'#{widget.objectName()}{modal_stylesheet}')

        self.abilities_list_groupbox.setStyleSheet(
            f'#{self.abilities_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.actions_list_groupbox.setStyleSheet(
            f'#{self.actions_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.bonus_actions_list_groupbox.setStyleSheet(
            f'#{self.abilities_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.reactions_list_groupbox.setStyleSheet(
            f'#{self.reactions_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.bonus_actions_list_groupbox.setStyleSheet(
            f'#{self.bonus_actions_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.legendary_actions_list_groupbox.setStyleSheet(
            f'#{self.legendary_actions_list_groupbox.objectName()}{papyrus_background_stylesheet}')
        self.mythic_actions_list_groupbox.setStyleSheet(
            f'#{self.mythic_actions_list_groupbox.objectName()}{papyrus_background_stylesheet}')

        set_derived_styles()
        return None

    def setup_comboboxes(self):
        # Size combobox
        self.size_combobox.clear()
        for size in Size:
            self.size_combobox.addItem(size.value)
        for cr in creature_datastructs.CR_TO_XP_TABLE:
            self.challenge_rating_combobox.addItem(str(cr))
        for save in AbilityScore:
            self.saving_throws_combobox.addItem(save.value)
        for skill in Skill:
            self.skills_combobox.addItem(skill.value)
        for condition in Condition:
            self.conditions_combobox.addItem(condition.value)
        for damage in DamageType:
            self.damage_combobox.addItem(damage.value)
        return True

    def setup_lineedit_signals(self):
        self.name_edit.editingFinished.connect(self.name_edit_changed)
        self.type_edit.editingFinished.connect(self.type_edit_changed)
        self.tag_edit.editingFinished.connect(self.tag_edit_changed)
        self.alignment_edit.editingFinished.connect(self.alignment_edit_changed)
        self.armor_type_edit.editingFinished.connect(self.armor_type_edit_changed)
        self.senses_edit.editingFinished.connect(self.senses_edit_changed)
        self.speeds_edit.editingFinished.connect(self.speed_edit_changed)

    def setup_spinbox_signals(self):
        self.str_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.str_score_spinbox.value(), self.str_mod_label, AbilityScore.STRENGTH))
        self.dex_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.dex_score_spinbox.value(), self.dex_mod_label, AbilityScore.DEXTERITY))
        self.con_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.con_score_spinbox.value(), self.con_mod_label, AbilityScore.CONSTITUTION))
        self.int_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.int_score_spinbox.value(), self.int_mod_label, AbilityScore.INTELLIGENCE))
        self.wis_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.wis_score_spinbox.value(), self.wis_mod_label, AbilityScore.WISDOM))
        self.cha_score_spinbox.valueChanged.connect(lambda: self.score_edit_changed(
            self.cha_score_spinbox.value(), self.cha_mod_label, AbilityScore.CHARISMA))
        self.hit_points_spinbox.valueChanged.connect(self.hit_points_edit_changed)
        self.max_hit_dice_spinbox.valueChanged.connect(self.hit_dice_edit_changed)
        self.ac_bonus_spinbox.valueChanged.connect(self.ac_bonus_edit_changed)

    def name_edit_changed(self):
        self.creature_block.name = self.name_edit.text()

    def type_edit_changed(self):
        self.creature_block.type = self.type_edit.text()

    def tag_edit_changed(self):
        self.creature_block.tag = self.tag_edit.text()

    def alignment_edit_changed(self):
        self.creature_block.alignment = self.alignment_edit.text()

    def score_edit_changed(self, score, modifier_label, abilityscore: AbilityScore):
        score = score
        self.creature_block.ability_scores[abilityscore] = score
        update_modifier_label(self.creature_block.ability_scores[abilityscore], modifier_label)

    def hit_points_edit_changed(self):
        con_mod = score_to_mod(self.creature_block.ability_scores[AbilityScore.CONSTITUTION])
        hit_dice = self.max_hit_dice_spinbox.value()

        hit_points_calc = creature_datastructs.MonsterStatblock.\
            calc_monster_hit_points(hit_dice=hit_dice, size=self.creature_block.size, con=con_mod)
        self.creature_block.hitpoints = hit_points_calc
        self.creature_block.hitdice = self.max_hit_dice_spinbox.value()
        self.update_creature_data()

    def hit_dice_edit_changed(self):
        con_mod = score_to_mod(self.creature_block.ability_scores[AbilityScore.CONSTITUTION])
        hit_dice = self.max_hit_dice_spinbox.value()

        hit_points_calc = creature_datastructs.MonsterStatblock.\
            calc_monster_hit_points(hit_dice=hit_dice, size=self.creature_block.size, con=con_mod)
        self.creature_block.hitpoints = hit_points_calc
        self.creature_block.hitdice = self.max_hit_dice_spinbox.value()
        self.update_creature_data()

    def ac_bonus_edit_changed(self):
        self.creature_block.acbonus = self.ac_bonus_spinbox.value()
        self.update_creature_data()

    def armor_type_edit_changed(self):
        self.creature_block.acdesc = self.armor_type_edit.text()
        self.update_creature_data()

    def senses_edit_changed(self):
        self.creature_block.senses = self.senses_edit.text()
        self.update_creature_data()

    def speed_edit_changed(self):
        self.creature_block.speed = self.speeds_edit.text()
        self.update_creature_data()

    def setup_checkbox_signals(self):
        def toggle_container_visibility(checkbox, container):
            checkbox_checked = checkbox.isChecked()
            print(f"Toggling {container} visibility to {checkbox_checked}")
            container.setVisible(True if checkbox_checked else False)
            checkbox.setText("Enabled" if checkbox_checked else "Disabled")

        self.reactions_enable_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(
            self.reactions_enable_checkbox, self.reactions_container))
        self.reactions_container.setVisible(False)

        self.bonus_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(
            self.bonus_actions_enabled_checkbox, self.bonus_actions_container))
        self.bonus_actions_container.setVisible(False)

        self.legendary_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(
            self.legendary_actions_enabled_checkbox, self.legendary_actions_container))
        self.legendary_actions_container.setVisible(False)

        self.mythic_actions_enabled_checkbox.stateChanged.connect(lambda state: toggle_container_visibility(
            self.mythic_actions_enabled_checkbox, self.mythic_actions_container))
        self.mythic_actions_container.setVisible(False)

    def setup_pushbutton_signals(self):
        self.save_button.pressed.connect(self.add_save_proficiency)
        self.skills_button.pressed.connect(self.add_skill_proficiency)
        self.expertise_pushbutton.pressed.connect(self.add_skill_expertise)
        self.condition_button.pressed.connect(self.add_condition_immunity)
        self.damage_vulnerable_button.pressed.connect(self.add_damage_vulnerability)
        self.damage_immune_button.pressed.connect(self.add_damage_immunity)
        self.damage_resistant_button.pressed.connect(self.add_damage_resistance)
        self.add_ability_button.pressed.connect(self.add_ability_dialog)
        self.add_ability_action_button.pressed.connect(self.add_ability_action_dialog)
        self.add_attack_action_button.pressed.connect(self.add_attack_action_dialog)
        self.add_reaction_button.pressed.connect(self.add_reaction_dialog)
        self.add_bonus_action_button.pressed.connect(self.add_bonus_action_dialog)
        self.add_legendary_action_button.pressed.connect(self.add_legendary_action_dialog)
        self.add_mythic_action_button.pressed.connect(self.add_mythic_action_dialog)
        self.gmbinder_convert_button.pressed.connect(self.display_gmbinder_string)
        self.save_monster_button.pressed.connect(self.save_monster_to_json)
        self.load_monster_button.pressed.connect(self.load_monster_from_json)

    def add_save_proficiency(self):
        selected_save = AbilityScore(self.saving_throws_combobox.currentText())
        if selected_save not in self.creature_block.saving_throws:
            self.creature_block.saving_throws.add(selected_save)
        self.update_saves()

    def add_skill_proficiency(self):
        selected_skill = Skill(self.skills_combobox.currentText())
        self.creature_block.add_skill_proficiency(selected_skill)
        self.update_skills()

    def add_skill_expertise(self):
        selected_skill = Skill(self.skills_combobox.currentText())
        self.creature_block.add_skill_expertise(selected_skill)
        self.update_skills()

    def add_condition_immunity(self):
        selected_condition = Condition(self.conditions_combobox.currentText())
        if selected_condition not in self.creature_block.condition_immunities:
            self.creature_block.condition_immunities.add(selected_condition)
        self.update_conditions()

    def add_damage_resistance(self):
        selected_damage = DamageType(self.damage_combobox.currentText())
        self.creature_block.add_damage_modifier(selected_damage, DamageModifier.RESISTANCE)
        self.update_damage()

    def add_damage_immunity(self):
        selected_damage = DamageType(self.damage_combobox.currentText())
        self.creature_block.add_damage_modifier(selected_damage, DamageModifier.IMMUNITY)
        self.update_damage()

    def add_damage_vulnerability(self):
        selected_damage = DamageType(self.damage_combobox.currentText())
        self.creature_block.add_damage_modifier(selected_damage, DamageModifier.VULNERABILITY)
        self.update_damage()

    def add_ability_dialog(self, ability_target: AbilityDescription = None):
        print(QApplication.instance())
        if ability_target is None:
            ability_target = AbilityDescription()
        dialog = AbilityDialog(ability_target, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for ability in self.creature_block.abilities:
                    if dialog.ability.name == ability.name:
                        self.creature_block.abilities.remove(ability)
            else:
                for ability in self.creature_block.abilities:
                    if dialog.ability.name == ability.name:
                        self.creature_block.abilities.remove(ability)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.abilities.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_abilities()
        return

    def add_ability_action_dialog(self, ability_target: AbilityDescription = None):
        print(QApplication.instance())
        if ability_target is None:
            ability_target = AbilityDescription()
        dialog = AbilityDialog(ability_target, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for ability in self.creature_block.actions:
                    if dialog.ability.name == ability.name:
                        self.creature_block.actions.remove(ability)
            else:
                for ability in self.creature_block.actions:
                    if dialog.ability.name == ability.name:
                        self.creature_block.actions.remove(ability)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.actions.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_actions()
        return

    def add_attack_action_dialog(self, attack_target: BaseAttack = None):
        print(QApplication.instance())
        if attack_target is None:
            attack_target = MeleeWeaponAttack()
        dialog = AttackDialog(attack_target, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.attack.name}")
            if dialog.delete_attack:
                for attack in self.creature_block.actions:
                    if dialog.attack.name == attack.name:
                        self.creature_block.actions.remove(attack)
            else:
                for attack in self.creature_block.actions:
                    if dialog.attack.name == attack.name:
                        self.creature_block.actions.remove(attack)

                self.creature_block.actions.append(dialog.attack)
        else:
            print("Not accepted")
        self.update_actions()
        return

    def add_reaction_dialog(self, reaction: AbilityDescription = None):
        print(QApplication.instance())
        if reaction is None:
            reaction = AbilityDescription()
        dialog = AbilityDialog(reaction, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for reaction in self.creature_block.reactions:
                    if dialog.ability.name == reaction.name:
                        self.creature_block.reactions.remove(reaction)
            else:
                for reaction in self.creature_block.reactions:
                    if dialog.ability.name == reaction.name:
                        self.creature_block.reactions.remove(reaction)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.reactions.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_reactions()
        return

    def add_bonus_action_dialog(self, bonus_action: AbilityDescription = None):
        print(QApplication.instance())
        if bonus_action is None:
            bonus_action = AbilityDescription()
        dialog = AbilityDialog(bonus_action, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for bonus_action in self.creature_block.bonusactions:
                    if dialog.ability.name == bonus_action.name:
                        self.creature_block.bonusactions.remove(bonus_action)
            else:
                for bonus_action in self.creature_block.bonusactions:
                    if dialog.ability.name == bonus_action.name:
                        self.creature_block.bonusactions.remove(bonus_action)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.bonusactions.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_bonus_actions()
        return

    def add_legendary_action_dialog(self, legendary_action: AbilityDescription = None):
        print(QApplication.instance())
        if legendary_action is None:
            legendary_action = AbilityDescription()
        dialog = AbilityDialog(legendary_action, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for legendary_action in self.creature_block.legendaryactions:
                    if dialog.ability.name == legendary_action.name:
                        self.creature_block.legendaryactions.remove(legendary_action)
            else:
                for legendary_action in self.creature_block.legendaryactions:
                    if dialog.ability.name == legendary_action.name:
                        self.creature_block.legendaryactions.remove(legendary_action)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.legendaryactions.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_legendary_actions()
        return

    def add_mythic_action_dialog(self, mythic_action: AbilityDescription = None):
        print(QApplication.instance())
        if mythic_action is None:
            mythic_action = AbilityDescription()
        dialog = AbilityDialog(mythic_action, parent=self)
        print("Dialog Created")
        if dialog.exec():
            print(f"{dialog.ability.name} {dialog.ability.description}")
            if dialog.delete_ability:
                for mythic_action in self.creature_block.mythicactions:
                    if dialog.ability.name == mythic_action.name:
                        self.creature_block.mythicactions.remove(mythic_action)
            else:
                for mythic_action in self.creature_block.mythicactions:
                    if dialog.ability.name == mythic_action.name:
                        self.creature_block.mythicactions.remove(mythic_action)

                print(f"{dialog.ability.name} {dialog.ability.description}")
                self.creature_block.mythicactions.append(dialog.ability)
        else:
            print("Not accepted")
        self.update_mythic_actions()
        return

    def display_gmbinder_string(self):
        gmbinder_string = convert_monster(self.creature_block)
        print(gmbinder_string)
        dialog = GMBinderConvertWindow(gmbinder_string, parent=self)
        dialog.exec()

    def save_monster_to_json(self):
        # Open file dialog and get file name
        file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON Files (*.json)")

        if file_name:
            self.creature_block.save_json_to_file(filename=file_name)

    def load_monster_from_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")

        if file_name:
            self.creature_block = creature_datastructs.MonsterStatblock.load_json_from_file(file_name)
            self.update_creature_data()

    def setup_combobox_signals(self):
        def size_combobox_changed():
            print(self.size_combobox.currentText())
            size = Size(self.size_combobox.currentText())
            self.creature_block.size = size
            self.hit_dice_edit_changed()

        def cr_combobox_changed():
            self.creature_block.challengerating = int(self.challenge_rating_combobox.currentText())
            self.update_creature_data()

        self.size_combobox.currentTextChanged.connect(size_combobox_changed)
        self.challenge_rating_combobox.currentTextChanged.connect(cr_combobox_changed)

    def update_saves(self):
        self.save_listwidget.clear()
        for save in self.creature_block.saving_throws:
            self.save_listwidget.addItem(save.value)

    def update_skills(self):
        def insert_skill_row(damagetype, modifier):
            self.skills_tablewidget.insertRow(self.skills_tablewidget.rowCount())
            self.skills_tablewidget.setItem(self.skills_tablewidget.rowCount() - 1, 0, QTableWidgetItem(damagetype))
            self.skills_tablewidget.setItem(self.skills_tablewidget.rowCount() - 1, 1, QTableWidgetItem(modifier))

        self.skills_tablewidget.setRowCount(0)
        for skill in self.creature_block.skills:
            insert_skill_row(skill.value, PROFICIENT)
        for expert in self.creature_block.expertise:
            insert_skill_row(expert.value, EXPERT)

    def update_conditions(self):
        self.condition_listwidget.clear()
        for condition in self.creature_block.condition_immunities:
            self.condition_listwidget.addItem(condition.value)

    def update_damage(self):
        def insert_damage_row(damagetype, modifier):
            self.damage_tablewidget.insertRow(self.damage_tablewidget.rowCount())
            self.damage_tablewidget.setItem(
                self.damage_tablewidget.rowCount() - 1, 0, QTableWidgetItem(damagetype.value))
            self.damage_tablewidget.setItem(
                self.damage_tablewidget.rowCount() - 1, 1, QTableWidgetItem(modifier))

        self.damage_tablewidget.setRowCount(0)
        for damage in self.creature_block.damage_vulnerabilities:
            insert_damage_row(damage, 'vulnerable')
        for damage in self.creature_block.damage_resistances:
            insert_damage_row(damage, 'resistant')
        for damage in self.creature_block.damage_immunities:
            insert_damage_row(damage, 'immune')

    def update_abilities(self):
        for i in reversed(range(self.abilities_list_layout.count())):
            self.abilities_list_layout.itemAt(i).widget().deleteLater()
        for ability in self.creature_block.abilities:
            insert_ability(self.abilities_list_layout, ability)

    def update_actions(self):
        for i in reversed(range(self.actions_list_layout.count())):
            self.actions_list_layout.itemAt(i).widget().deleteLater()
        for action in self.creature_block.actions:
            if isinstance(action, AbilityDescription):
                print("Adding ability action")
                insert_ability(self.actions_list_layout, action)
            elif isinstance(action, BaseAttack):
                print("Adding attack action")
                insert_attack(self.actions_list_layout, action, self.creature_block)
            else:
                print("Invalid action")

    def update_reactions(self):
        for i in reversed(range(self.reactions_list_layout.count())):
            self.reactions_list_layout.itemAt(i).widget().deleteLater()
        for reaction in self.creature_block.reactions:
            insert_ability(self.reactions_list_layout, reaction)

    def update_bonus_actions(self):
        for i in reversed(range(self.bonus_actions_list_layout.count())):
            self.bonus_actions_list_layout.itemAt(i).widget().deleteLater()
        for bonusactions in self.creature_block.bonusactions:
            insert_ability(self.bonus_actions_list_layout, bonusactions)

    def update_legendary_actions(self):
        for i in reversed(range(self.legendary_actions_list_layout.count())):
            self.legendary_actions_list_layout.itemAt(i).widget().deleteLater()
        for legendaryactions in self.creature_block.legendaryactions:
            insert_ability(self.legendary_actions_list_layout, legendaryactions)

    def update_mythic_actions(self):
        for i in reversed(range(self.mythic_actions_list_layout.count())):
            self.mythic_actions_list_layout.itemAt(i).widget().deleteLater()
        for mythicactions in self.creature_block.mythicactions:
            insert_ability(self.mythic_actions_list_layout, mythicactions)

    def update_creature_data(self):
        print(self.creature_block.name)
        self.name_edit.setText(self.creature_block.name)
        set_combo_box_selected_item(self.size_combobox, self.creature_block.size.value)
        self.type_edit.setText(self.creature_block.type)
        self.tag_edit.setText(self.creature_block.tag)
        self.alignment_edit.setText(self.creature_block.alignment)
        set_combo_box_selected_item(self.challenge_rating_combobox, str(self.creature_block.challengerating))
        self.xp_calculation_label.setText(str(
            creature_datastructs.CR_TO_XP_TABLE[self.creature_block.challengerating]))
        self.proficiency_bonus_calculation_label.setText('+' + str(
            proficiency_bonus(self.creature_block.challengerating)))
        self.hit_points_spinbox.setValue(self.creature_block.hitpoints)
        self.max_hit_dice_spinbox.setValue(self.creature_block.hitdice)
        self.hit_die_calculation_label.setText(f"d{Size.hitdice(self.creature_block.size)}")
        self.ac_bonus_spinbox.setValue(self.creature_block.acbonus)
        self.armor_type_edit.setText(self.creature_block.acdesc)
        self.senses_edit.setText(self.creature_block.senses)
        self.speeds_edit.setText(self.creature_block.speed)
        self.str_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.STRENGTH])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.STRENGTH], self.str_mod_label)
        self.dex_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.DEXTERITY])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.DEXTERITY], self.dex_mod_label)
        self.con_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.CONSTITUTION])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.CONSTITUTION], self.con_mod_label)
        self.int_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.INTELLIGENCE])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.INTELLIGENCE], self.int_mod_label)
        self.wis_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.WISDOM])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.WISDOM], self.wis_mod_label)
        self.cha_score_spinbox.setValue(self.creature_block.ability_scores[AbilityScore.CHARISMA])
        update_modifier_label(self.creature_block.ability_scores[AbilityScore.CHARISMA], self.cha_mod_label)
        self.update_saves()
        self.update_skills()
        self.update_conditions()
        self.update_damage()
        self.update_abilities()
        self.update_actions()
        self.update_bonus_actions()
        self.update_reactions()
        self.update_legendary_actions()
        self.mythic_description_edit.setText(self.creature_block.mythicdescription)
        self.update_mythic_actions()


def update_modifier_label(score, label):
    mod = score_to_mod(score)
    modstr = f'+{mod}' if mod >= 0 else f'{mod}'
    label.setText(modstr)


def set_combo_box_selected_item(combo_box, item):
    index = -1
    for i in range(combo_box.count()):
        print(f"{combo_box.itemText(i)} {item}")
        if combo_box.itemText(i) == item:
            index = i
            break

    combo_box.setCurrentIndex(index)
    print(combo_box.currentText())


def update_hitdice(size, modifier_label):
    if isinstance(size, Size):
        modifier_label.setText(str(f"d{Size.hitdice(size)}"))
    else:
        raise TypeError("Tried to enter a non-Size value to calculate hitdice")


def update_prof_bonus(cr, modifier_label):
    modifier_label.setText(f'+{proficiency_bonus(cr)}')


def insert_ability(layout, ability):
    new_ability = AbilityButton(ability)
    layout.addWidget(new_ability)


def insert_attack(layout, attack, creature):
    new_attack = AttackButton(attack, creature)
    print(new_attack.text())
    layout.addWidget(new_attack)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MonsterEditorForm(creature_block=generate_test_monster())
    myWindow.show()
    app.exec()
