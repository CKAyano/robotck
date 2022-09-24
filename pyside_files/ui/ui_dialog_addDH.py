# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_addDH.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTextBrowser,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(862, 416)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_first = QLabel(Dialog)
        self.label_first.setObjectName(u"label_first")
        self.label_first.setMaximumSize(QSize(16777215, 30))
        self.label_first.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_first, 0, 0, 1, 1)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 5, 0, 1, 2)

        self.label_second = QLabel(Dialog)
        self.label_second.setObjectName(u"label_second")
        self.label_second.setMaximumSize(QSize(16777215, 30))
        self.label_second.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_second, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 10, 0, 1, 2)

        self.lineEdit_first = QLineEdit(Dialog)
        self.lineEdit_first.setObjectName(u"lineEdit_first")

        self.gridLayout_2.addWidget(self.lineEdit_first, 0, 1, 1, 1)

        self.lineEdit_fourth = QLineEdit(Dialog)
        self.lineEdit_fourth.setObjectName(u"lineEdit_fourth")

        self.gridLayout_2.addWidget(self.lineEdit_fourth, 3, 1, 1, 1)

        self.lineEdit_second = QLineEdit(Dialog)
        self.lineEdit_second.setObjectName(u"lineEdit_second")

        self.gridLayout_2.addWidget(self.lineEdit_second, 1, 1, 1, 1)

        self.lineEdit_third = QLineEdit(Dialog)
        self.lineEdit_third.setObjectName(u"lineEdit_third")

        self.gridLayout_2.addWidget(self.lineEdit_third, 2, 1, 1, 1)

        self.radioButton_rad = QRadioButton(Dialog)
        self.buttonGroup_angle = QButtonGroup(Dialog)
        self.buttonGroup_angle.setObjectName(u"buttonGroup_angle")
        self.buttonGroup_angle.addButton(self.radioButton_rad)
        self.radioButton_rad.setObjectName(u"radioButton_rad")
        self.radioButton_rad.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_rad, 8, 0, 1, 1)

        self.label_third = QLabel(Dialog)
        self.label_third.setObjectName(u"label_third")
        self.label_third.setMaximumSize(QSize(16777215, 30))
        self.label_third.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_third, 2, 0, 1, 1)

        self.radioButton_deg = QRadioButton(Dialog)
        self.buttonGroup_angle.addButton(self.radioButton_deg)
        self.radioButton_deg.setObjectName(u"radioButton_deg")

        self.gridLayout_2.addWidget(self.radioButton_deg, 8, 1, 1, 1)

        self.label_fourth = QLabel(Dialog)
        self.label_fourth.setObjectName(u"label_fourth")
        self.label_fourth.setMaximumSize(QSize(16777215, 30))
        self.label_fourth.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_fourth, 3, 0, 1, 1)

        self.radioButton_modified = QRadioButton(Dialog)
        self.buttonGroup_dhType = QButtonGroup(Dialog)
        self.buttonGroup_dhType.setObjectName(u"buttonGroup_dhType")
        self.buttonGroup_dhType.addButton(self.radioButton_modified)
        self.radioButton_modified.setObjectName(u"radioButton_modified")

        self.gridLayout_2.addWidget(self.radioButton_modified, 6, 1, 1, 1)

        self.radioButton_standard = QRadioButton(Dialog)
        self.buttonGroup_dhType.addButton(self.radioButton_standard)
        self.radioButton_standard.setObjectName(u"radioButton_standard")
        self.radioButton_standard.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_standard, 6, 0, 1, 1)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 7, 0, 1, 2)

        self.pushButton_addlink = QPushButton(Dialog)
        self.pushButton_addlink.setObjectName(u"pushButton_addlink")

        self.gridLayout_2.addWidget(self.pushButton_addlink, 9, 0, 1, 2)

        self.radioButton_revol = QRadioButton(Dialog)
        self.buttonGroup_is_revol = QButtonGroup(Dialog)
        self.buttonGroup_is_revol.setObjectName(u"buttonGroup_is_revol")
        self.buttonGroup_is_revol.addButton(self.radioButton_revol)
        self.radioButton_revol.setObjectName(u"radioButton_revol")
        self.radioButton_revol.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_revol, 4, 0, 1, 1)

        self.radioButton_prism = QRadioButton(Dialog)
        self.buttonGroup_is_revol.addButton(self.radioButton_prism)
        self.radioButton_prism.setObjectName(u"radioButton_prism")

        self.gridLayout_2.addWidget(self.radioButton_prism, 4, 1, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)

        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 626, 367))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.textBrowser_dh_list = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser_dh_list.setObjectName(u"textBrowser_dh_list")

        self.gridLayout_3.addWidget(self.textBrowser_dh_list, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        QWidget.setTabOrder(self.lineEdit_first, self.lineEdit_second)
        QWidget.setTabOrder(self.lineEdit_second, self.lineEdit_third)
        QWidget.setTabOrder(self.lineEdit_third, self.lineEdit_fourth)
        QWidget.setTabOrder(self.lineEdit_fourth, self.radioButton_revol)
        QWidget.setTabOrder(self.radioButton_revol, self.radioButton_prism)
        QWidget.setTabOrder(self.radioButton_prism, self.radioButton_standard)
        QWidget.setTabOrder(self.radioButton_standard, self.radioButton_modified)
        QWidget.setTabOrder(self.radioButton_modified, self.radioButton_rad)
        QWidget.setTabOrder(self.radioButton_rad, self.radioButton_deg)
        QWidget.setTabOrder(self.radioButton_deg, self.pushButton_addlink)
        QWidget.setTabOrder(self.pushButton_addlink, self.textBrowser_dh_list)
        QWidget.setTabOrder(self.textBrowser_dh_list, self.scrollArea)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u65b0\u589eD-H", None))
        self.label_first.setText(QCoreApplication.translate("Dialog", u"Theta: ", None))
        self.label_second.setText(QCoreApplication.translate("Dialog", u"d: ", None))
        self.radioButton_rad.setText(QCoreApplication.translate("Dialog", u"\u5f33\u5ea6 (rad)", None))
        self.label_third.setText(QCoreApplication.translate("Dialog", u"a: ", None))
        self.radioButton_deg.setText(QCoreApplication.translate("Dialog", u"\u89d2\u5ea6 (deg)", None))
        self.label_fourth.setText(QCoreApplication.translate("Dialog", u"Alpha: ", None))
        self.radioButton_modified.setText(QCoreApplication.translate("Dialog", u"Modified D-H", None))
        self.radioButton_standard.setText(QCoreApplication.translate("Dialog", u"Standard D-H", None))
        self.pushButton_addlink.setText(QCoreApplication.translate("Dialog", u"\u65b0\u589eLink", None))
        self.radioButton_revol.setText(QCoreApplication.translate("Dialog", u"\u65cb\u8f49\u8ef8", None))
        self.radioButton_prism.setText(QCoreApplication.translate("Dialog", u"\u5e73\u79fb\u8ef8", None))
    # retranslateUi

