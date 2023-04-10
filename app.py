from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from pyqtui.designer_ui.main_window_ui import Ui_MainWindow
from pyqtui.creature_editor_app import MonsterEditorForm
from creatures.creature_generator import generate_test_monster

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class MainWindowApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def file_dialog_clicked(self):
        monster_form = MonsterEditorForm(creature_block=generate_test_monster(), parent=self)
        monster_form.show()


app = QApplication(sys.argv)
myWindow = MainWindowApp(None)
myWindow.show()
app.exec()
