# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

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
        self.horizontalLayout_fk_input_radioButton = QHBoxLayout()
        self.horizontalLayout_fk_input_radioButton.setObjectName(u"horizontalLayout_fk_input_radioButton")
        self.radioButton_fk_rad = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_rad.setObjectName(u"radioButton_fk_rad")
        self.radioButton_fk_rad.setChecked(True)

        self.horizontalLayout_fk_input_radioButton.addWidget(self.radioButton_fk_rad)

        self.radioButton_fk_deg = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_deg.setObjectName(u"radioButton_fk_deg")
        self.radioButton_fk_deg.setChecked(False)

        self.horizontalLayout_fk_input_radioButton.addWidget(self.radioButton_fk_deg)


        self.horizontalLayout_fk_input.addLayout(self.horizontalLayout_fk_input_radioButton)

        self.horizontalLayout_fk_input_doubleSpinBox = QHBoxLayout()
        self.horizontalLayout_fk_input_doubleSpinBox.setObjectName(u"horizontalLayout_fk_input_doubleSpinBox")
        self.label_fk_angle = QLabel(self.groupBox_fk_input)
        self.label_fk_angle.setObjectName(u"label_fk_angle")
        self.label_fk_angle.setMaximumSize(QSize(40, 16777215))
        self.label_fk_angle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_fk_input_doubleSpinBox.addWidget(self.label_fk_angle)

        self.doubleSpinBox_fk_j1 = QDoubleSpinBox(self.groupBox_fk_input)
        self.doubleSpinBox_fk_j1.setObjectName(u"doubleSpinBox_fk_j1")
        self.doubleSpinBox_fk_j1.setEnabled(False)
        self.doubleSpinBox_fk_j1.setDecimals(6)
        self.doubleSpinBox_fk_j1.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_fk_j1.setMaximum(1000.000000000000000)

        self.horizontalLayout_fk_input_doubleSpinBox.addWidget(self.doubleSpinBox_fk_j1)

        self.doubleSpinBox_fk_j2 = QDoubleSpinBox(self.groupBox_fk_input)
        self.doubleSpinBox_fk_j2.setObjectName(u"doubleSpinBox_fk_j2")
        self.doubleSpinBox_fk_j2.setEnabled(False)
        self.doubleSpinBox_fk_j2.setDecimals(6)
        self.doubleSpinBox_fk_j2.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_fk_j2.setMaximum(1000.000000000000000)

        self.horizontalLayout_fk_input_doubleSpinBox.addWidget(self.doubleSpinBox_fk_j2)


        self.horizontalLayout_fk_input.addLayout(self.horizontalLayout_fk_input_doubleSpinBox)

        self.horizontalLayout_fk_input.setStretch(0, 1)
        self.horizontalLayout_fk_input.setStretch(1, 4)

        self.verticalLayout_tab_fk.addWidget(self.groupBox_fk_input)

        self.groupBox_fk_ouput = QGroupBox(self.tab_fk)
        self.groupBox_fk_ouput.setObjectName(u"groupBox_fk_ouput")
        self.gridLayout_3 = QGridLayout(self.groupBox_fk_ouput)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_fk_output_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_fk_output_1, 0, 2, 1, 1)

        self.label_fk_joint = QLabel(self.groupBox_fk_ouput)
        self.label_fk_joint.setObjectName(u"label_fk_joint")
        self.label_fk_joint.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_fk_joint, 0, 0, 1, 1)

        self.spinBox_fk_numjoint = QSpinBox(self.groupBox_fk_ouput)
        self.spinBox_fk_numjoint.setObjectName(u"spinBox_fk_numjoint")

        self.gridLayout_3.addWidget(self.spinBox_fk_numjoint, 0, 1, 1, 1)

        self.checkBox_fk_round = QCheckBox(self.groupBox_fk_ouput)
        self.checkBox_fk_round.setObjectName(u"checkBox_fk_round")
        self.checkBox_fk_round.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.checkBox_fk_round, 0, 3, 1, 1, Qt.AlignRight)

        self.spinBox_fk_round = QSpinBox(self.groupBox_fk_ouput)
        self.spinBox_fk_round.setObjectName(u"spinBox_fk_round")
        self.spinBox_fk_round.setEnabled(False)

        self.gridLayout_3.addWidget(self.spinBox_fk_round, 0, 4, 1, 1)

        self.comboBox_fk_result = QComboBox(self.groupBox_fk_ouput)
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.addItem("")
        self.comboBox_fk_result.setObjectName(u"comboBox_fk_result")

        self.gridLayout_3.addWidget(self.comboBox_fk_result, 0, 6, 1, 1)

        self.pushButton_fk_result = QPushButton(self.groupBox_fk_ouput)
        self.pushButton_fk_result.setObjectName(u"pushButton_fk_result")
        self.pushButton_fk_result.setEnabled(False)

        self.gridLayout_3.addWidget(self.pushButton_fk_result, 0, 7, 1, 1)

        self.textBrowser_fk_result = QTextBrowser(self.groupBox_fk_ouput)
        self.textBrowser_fk_result.setObjectName(u"textBrowser_fk_result")

        self.gridLayout_3.addWidget(self.textBrowser_fk_result, 1, 0, 1, 8)

        self.horizontalSpacer_fk_output_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_fk_output_2, 0, 5, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 2)
        self.gridLayout_3.setColumnStretch(1, 2)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.gridLayout_3.setColumnStretch(3, 2)
        self.gridLayout_3.setColumnStretch(4, 2)
        self.gridLayout_3.setColumnStretch(5, 1)
        self.gridLayout_3.setColumnStretch(6, 3)
        self.gridLayout_3.setColumnStretch(7, 3)

        self.verticalLayout_tab_fk.addWidget(self.groupBox_fk_ouput)

        self.verticalLayout_tab_fk.setStretch(0, 1)
        self.verticalLayout_tab_fk.setStretch(1, 10)
        self.tabWidget_main.addTab(self.tab_fk, "")
        self.tab_ik = QWidget()
        self.tab_ik.setObjectName(u"tab_ik")
        self.verticalLayout_tab_ik = QVBoxLayout(self.tab_ik)
        self.verticalLayout_tab_ik.setObjectName(u"verticalLayout_tab_ik")
        self.groupBox_ik_input = QGroupBox(self.tab_ik)
        self.groupBox_ik_input.setObjectName(u"groupBox_ik_input")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_ik_input)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_ik_input = QHBoxLayout()
        self.horizontalLayout_ik_input.setObjectName(u"horizontalLayout_ik_input")
        self.label_ik_method = QLabel(self.groupBox_ik_input)
        self.label_ik_method.setObjectName(u"label_ik_method")
        self.label_ik_method.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_ik_input.addWidget(self.label_ik_method)

        self.comboBox_ik_method = QComboBox(self.groupBox_ik_input)
        self.comboBox_ik_method.addItem("")
        self.comboBox_ik_method.addItem("")
        self.comboBox_ik_method.setObjectName(u"comboBox_ik_method")
        self.comboBox_ik_method.setEnabled(False)
        self.comboBox_ik_method.setEditable(False)

        self.horizontalLayout_ik_input.addWidget(self.comboBox_ik_method)

        self.label_ik_coord = QLabel(self.groupBox_ik_input)
        self.label_ik_coord.setObjectName(u"label_ik_coord")
        self.label_ik_coord.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_ik_input.addWidget(self.label_ik_coord)

        self.doubleSpinBox_ik_x = QDoubleSpinBox(self.groupBox_ik_input)
        self.doubleSpinBox_ik_x.setObjectName(u"doubleSpinBox_ik_x")
        self.doubleSpinBox_ik_x.setEnabled(False)
        self.doubleSpinBox_ik_x.setDecimals(6)
        self.doubleSpinBox_ik_x.setMinimum(-100000.000000000000000)
        self.doubleSpinBox_ik_x.setMaximum(100000.000000000000000)

        self.horizontalLayout_ik_input.addWidget(self.doubleSpinBox_ik_x)

        self.doubleSpinBox_ik_y = QDoubleSpinBox(self.groupBox_ik_input)
        self.doubleSpinBox_ik_y.setObjectName(u"doubleSpinBox_ik_y")
        self.doubleSpinBox_ik_y.setEnabled(False)
        self.doubleSpinBox_ik_y.setDecimals(6)
        self.doubleSpinBox_ik_y.setMinimum(-100000.000000000000000)
        self.doubleSpinBox_ik_y.setMaximum(100000.000000000000000)

        self.horizontalLayout_ik_input.addWidget(self.doubleSpinBox_ik_y)

        self.doubleSpinBox_ik_z = QDoubleSpinBox(self.groupBox_ik_input)
        self.doubleSpinBox_ik_z.setObjectName(u"doubleSpinBox_ik_z")
        self.doubleSpinBox_ik_z.setEnabled(False)
        self.doubleSpinBox_ik_z.setDecimals(6)
        self.doubleSpinBox_ik_z.setMinimum(-100000.000000000000000)
        self.doubleSpinBox_ik_z.setMaximum(100000.000000000000000)

        self.horizontalLayout_ik_input.addWidget(self.doubleSpinBox_ik_z)


        self.verticalLayout_4.addLayout(self.horizontalLayout_ik_input)

        self.horizontalLayout_ik_initAngle = QHBoxLayout()
        self.horizontalLayout_ik_initAngle.setObjectName(u"horizontalLayout_ik_initAngle")
        self.horizontalLayout_ik_initAngle_radioButton = QHBoxLayout()
        self.horizontalLayout_ik_initAngle_radioButton.setObjectName(u"horizontalLayout_ik_initAngle_radioButton")
        self.radioButton_ik_rad = QRadioButton(self.groupBox_ik_input)
        self.radioButton_ik_rad.setObjectName(u"radioButton_ik_rad")
        self.radioButton_ik_rad.setChecked(True)

        self.horizontalLayout_ik_initAngle_radioButton.addWidget(self.radioButton_ik_rad)

        self.radioButton_ik_deg = QRadioButton(self.groupBox_ik_input)
        self.radioButton_ik_deg.setObjectName(u"radioButton_ik_deg")

        self.horizontalLayout_ik_initAngle_radioButton.addWidget(self.radioButton_ik_deg)


        self.horizontalLayout_ik_initAngle.addLayout(self.horizontalLayout_ik_initAngle_radioButton)

        self.horizontalLayout_ik_initAngle_doubleSpinBox = QHBoxLayout()
        self.horizontalLayout_ik_initAngle_doubleSpinBox.setObjectName(u"horizontalLayout_ik_initAngle_doubleSpinBox")
        self.label_ik_init_angle = QLabel(self.groupBox_ik_input)
        self.label_ik_init_angle.setObjectName(u"label_ik_init_angle")
        self.label_ik_init_angle.setMaximumSize(QSize(40, 16777215))
        self.label_ik_init_angle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_ik_initAngle_doubleSpinBox.addWidget(self.label_ik_init_angle)

        self.doubleSpinBox_ik_init_j1 = QDoubleSpinBox(self.groupBox_ik_input)
        self.doubleSpinBox_ik_init_j1.setObjectName(u"doubleSpinBox_ik_init_j1")
        self.doubleSpinBox_ik_init_j1.setEnabled(False)
        self.doubleSpinBox_ik_init_j1.setDecimals(6)
        self.doubleSpinBox_ik_init_j1.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_ik_init_j1.setMaximum(1000.000000000000000)

        self.horizontalLayout_ik_initAngle_doubleSpinBox.addWidget(self.doubleSpinBox_ik_init_j1)

        self.doubleSpinBox_ik_init_j2 = QDoubleSpinBox(self.groupBox_ik_input)
        self.doubleSpinBox_ik_init_j2.setObjectName(u"doubleSpinBox_ik_init_j2")
        self.doubleSpinBox_ik_init_j2.setEnabled(False)
        self.doubleSpinBox_ik_init_j2.setDecimals(6)
        self.doubleSpinBox_ik_init_j2.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_ik_init_j2.setMaximum(1000.000000000000000)

        self.horizontalLayout_ik_initAngle_doubleSpinBox.addWidget(self.doubleSpinBox_ik_init_j2)


        self.horizontalLayout_ik_initAngle.addLayout(self.horizontalLayout_ik_initAngle_doubleSpinBox)

        self.horizontalLayout_ik_initAngle.setStretch(0, 1)
        self.horizontalLayout_ik_initAngle.setStretch(1, 4)

        self.verticalLayout_4.addLayout(self.horizontalLayout_ik_initAngle)


        self.verticalLayout_tab_ik.addWidget(self.groupBox_ik_input)

        self.groupBox_ik_output = QGroupBox(self.tab_ik)
        self.groupBox_ik_output.setObjectName(u"groupBox_ik_output")
        self.gridLayout = QGridLayout(self.groupBox_ik_output)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_ik_result = QPushButton(self.groupBox_ik_output)
        self.pushButton_ik_result.setObjectName(u"pushButton_ik_result")
        self.pushButton_ik_result.setEnabled(False)

        self.gridLayout.addWidget(self.pushButton_ik_result, 0, 2, 1, 1)

        self.textBrowser_ik_result = QTextBrowser(self.groupBox_ik_output)
        self.textBrowser_ik_result.setObjectName(u"textBrowser_ik_result")

        self.gridLayout.addWidget(self.textBrowser_ik_result, 1, 0, 1, 3)

        self.checkBox_ik_round = QCheckBox(self.groupBox_ik_output)
        self.checkBox_ik_round.setObjectName(u"checkBox_ik_round")

        self.gridLayout.addWidget(self.checkBox_ik_round, 0, 0, 1, 1)

        self.spinBox_ik_round = QSpinBox(self.groupBox_ik_output)
        self.spinBox_ik_round.setObjectName(u"spinBox_ik_round")

        self.gridLayout.addWidget(self.spinBox_ik_round, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 10)

        self.verticalLayout_tab_ik.addWidget(self.groupBox_ik_output)

        self.verticalLayout_tab_ik.setStretch(0, 2)
        self.verticalLayout_tab_ik.setStretch(1, 10)
        self.tabWidget_main.addTab(self.tab_ik, "")
        self.tab_plot = QWidget()
        self.tab_plot.setObjectName(u"tab_plot")
        self.verticalLayout_tab_plot = QVBoxLayout(self.tab_plot)
        self.verticalLayout_tab_plot.setObjectName(u"verticalLayout_tab_plot")
        self.groupBox_plot_input = QGroupBox(self.tab_plot)
        self.groupBox_plot_input.setObjectName(u"groupBox_plot_input")
        self.horizontalLayout_plot_input = QHBoxLayout(self.groupBox_plot_input)
        self.horizontalLayout_plot_input.setObjectName(u"horizontalLayout_plot_input")
        self.horizontalLayout_plot_input_radioButton = QHBoxLayout()
        self.horizontalLayout_plot_input_radioButton.setObjectName(u"horizontalLayout_plot_input_radioButton")
        self.radioButton_plot_rad = QRadioButton(self.groupBox_plot_input)
        self.radioButton_plot_rad.setObjectName(u"radioButton_plot_rad")
        self.radioButton_plot_rad.setChecked(True)

        self.horizontalLayout_plot_input_radioButton.addWidget(self.radioButton_plot_rad)

        self.radioButton_plot_deg = QRadioButton(self.groupBox_plot_input)
        self.radioButton_plot_deg.setObjectName(u"radioButton_plot_deg")
        self.radioButton_plot_deg.setChecked(False)

        self.horizontalLayout_plot_input_radioButton.addWidget(self.radioButton_plot_deg)


        self.horizontalLayout_plot_input.addLayout(self.horizontalLayout_plot_input_radioButton)

        self.horizontalLayout_plot_input_doubleSpinBox = QHBoxLayout()
        self.horizontalLayout_plot_input_doubleSpinBox.setObjectName(u"horizontalLayout_plot_input_doubleSpinBox")
        self.label_plot_angle = QLabel(self.groupBox_plot_input)
        self.label_plot_angle.setObjectName(u"label_plot_angle")
        self.label_plot_angle.setMaximumSize(QSize(40, 16777215))
        self.label_plot_angle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_plot_input_doubleSpinBox.addWidget(self.label_plot_angle)

        self.doubleSpinBox_plot_j1 = QDoubleSpinBox(self.groupBox_plot_input)
        self.doubleSpinBox_plot_j1.setObjectName(u"doubleSpinBox_plot_j1")
        self.doubleSpinBox_plot_j1.setEnabled(False)
        self.doubleSpinBox_plot_j1.setDecimals(6)
        self.doubleSpinBox_plot_j1.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_plot_j1.setMaximum(1000.000000000000000)

        self.horizontalLayout_plot_input_doubleSpinBox.addWidget(self.doubleSpinBox_plot_j1)

        self.doubleSpinBox_plot_j2 = QDoubleSpinBox(self.groupBox_plot_input)
        self.doubleSpinBox_plot_j2.setObjectName(u"doubleSpinBox_plot_j2")
        self.doubleSpinBox_plot_j2.setEnabled(False)
        self.doubleSpinBox_plot_j2.setDecimals(6)
        self.doubleSpinBox_plot_j2.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_plot_j2.setMaximum(1000.000000000000000)

        self.horizontalLayout_plot_input_doubleSpinBox.addWidget(self.doubleSpinBox_plot_j2)


        self.horizontalLayout_plot_input.addLayout(self.horizontalLayout_plot_input_doubleSpinBox)

        self.horizontalLayout_plot_input.setStretch(0, 1)
        self.horizontalLayout_plot_input.setStretch(1, 4)

        self.verticalLayout_tab_plot.addWidget(self.groupBox_plot_input)

        self.groupBox_plot_output = QGroupBox(self.tab_plot)
        self.groupBox_plot_output.setObjectName(u"groupBox_plot_output")
        self.gridLayout_plot_output = QGridLayout(self.groupBox_plot_output)
        self.gridLayout_plot_output.setObjectName(u"gridLayout_plot_output")
        self.pushButton_plot_output = QPushButton(self.groupBox_plot_output)
        self.pushButton_plot_output.setObjectName(u"pushButton_plot_output")

        self.gridLayout_plot_output.addWidget(self.pushButton_plot_output, 0, 0, 1, 1)


        self.verticalLayout_tab_plot.addWidget(self.groupBox_plot_output)

        self.verticalLayout_tab_plot.setStretch(0, 1)
        self.verticalLayout_tab_plot.setStretch(1, 10)
        self.tabWidget_main.addTab(self.tab_plot, "")
        self.tab_trajectory = QWidget()
        self.tab_trajectory.setObjectName(u"tab_trajectory")
        self.verticalLayout_tab_traj = QVBoxLayout(self.tab_trajectory)
        self.verticalLayout_tab_traj.setObjectName(u"verticalLayout_tab_traj")
        self.groupBox_traj_input = QGroupBox(self.tab_trajectory)
        self.groupBox_traj_input.setObjectName(u"groupBox_traj_input")
        self.verticalLayout = QVBoxLayout(self.groupBox_traj_input)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_traj_input_method_angle = QHBoxLayout()
        self.horizontalLayout_traj_input_method_angle.setObjectName(u"horizontalLayout_traj_input_method_angle")
        self.label = QLabel(self.groupBox_traj_input)
        self.label.setObjectName(u"label")

        self.horizontalLayout_traj_input_method_angle.addWidget(self.label)

        self.comboBox = QComboBox(self.groupBox_traj_input)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_traj_input_method_angle.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_traj_input_method_angle)

        self.horizontalLayout_traj_input_init = QHBoxLayout()
        self.horizontalLayout_traj_input_init.setObjectName(u"horizontalLayout_traj_input_init")

        self.verticalLayout.addLayout(self.horizontalLayout_traj_input_init)


        self.verticalLayout_tab_traj.addWidget(self.groupBox_traj_input)

        self.groupBox_traj_output = QGroupBox(self.tab_trajectory)
        self.groupBox_traj_output.setObjectName(u"groupBox_traj_output")

        self.verticalLayout_tab_traj.addWidget(self.groupBox_traj_output)

        self.verticalLayout_tab_traj.setStretch(0, 2)
        self.verticalLayout_tab_traj.setStretch(1, 10)
        self.tabWidget_main.addTab(self.tab_trajectory, "")

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
        self.radioButton_fk_rad.setText(QCoreApplication.translate("MainWindow", u"\u5f33\u5ea6 (rad)", None))
        self.radioButton_fk_deg.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u5ea6 (deg)", None))
        self.label_fk_angle.setText(QCoreApplication.translate("MainWindow", u"Angle: ", None))
        self.groupBox_fk_ouput.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u51fa", None))
        self.label_fk_joint.setText(QCoreApplication.translate("MainWindow", u"\u8ef8\uff1a", None))
        self.checkBox_fk_round.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u6578\u9ede\u4f4d\u6578: ", None))
        self.comboBox_fk_result.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5ea7\u6a19", None))
        self.comboBox_fk_result.setItemText(1, QCoreApplication.translate("MainWindow", u"zyx\u6b50\u62c9\u89d2", None))
        self.comboBox_fk_result.setItemText(2, QCoreApplication.translate("MainWindow", u"\u65cb\u8f49\u77e9\u9663", None))
        self.comboBox_fk_result.setItemText(3, QCoreApplication.translate("MainWindow", u"\u9f4a\u6b21\u77e9\u9663", None))

        self.pushButton_fk_result.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u7b97\u7d50\u679c", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_fk), QCoreApplication.translate("MainWindow", u"Forward Kinematics", None))
        self.groupBox_ik_input.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u5165", None))
        self.label_ik_method.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u6cd5: ", None))
        self.comboBox_ik_method.setItemText(0, QCoreApplication.translate("MainWindow", u"Simplex", None))
        self.comboBox_ik_method.setItemText(1, QCoreApplication.translate("MainWindow", u"Pieper", None))

        self.label_ik_coord.setText(QCoreApplication.translate("MainWindow", u"\u5ea7\u6a19: ", None))
        self.radioButton_ik_rad.setText(QCoreApplication.translate("MainWindow", u"\u5f33\u5ea6 (rad)", None))
        self.radioButton_ik_deg.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u5ea6 (deg)", None))
        self.label_ik_init_angle.setText(QCoreApplication.translate("MainWindow", u"Angle: ", None))
        self.groupBox_ik_output.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u51fa", None))
        self.pushButton_ik_result.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u7b97\u7d50\u679c", None))
        self.checkBox_ik_round.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u6578\u9ede\u4f4d\u6578: ", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_ik), QCoreApplication.translate("MainWindow", u"Inverse Kinematics", None))
        self.groupBox_plot_input.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u5165", None))
        self.radioButton_plot_rad.setText(QCoreApplication.translate("MainWindow", u"\u5f33\u5ea6 (rad)", None))
        self.radioButton_plot_deg.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u5ea6 (deg)", None))
        self.label_plot_angle.setText(QCoreApplication.translate("MainWindow", u"Angle: ", None))
        self.groupBox_plot_output.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u51fa", None))
        self.pushButton_plot_output.setText(QCoreApplication.translate("MainWindow", u"\u986f\u793a\u7d50\u679c", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_plot), QCoreApplication.translate("MainWindow", u"Plot Robot", None))
        self.groupBox_traj_input.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u5165", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_traj_output.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u51fa", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_trajectory), QCoreApplication.translate("MainWindow", u"Trajectory Planning", None))
        self.menu_setting.setTitle(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
    # retranslateUi

