import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from statblockdatastructs import MonsterBlock
import json

from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from PyQt6.uic import loadUi

from main_window import Ui_MainWindow

class MainWindowApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def file_dialog_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")

        if file_name:
            self.load_monster_button.setText(file_name)
            print(file_name)
            json_file = open(file_name, 'r')
            monster = MonsterBlock()
            monster.load_json(json.loads(json_file.read()))


app = QApplication(sys.argv)
myWindow = MainWindowApp(None)
myWindow.show()
app.exec()