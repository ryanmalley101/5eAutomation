import os
import sys
from pathlib import Path
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import statblockdatastructs

from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QLabel, QLineEdit, QListView, QSizePolicy, QComboBox, QPushButton, QCheckBox, QTextEdit
)
from PyQt6 import QtCore

from creature_editor_ui import Ui_Form

CURRENT_DIRECTORY = Path(__file__).resolve().parent

class CreatureEditorForm(QDialog, Ui_Form):
    def __init__(self, monster_block: statblockdatastructs.MonsterBlock, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        QtCore.QDir.addSearchPath('images', os.fspath(CURRENT_DIRECTORY / "images"))
        self.setup_comboboxes()
        self.name_edit.setText(monster_block.name)
        self.alignment_edit.setText(monster_block.alignment)
        self.set_stylesheet()
        self.setup_checkbox_signals()

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
                widget.setStyleSheet(f'#{widget.objectName()}{{background-image: none; background-color: white; font: 12pt "Cambria";}}')
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
        for size in statblockdatastructs.Size:
            self.size_combobox.addItem(size.name)
        for cr in statblockdatastructs.CR_TO_XP_TABLE:
            self.challenge_rating_combobox.addItem(f"{cr} ({statblockdatastructs.CR_TO_XP_TABLE[cr]} xp)")
        for save in statblockdatastructs.AbilityScores:
            self.saving_throws_combobox.addItem(save.name)
        for skill in statblockdatastructs.SKILL_LIST:
            self.skills_combobox.addItem(skill)
        for condition in statblockdatastructs.CONDITION_LIST:
            self.conditions_combobox.addItem(condition)
        for damage in statblockdatastructs.DAMAGE_LIST:
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = CreatureEditorForm(monster_block=statblockdatastructs.MonsterBlock(), parent=None)
    myWindow.show()
    app.exec()