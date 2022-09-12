# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(887, 852)
        self.action_refresh = QAction(MainWindow)
        self.action_refresh.setObjectName(u"action_refresh")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_centralwidget = QVBoxLayout(self.centralwidget)
        self.verticalLayout_centralwidget.setObjectName(u"verticalLayout_centralwidget")
        self.verticalLayout_main = QVBoxLayout()
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.groupBox_dhsetting = QGroupBox(self.centralwidget)
        self.groupBox_dhsetting.setObjectName(u"groupBox_dhsetting")
        self.horizontalLayout_dhsetting = QHBoxLayout(self.groupBox_dhsetting)
        self.horizontalLayout_dhsetting.setObjectName(u"horizontalLayout_dhsetting")
        self.horizontalLayout_dhsetting.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.comboBox_dh = QComboBox(self.groupBox_dhsetting)
        self.comboBox_dh.addItem("")
        self.comboBox_dh.setObjectName(u"comboBox_dh")

        self.horizontalLayout_dhsetting.addWidget(self.comboBox_dh)

        self.pushButton_newDH = QPushButton(self.groupBox_dhsetting)
        self.pushButton_newDH.setObjectName(u"pushButton_newDH")

        self.horizontalLayout_dhsetting.addWidget(self.pushButton_newDH)

        self.label_info = QLabel(self.groupBox_dhsetting)
        self.label_info.setObjectName(u"label_info")

        self.horizontalLayout_dhsetting.addWidget(self.label_info)

        self.horizontalLayout_dhsetting.setStretch(0, 3)
        self.horizontalLayout_dhsetting.setStretch(1, 1)
        self.horizontalLayout_dhsetting.setStretch(2, 8)

        self.verticalLayout_main.addWidget(self.groupBox_dhsetting)

        self.tabWidget_main = QTabWidget(self.centralwidget)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tab_fk = QWidget()
        self.tab_fk.setObjectName(u"tab_fk")
        self.verticalLayout_tab_fk = QVBoxLayout(self.tab_fk)
        self.verticalLayout_tab_fk.setObjectName(u"verticalLayout_tab_fk")
        self.groupBox_fk_input = QGroupBox(self.tab_fk)
        self.groupBox_fk_input.setObjectName(u"groupBox_fk_input")
        self.horizontalLayout_fk_input = QHBoxLayout(self.groupBox_fk_input)
        self.horizontalLayout_fk_input.setObjectName(u"horizontalLayout_fk_input")
        self.label_fk_angle = QLabel(self.groupBox_fk_input)
        self.label_fk_angle.setObjectName(u"label_fk_angle")
        self.label_fk_angle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_fk_input.addWidget(self.label_fk_angle)

        self.doubleSpinBox_fk_j1 = QDoubleSpinBox(self.groupBox_fk_input)
        self.doubleSpinBox_fk_j1.setObjectName(u"doubleSpinBox_fk_j1")
        self.doubleSpinBox_fk_j1.setDecimals(6)

        self.horizontalLayout_fk_input.addWidget(self.doubleSpinBox_fk_j1)

        self.doubleSpinBox_fk_j2 = QDoubleSpinBox(self.groupBox_fk_input)
        self.doubleSpinBox_fk_j2.setObjectName(u"doubleSpinBox_fk_j2")
        self.doubleSpinBox_fk_j2.setDecimals(6)

        self.horizontalLayout_fk_input.addWidget(self.doubleSpinBox_fk_j2)

        self.radioButton_fk_rad = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_rad.setObjectName(u"radioButton_fk_rad")
        self.radioButton_fk_rad.setChecked(True)

        self.horizontalLayout_fk_input.addWidget(self.radioButton_fk_rad)

        self.radioButton_fk_deg = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_deg.setObjectName(u"radioButton_fk_deg")
        self.radioButton_fk_deg.setChecked(False)

        self.horizontalLayout_fk_input.addWidget(self.radioButton_fk_deg)


        self.verticalLayout_tab_fk.addWidget(self.groupBox_fk_input)

        self.groupBox_fk_ouput = QGroupBox(self.tab_fk)
        self.groupBox_fk_ouput.setObjectName(u"groupBox_fk_ouput")
        self.gridLayout_fk_output = QGridLayout(self.groupBox_fk_ouput)
        self.gridLayout_fk_output.setObjectName(u"gridLayout_fk_output")
        self.checkBox_fk_round = QCheckBox(self.groupBox_fk_ouput)
        self.checkBox_fk_round.setObjectName(u"checkBox_fk_round")

        self.gridLayout_fk_output.addWidget(self.checkBox_fk_round, 1, 0, 1, 1)

        self.textBrowser_fk_result = QTextBrowser(self.groupBox_fk_ouput)
        self.textBrowser_fk_result.setObjectName(u"textBrowser_fk_result")

        self.gridLayout_fk_output.addWidget(self.textBrowser_fk_result, 0, 5, 10, 1)

        self.comboBox_fk_result = QComboBox(self.groupBox_fk_ouput)
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.setObjectName(u"comboBox_fk_result")

        self.gridLayout_fk_output.addWidget(self.comboBox_fk_result, 2, 0, 1, 4)

        self.label_fk_joint = QLabel(self.groupBox_fk_ouput)
        self.label_fk_joint.setObjectName(u"label_fk_joint")
        self.label_fk_joint.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_fk_output.addWidget(self.label_fk_joint, 0, 0, 1, 1)

        self.pushButton_fk_result = QPushButton(self.groupBox_fk_ouput)
        self.pushButton_fk_result.setObjectName(u"pushButton_fk_result")

        self.gridLayout_fk_output.addWidget(self.pushButton_fk_result, 2, 4, 1, 1)

        self.spinBox_fk_numjoint = QSpinBox(self.groupBox_fk_ouput)
        self.spinBox_fk_numjoint.setObjectName(u"spinBox_fk_numjoint")

        self.gridLayout_fk_output.addWidget(self.spinBox_fk_numjoint, 0, 3, 1, 2)

        self.spinBox_fk_round = QSpinBox(self.groupBox_fk_ouput)
        self.spinBox_fk_round.setObjectName(u"spinBox_fk_round")

        self.gridLayout_fk_output.addWidget(self.spinBox_fk_round, 1, 3, 1, 2)


        self.verticalLayout_tab_fk.addWidget(self.groupBox_fk_ouput)

        self.verticalLayout_tab_fk.setStretch(0, 1)
        self.verticalLayout_tab_fk.setStretch(1, 10)
        self.tabWidget_main.addTab(self.tab_fk, "")
        self.tab_ik = QWidget()
        self.tab_ik.setObjectName(u"tab_ik")
        self.tabWidget_main.addTab(self.tab_ik, "")
        self.tab_plot = QWidget()
        self.tab_plot.setObjectName(u"tab_plot")
        self.tabWidget_main.addTab(self.tab_plot, "")

        self.verticalLayout_main.addWidget(self.tabWidget_main)

        self.verticalLayout_main.setStretch(0, 1)
        self.verticalLayout_main.setStretch(1, 10)

        self.verticalLayout_centralwidget.addLayout(self.verticalLayout_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 887, 21))
        self.menu_setting = QMenu(self.menuBar)
        self.menu_setting.setObjectName(u"menu_setting")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu_setting.menuAction())
        self.menu_setting.addAction(self.action_refresh)

        self.retranslateUi(MainWindow)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Robot CK GUI", None))
        self.action_refresh.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u6574\u7406", None))
        self.groupBox_dhsetting.setTitle(QCoreApplication.translate("MainWindow", u"D-H Settings", None))
        self.comboBox_dh.setItemText(0, QCoreApplication.translate("MainWindow", u"< \u8acb\u9078\u64c7 D-H >", None))

        self.pushButton_newDH.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u589e D-H", None))
        self.label_info.setText(QCoreApplication.translate("MainWindow", u"\u8acb\u9078\u64c7\u6a5f\u68b0\u624b\u81c2D-H", None))
        self.groupBox_fk_input.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u5165", None))
        self.label_fk_angle.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u5ea6\uff1a", None))
        self.radioButton_fk_rad.setText(QCoreApplication.translate("MainWindow", u"\u5f33\u5ea6 (rad)", None))
        self.radioButton_fk_deg.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u5ea6 (deg)", None))
        self.groupBox_fk_ouput.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u51fa", None))
        self.checkBox_fk_round.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u6578\u9ede\u4f4d\u6578", None))
        self.comboBox_fk_result.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5ea7\u6a19", None))
        self.comboBox_fk_result.setItemText(1, QCoreApplication.translate("MainWindow", u"zyx\u6b50\u62c9\u89d2", None))
        self.comboBox_fk_result.setItemText(2, QCoreApplication.translate("MainWindow", u"\u65cb\u8f49\u77e9\u9663", None))
        self.comboBox_fk_result.setItemText(3, QCoreApplication.translate("MainWindow", u"\u9f4a\u6b21\u77e9\u9663", None))
        self.comboBox_fk_result.setItemText(4, QCoreApplication.translate("MainWindow", u"json", None))
        self.comboBox_fk_result.setItemText(5, QCoreApplication.translate("MainWindow", u"yaml", None))

        self.label_fk_joint.setText(QCoreApplication.translate("MainWindow", u"\u8ef8\uff1a", None))
        self.pushButton_fk_result.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u7b97\u7d50\u679c", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_fk), QCoreApplication.translate("MainWindow", u"Forward Kinematics", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_ik), QCoreApplication.translate("MainWindow", u"Inverse Kinematics", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_plot), QCoreApplication.translate("MainWindow", u"Plot Robot", None))
        self.menu_setting.setTitle(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
    # retranslateUi

