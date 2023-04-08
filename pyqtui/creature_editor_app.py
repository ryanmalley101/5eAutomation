import os
import sys
from pathlib import Path
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from creatures import creature_datastructs
from srd.srd_datastructs import AbilityScores, SKILL_LIST, CONDITION_LIST, DAMAGE_LIST, proficiency_bonus

from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QListView, QSizePolicy, QComboBox, QPushButton, QCheckBox, QTextEdit
)

from PyQt6.QtGui import QStandardItemModel, QStandardItem

from PyQt6 import QtCore

from creature_editor_ui import Ui_Form
from creatures.creature_generator import generate_test_creature

CURRENT_DIRECTORY = Path(__file__).resolve().parent

class CreatureEditorForm(QDialog, Ui_Form):
    def __init__(self, creature_block: creature_datastructs.CreatureStatblock, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        QtCore.QDir.addSearchPath('images', os.fspath(CURRENT_DIRECTORY / "images"))

        # Set up the list models for the various QListViews
        self.save_list_model = QStandardItemModel()
        self.skills_list_model = QStandardItemModel()
        self.condition_list_model = QStandardItemModel()
        self.damage_list_model = QStandardItemModel()
        self.abilities_list_model = QStandardItemModel()
        self.actions_list_model = QStandardItemModel()
        self.reactions_list_model = QStandardItemModel()
        self.bonus_actions_list_model = QStandardItemModel()
        self.legendary_actions_list_model = QStandardItemModel()
        self.mythic_actions_list_model = QStandardItemModel()

        self.setup_comboboxes()
        self.set_stylesheet()
        self.setup_checkbox_signals()
        self.init_creature_data(creature_block)

    def set_stylesheet(self):
        # Sets the stylesheet for derived elements like hit die size and prof bonus
        def set_derived_styles():
            derived_stylesheet = 'background-color: rgb(125, 132, 145); font: 16pt "Cambria";'
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
            print(widget)
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

        set_derived_styles()
        return None


    def setup_comboboxes(self):
        # Size combobox
        self.size_combobox.clear()
        for size in creature_datastructs.Size:
            self.size_combobox.addItem(size.name)
        for cr in creature_datastructs.CR_TO_XP_TABLE:
            self.challenge_rating_combobox.addItem(str(cr))
        for save in creature_datastructs.AbilityScores:
            self.saving_throws_combobox.addItem(save.name)
        for skill in SKILL_LIST:
            self.skills_combobox.addItem(skill)
        for condition in CONDITION_LIST:
            self.conditions_combobox.addItem(condition)
        for damage in DAMAGE_LIST:
            self.damage_combobox.addItem(damage)
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


    def init_creature_data(self, creature):
        def initsaves():
            # if creature.strsave: self.save_listview
            if creature.dexsave: self.save_list_model.appendRow(QStandardItem(AbilityScores.DEXTERITY.value))
            if creature.consave: self.save_list_model.appendRow(QStandardItem(AbilityScores.CONSTITUTION.value))
            if creature.intsave: self.save_list_model.appendRow(QStandardItem(AbilityScores.INTELLIGENCE.value))
            if creature.wissave: self.save_list_model.appendRow(QStandardItem(AbilityScores.WISDOM.value))
            if creature.chasave: self.save_list_model.appendRow(QStandardItem(AbilityScores.CHARISMA.value))


        print(creature.name)
        self.name_edit.setText(creature.name)
        self.size_combobox.setCurrentIndex(self.size_combobox.findData(creature.size.value))
        self.type_edit.setText(creature.type)
        self.tag_edit.setText(creature.tag)
        self.alignment_edit.setText(creature.alignment)
        set_combo_box_selected_item(self.challenge_rating_combobox, str(creature.challengerating))
        self.proficiency_bonus_calculation_label.setText(str(proficiency_bonus(creature.challengerating)))
        self.challenge_rating_combobox.setCurrentIndex(self.challenge_rating_combobox.findData(creature.challengerating))
        self.xp_calculation_label.setText(str(
            creature_datastructs.CR_TO_XP_TABLE[creature.challengerating]))
        self.proficiency_bonus_calculation_label.setText(str(
            creature_datastructs.proficiency_bonus(creature.challengerating)))
        self.hit_points_edit.setText(str(creature.hitpoints))
        self.max_hit_dice_edit.setText(creature.hitdice)
        self.hit_die_calculation_label.setText(f"d{creature_datastructs.Size.hitdice(creature.size)}")
        self.ac_bonus_edit.setText(str(creature.acbonus))
        self.armor_type_edit.setText(creature.acdesc)
        self.senses_edit.setText(creature.senses)
        self.speeds_edit.setText(creature.speed)
        self.str_edit.setText(str(creature.ability_scores[AbilityScores.STRENGTH]))
        self.dex_edit.setText(str(creature.ability_scores[AbilityScores.DEXTERITY]))
        self.con_edit.setText(str(creature.ability_scores[AbilityScores.CONSTITUTION]))
        self.int_edit.setText(str(creature.ability_scores[AbilityScores.INTELLIGENCE]))
        self.wis_edit.setText(str(creature.ability_scores[AbilityScores.WISDOM]))
        self.cha_edit.setText(str(creature.ability_scores[AbilityScores.CHARISMA]))
        initsaves()


def set_combo_box_selected_item(combo_box, item):
    index = -1
    for i in range(combo_box.count()):
        if combo_box.itemText(i) == item:
            index = i
            break

    combo_box.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = CreatureEditorForm(creature_block=generate_test_creature(), parent=None)
    myWindow.show()
    app.exec()