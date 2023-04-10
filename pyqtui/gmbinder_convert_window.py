from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QWidget
from pyqtui.gmbinder_convert_ui import Ui_GMBinderConversion
from srd.srd_datastructs import AbilityDescription

class GMBinderConvertWindow(QWidget, Ui_GMBinderConversion):
    def __init__(self, gmbinder_string:str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.gmbinder_string_textbrowser.setPlainText(gmbinder_string)

