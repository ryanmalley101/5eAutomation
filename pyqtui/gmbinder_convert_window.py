from PyQt6.QtWidgets import QDialog
from pyqtui.designer_ui.gmbinder_convert_ui import Ui_GMBinderBrowser


class GMBinderConvertWindow(QDialog, Ui_GMBinderBrowser):
    def __init__(self, gmbinder_string: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.gmbinder_string_textbrowser.setPlainText(gmbinder_string)
