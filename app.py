from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, \
    QComboBox, QSpinBox, QListWidget
from pyqtui.designer_ui.main_window_ui import Ui_MainWindow
from pyqtui.creature_editor_app import MonsterEditorForm
from pyqtui.style.stylesheets import *
from creatures.creature_generator import generate_test_monster
from PyQt6 import QtCore
from open5e.Open5eAPI import fetch_srd_monster_names, fetch_srd_monster

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
CURRENT_DIRECTORY = Path(__file__).resolve().parent


class MainWindowApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        QtCore.QDir.addSearchPath('images', os.fspath(CURRENT_DIRECTORY / "pyqtui/images"))
        self.setupUi(self)
        self.creature_names = []
        for name in fetch_srd_monster_names():
            self.creature_names.append(name)
            self.creature_combobox.addItem(name)
        self.creature_filter_lineedit.textChanged.connect(self.filter_monsters)
        self.load_monster_button.clicked.connect(self.monster_editor_button_clicked)
        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet('QWidget{font: 12pt "Cambria"}')
        self.centralwidget.setStyleSheet(f'#{self.centralwidget.objectName()}{papyrus_background_stylesheet}')
        for widget in self.centralwidget.findChildren((QLabel, QListWidget, QLineEdit, QComboBox,
                                                  QPushButton, QCheckBox, QTextEdit, QComboBox, QSpinBox)):
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f'#{widget.objectName()}{label_stylesheet}')
            elif isinstance(widget, QListWidget) or isinstance(widget, QTextEdit):
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

    def monster_editor_button_clicked(self):
        if self.creature_combobox.currentText() != "":
            print(fetch_srd_monster(self.creature_combobox.currentText().lower()))
            monster_form = MonsterEditorForm(creature_block=fetch_srd_monster(self.creature_combobox.currentText().lower()), parent=self)
            monster_form.show()
        else:
            monster_form = MonsterEditorForm(creature_block=generate_test_monster(), parent=self)
            monster_form.show()


    def filter_monsters(self, search_term):
        # Filter the monster names based on the search term
        filtered_monsters = [name for name in self.creature_names if search_term.lower() in name.lower()]

        # Update the list view with the filtered monster names
        self.creature_combobox.clear()
        self.creature_combobox.addItems(filtered_monsters)

app = QApplication(sys.argv)
myWindow = MainWindowApp(None)
myWindow.show()
app.exec()
