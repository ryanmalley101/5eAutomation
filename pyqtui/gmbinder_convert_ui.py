# Form implementation generated from reading ui file '.\qtdesignfiles\gmbinder_convert_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GMBinderConversion(object):
    def setupUi(self, GMBinderConversion):
        GMBinderConversion.setObjectName("GMBinderConversion")
        GMBinderConversion.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(GMBinderConversion)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(parent=GMBinderConversion)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gmbinder_string_textbrowser = QtWidgets.QTextBrowser(parent=self.groupBox)
        self.gmbinder_string_textbrowser.setObjectName("gmbinder_string_textbrowser")
        self.gridLayout.addWidget(self.gmbinder_string_textbrowser, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(GMBinderConversion)
        QtCore.QMetaObject.connectSlotsByName(GMBinderConversion)

    def retranslateUi(self, GMBinderConversion):
        _translate = QtCore.QCoreApplication.translate
        GMBinderConversion.setWindowTitle(_translate("GMBinderConversion", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GMBinderConversion = QtWidgets.QWidget()
    ui = Ui_GMBinderConversion()
    ui.setupUi(GMBinderConversion)
    GMBinderConversion.show()
    sys.exit(app.exec())
