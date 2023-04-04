# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_traj.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(912, 441)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_type = QGridLayout()
        self.gridLayout_type.setObjectName(u"gridLayout_type")
        self.radioButton_objective_cartesian = QRadioButton(Dialog)
        self.buttonGroup = QButtonGroup(Dialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_objective_cartesian)
        self.radioButton_objective_cartesian.setObjectName(u"radioButton_objective_cartesian")
        self.radioButton_objective_cartesian.setChecked(True)

        self.gridLayout_type.addWidget(self.radioButton_objective_cartesian, 0, 0, 1, 1)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_type.addWidget(self.line_2, 3, 0, 1, 2)

        self.radioButton_objective_joint = QRadioButton(Dialog)
        self.buttonGroup.addButton(self.radioButton_objective_joint)
        self.radioButton_objective_joint.setObjectName(u"radioButton_objective_joint")

        self.gridLayout_type.addWidget(self.radioButton_objective_joint, 0, 1, 1, 1)

        self.radioButton_rad = QRadioButton(Dialog)
        self.buttonGroup_2 = QButtonGroup(Dialog)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_rad)
        self.radioButton_rad.setObjectName(u"radioButton_rad")
        self.radioButton_rad.setChecked(True)

        self.gridLayout_type.addWidget(self.radioButton_rad, 2, 0, 1, 1)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_type.addWidget(self.line, 1, 0, 1, 2)

        self.radioButton_deg = QRadioButton(Dialog)
        self.buttonGroup_2.addButton(self.radioButton_deg)
        self.radioButton_deg.setObjectName(u"radioButton_deg")

        self.gridLayout_type.addWidget(self.radioButton_deg, 2, 1, 1, 1)

        self.verticalLayout_input_label = QVBoxLayout()
        self.verticalLayout_input_label.setObjectName(u"verticalLayout_input_label")
        self.label_x = QLabel(Dialog)
        self.label_x.setObjectName(u"label_x")
        self.label_x.setMaximumSize(QSize(16777215, 20))
        self.label_x.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_input_label.addWidget(self.label_x)

        self.label_y = QLabel(Dialog)
        self.label_y.setObjectName(u"label_y")
        self.label_y.setMaximumSize(QSize(16777215, 20))
        self.label_y.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_input_label.addWidget(self.label_y)

        self.label_z = QLabel(Dialog)
        self.label_z.setObjectName(u"label_z")
        self.label_z.setMaximumSize(QSize(16777215, 20))
        self.label_z.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_input_label.addWidget(self.label_z)


        self.gridLayout_type.addLayout(self.verticalLayout_input_label, 4, 0, 1, 1)

        self.verticalLayout_input_value = QVBoxLayout()
        self.verticalLayout_input_value.setObjectName(u"verticalLayout_input_value")
        self.lineEdit_2 = QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_input_value.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(Dialog)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_input_value.addWidget(self.lineEdit_3)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_input_value.addWidget(self.lineEdit)


        self.gridLayout_type.addLayout(self.verticalLayout_input_value, 4, 1, 1, 1)

        self.pushButton_add = QPushButton(Dialog)
        self.pushButton_add.setObjectName(u"pushButton_add")

        self.gridLayout_type.addWidget(self.pushButton_add, 5, 0, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout_type)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 647, 390))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u65b0\u589e\u898f\u5283\u9ede", None))
        self.radioButton_objective_cartesian.setText(QCoreApplication.translate("Dialog", u"Cartesian space", None))
        self.radioButton_objective_joint.setText(QCoreApplication.translate("Dialog", u"joint space", None))
        self.radioButton_rad.setText(QCoreApplication.translate("Dialog", u"\u5f33\u5ea6 (rad)", None))
        self.radioButton_deg.setText(QCoreApplication.translate("Dialog", u"\u89d2\u5ea6 (deg)", None))
        self.label_x.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.label_y.setText(QCoreApplication.translate("Dialog", u"Y", None))
        self.label_z.setText(QCoreApplication.translate("Dialog", u"Z", None))
        self.pushButton_add.setText(QCoreApplication.translate("Dialog", u"\u65b0\u589e", None))
    # retranslateUi

