# Form implementation generated from reading ui file '.\qtdesignfiles\attack_dialogue_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AttackDialogue(object):
    def setupUi(self, AttackDialogue):
        AttackDialogue.setObjectName("AttackDialogue")
        AttackDialogue.resize(590, 550)
        self.gridLayout_2 = QtWidgets.QGridLayout(AttackDialogue)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(parent=AttackDialogue)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.attack_name_label = QtWidgets.QLabel(parent=self.groupBox)
        self.attack_name_label.setObjectName("attack_name_label")
        self.verticalLayout_10.addWidget(self.attack_name_label)
        self.attack_name_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.attack_name_edit.setObjectName("attack_name_edit")
        self.verticalLayout_10.addWidget(self.attack_name_edit)
        self.verticalLayout_12.addLayout(self.verticalLayout_10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.attack_type_label = QtWidgets.QLabel(parent=self.groupBox)
        self.attack_type_label.setObjectName("attack_type_label")
        self.verticalLayout_8.addWidget(self.attack_type_label)
        self.attack_type_combobox = QtWidgets.QComboBox(parent=self.groupBox)
        self.attack_type_combobox.setObjectName("attack_type_combobox")
        self.verticalLayout_8.addWidget(self.attack_type_combobox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.attack_modifier_label = QtWidgets.QLabel(parent=self.groupBox)
        self.attack_modifier_label.setObjectName("attack_modifier_label")
        self.verticalLayout_7.addWidget(self.attack_modifier_label)
        self.attack_modifier_combobox = QtWidgets.QComboBox(parent=self.groupBox)
        self.attack_modifier_combobox.setObjectName("attack_modifier_combobox")
        self.verticalLayout_7.addWidget(self.attack_modifier_combobox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.attack_bonus_label = QtWidgets.QLabel(parent=self.groupBox)
        self.attack_bonus_label.setObjectName("attack_bonus_label")
        self.verticalLayout_9.addWidget(self.attack_bonus_label)
        self.attack_bonus_spinbox = QtWidgets.QSpinBox(parent=self.groupBox)
        self.attack_bonus_spinbox.setObjectName("attack_bonus_spinbox")
        self.verticalLayout_9.addWidget(self.attack_bonus_spinbox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        self.verticalLayout_12.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.damage_dice_label = QtWidgets.QLabel(parent=self.groupBox)
        self.damage_dice_label.setObjectName("damage_dice_label")
        self.verticalLayout_5.addWidget(self.damage_dice_label)
        self.damage_dice_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.damage_dice_edit.setObjectName("damage_dice_edit")
        self.verticalLayout_5.addWidget(self.damage_dice_edit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.targets_label = QtWidgets.QLabel(parent=self.groupBox)
        self.targets_label.setObjectName("targets_label")
        self.verticalLayout_6.addWidget(self.targets_label)
        self.targets_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.targets_edit.setObjectName("targets_edit")
        self.verticalLayout_6.addWidget(self.targets_edit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_12.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.reach_label = QtWidgets.QLabel(parent=self.groupBox)
        self.reach_label.setObjectName("reach_label")
        self.verticalLayout_4.addWidget(self.reach_label)
        self.reach_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.reach_edit.setText("")
        self.reach_edit.setObjectName("reach_edit")
        self.verticalLayout_4.addWidget(self.reach_edit)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.range_edit = QtWidgets.QLabel(parent=self.groupBox)
        self.range_edit.setObjectName("range_edit")
        self.verticalLayout_3.addWidget(self.range_edit)
        self.range_edit_2 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.range_edit_2.setText("")
        self.range_edit_2.setObjectName("range_edit_2")
        self.verticalLayout_3.addWidget(self.range_edit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.short_range_label = QtWidgets.QLabel(parent=self.groupBox)
        self.short_range_label.setObjectName("short_range_label")
        self.verticalLayout_2.addWidget(self.short_range_label)
        self.short_range_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.short_range_edit.setText("")
        self.short_range_edit.setObjectName("short_range_edit")
        self.verticalLayout_2.addWidget(self.short_range_edit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.long_range_label = QtWidgets.QLabel(parent=self.groupBox)
        self.long_range_label.setObjectName("long_range_label")
        self.verticalLayout.addWidget(self.long_range_label)
        self.long_range_edit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.long_range_edit.setText("")
        self.long_range_edit.setObjectName("long_range_edit")
        self.verticalLayout.addWidget(self.long_range_edit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_12.addLayout(self.horizontalLayout)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.attack_description_label = QtWidgets.QLabel(parent=self.groupBox)
        self.attack_description_label.setObjectName("attack_description_label")
        self.verticalLayout_11.addWidget(self.attack_description_label)
        self.attack_description_edit = QtWidgets.QTextEdit(parent=self.groupBox)
        self.attack_description_edit.setObjectName("attack_description_edit")
        self.verticalLayout_11.addWidget(self.attack_description_edit)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.apply_attack_pushbutton = QtWidgets.QPushButton(parent=self.groupBox)
        self.apply_attack_pushbutton.setObjectName("apply_attack_pushbutton")
        self.horizontalLayout_4.addWidget(self.apply_attack_pushbutton)
        self.delete_attack_pushbutton = QtWidgets.QPushButton(parent=self.groupBox)
        self.delete_attack_pushbutton.setObjectName("delete_attack_pushbutton")
        self.horizontalLayout_4.addWidget(self.delete_attack_pushbutton)
        self.cancel_attack_pushbutton = QtWidgets.QPushButton(parent=self.groupBox)
        self.cancel_attack_pushbutton.setObjectName("cancel_attack_pushbutton")
        self.horizontalLayout_4.addWidget(self.cancel_attack_pushbutton)
        self.verticalLayout_12.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_12, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(AttackDialogue)
        QtCore.QMetaObject.connectSlotsByName(AttackDialogue)

    def retranslateUi(self, AttackDialogue):
        _translate = QtCore.QCoreApplication.translate
        AttackDialogue.setWindowTitle(_translate("AttackDialogue", "Dialog"))
        self.attack_name_label.setText(_translate("AttackDialogue", "Attack Name"))
        self.attack_type_label.setText(_translate("AttackDialogue", "Attack Type"))
        self.attack_modifier_label.setText(_translate("AttackDialogue", "Attack Modifier"))
        self.attack_bonus_label.setText(_translate("AttackDialogue", "Attack Bonus"))
        self.damage_dice_label.setText(_translate("AttackDialogue", "Damage Dice (eg. 1d8+2d4+M)"))
        self.targets_label.setText(_translate("AttackDialogue", "Targets"))
        self.targets_edit.setText(_translate("AttackDialogue", "one target."))
        self.reach_label.setText(_translate("AttackDialogue", "Reach"))
        self.range_edit.setText(_translate("AttackDialogue", "Range"))
        self.short_range_label.setText(_translate("AttackDialogue", "Short Range"))
        self.long_range_label.setText(_translate("AttackDialogue", "Long Range"))
        self.attack_description_label.setText(_translate("AttackDialogue", "Attack Description"))
        self.apply_attack_pushbutton.setText(_translate("AttackDialogue", "Apply"))
        self.delete_attack_pushbutton.setText(_translate("AttackDialogue", "Delete"))
        self.cancel_attack_pushbutton.setText(_translate("AttackDialogue", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttackDialogue = QtWidgets.QDialog()
    ui = Ui_AttackDialogue()
    ui.setupUi(AttackDialogue)
    AttackDialogue.show()
    sys.exit(app.exec())
