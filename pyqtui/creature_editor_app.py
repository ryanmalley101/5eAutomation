import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import statblockdatastructs

from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt6.uic import loadUi

from creature_editor_ui import Ui_Form

class CreatureEditorForm(QDialog, Ui_Form):
    def __init__(self, monster_block: statblockdatastructs.MonsterBlock, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name_edit.setText(monster_block.name)
        self.alignmentLineEdit.setText(monster_block.alignment)

    def setup_comboboxes(self):
        # Size combobox
        self.size_combobox.clear()
        for member in statblockdatastructs.Size:
            self.size_comboboxze.addItem(member.value)

        return None
