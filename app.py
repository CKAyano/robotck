import sys
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QMessageBox,
    QStyle,
    QDialogButtonBox,
    QDoubleSpinBox,
    QRadioButton,
    QLabel,
)
from pyside_files.ui.ui_main_window import Ui_MainWindow as main_window
from pyside_files.ui.ui_dialog_addDH import Ui_Dialog as dialog_dhAdd
from pyside_files.ui.ui_dialog_saveDH import Ui_Dialog as dialog_dhSave
from pyside_files.config.jsonschema import SCHEMA
from robotck.dh_types import DHAngleType, DHType
import pandas as pd
import sympy as sp
import numpy as np
import json
import os
import copy
import jsonschema
from robotck.robot import Robot, deg2rad, DHParameterError
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

np.set_printoptions(suppress=True, threshold=sys.maxsize)

CONFIG_PATH = "./conf"
DH_CONFIG_PATH = f"{CONFIG_PATH}/dh.json"
DH_STYLE_PATH = f"{CONFIG_PATH}/df_style.css"
ICON_PATH = f"{CONFIG_PATH}/ico/icon.png"
TMP_PATH = "./tmp"

HTML_STRING = """
        <html>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <link rel="stylesheet" type="text/css" href="../conf/df_style.css"/>
        <body>
            {table}
        </body>
        </html>.
        """


def is_blank(element: str):
    if len(element) == 0:
        return True
    return False


def is_str_style(element: str):
    if is_blank(element):
        return False
    str_prefix = ['"', "'"]
    if element[0] in str_prefix and element[0] == element[-1]:
        return True
    return False


def is_float(element: str):
    if is_blank(element):
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def error_handling_str(element: str, msg: str):
    if is_str_style(element):
        return element
    raise DHValueError(msg)


def error_handling_float(element: str, msg: str):
    if is_float(element):
        return float(element)
    raise DHValueError(msg)


def error_handling_blank(name: str, msg: str):
    if is_blank(name):
        raise BlankValueError(msg)


def highlight_str(val):
    color = (
        f'<p style="background-color:grey; color:white; font-weight: bold">"{val}"</p>'
        if isinstance(val, str)
        else str(val)
    )
    return color


def warning_msg_box(msg: str):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("警告")

    pixmap = QStyle.SP_MessageBoxWarning
    icon = QDialog().style().standardIcon(pixmap)
    msg_box.setWindowIcon(icon)

    msg_box.setIcon(msg_box.Warning)

    msg_box.setText(msg)
    msg_box.exec()


def info_msg_box(msg: str):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("輸入錯誤")

    pixmap = QStyle.SP_MessageBoxInformation
    icon = QDialog().style().standardIcon(pixmap)
    msg_box.setWindowIcon(icon)

    msg_box.setIcon(msg_box.Information)

    msg_box.setText(msg)
    msg_box.exec()


def is_validated_config(json_path):
    if not os.path.exists(json_path) or os.stat(json_path).st_size == 0:
        with open(json_path, "w") as file:
            file.write("[]")
            return True
    try:
        with open(json_path) as file:
            config = json.load(file)
    except json.decoder.JSONDecodeError:
        return False
    try:
        jsonschema.validate(instance=config, schema=SCHEMA)
        return True
    except jsonschema.ValidationError:
        return False


def check_validated_config(json_path):
    if not is_validated_config(json_path):
        warning_msg_box("設定檔格式有誤")
        sys.exit(0)


def get_robot_instance_from_robot_dict(robot_dict: dict) -> Robot:
    if robot_dict["is_std"]:
        dh_type = DHType.STANDARD
    else:
        dh_type = DHType.MODIFIED

    if robot_dict["is_rad"]:
        dh_angle = DHAngleType.RAD
    else:
        dh_angle = DHAngleType.DEG

    return Robot(robot_dict["dh"], robot_dict["robot_name"], dh_angle, dh_type, robot_dict["is_revol"])


class DHValueError(ValueError):
    pass


class BlankValueError(ValueError):
    pass


class DuplicateNameError(ValueError):
    pass


class MainWindow(main_window, QMainWindow):
    def __init__(self):
        super().__init__()
        print([cls.__name__ for cls in MainWindow.__mro__])

        self.setupUi(self)

        self.setWindowIcon(QIcon(ICON_PATH))

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_main.setTabEnabled(3, False)

        self.doubleSpinBox_fk_j_list: list[QDoubleSpinBox] = []
        self.doubleSpinBox_ik_init_list: list[QDoubleSpinBox] = []
        self.doubleSpinBox_plot_j_list: list[QDoubleSpinBox] = []

        self.robot_instance: Optional[Robot] = None

        self.widget_plot_fig = Figure(figsize=(5, 3))
        self.widget_plot_fig.add_axes([0, 0, 1, 1], projection="3d")
        self.widget_plot = FigureCanvas(self.widget_plot_fig)
        self.gridLayout_plot_output.addWidget(self.widget_plot)

        self._connect_event()

        check_validated_config(DH_CONFIG_PATH)

        self.set_dh_combo_box()
        self.on_change_dh()

    def _connect_event(self):
        self.pushButton_newDH.clicked.connect(self.on_open_addDH)
        self.comboBox_dh.currentTextChanged.connect(self.on_change_dh)

        self.pushButton_fk_result.clicked.connect(self.on_calc_fk_result)
        self.checkBox_fk_round.clicked.connect(self.on_click_fk_checkbox_round)

        self.comboBox_ik_method.currentTextChanged.connect(self.on_change_ik_method)
        self.pushButton_ik_result.clicked.connect(self.on_calc_ik_result)
        self.checkBox_ik_round.clicked.connect(self.on_click_ik_checkbox_round)

        # self.tabWidget_main.currentChanged.connect(self.on_change_dh)

        self.pushButton_plot_output.clicked.connect(self.on_plot_result)

    def is_default_dh(self):
        return self.comboBox_dh.currentIndex() == 0

    def on_open_addDH(self):
        dlog = DHAddDlg(self)
        dlog.exec()
        self.set_dh_combo_box()

    def set_dh_combo_box(self):
        self.comboBox_dh.clear()
        self.comboBox_dh.addItem("< 請選擇 D-H >")
        with open(DH_CONFIG_PATH, "r") as file:
            dh_all_dict = json.load(file)
        if dh_all_dict:
            dh_all_names = [i["robot_name"] for i in dh_all_dict]
            self.comboBox_dh.addItems(dh_all_names)

    def get_robot_instance(self):
        with open(DH_CONFIG_PATH, "r") as file:
            robot_all_dict = json.load(file)
        if robot_all_dict:
            robot_dict = [i for i in robot_all_dict if i["robot_name"] == self.comboBox_dh.currentText()]
            if robot_dict:
                robot_dict = robot_dict[0]
                robot = get_robot_instance_from_robot_dict(robot_dict)
                return robot

    def is_current_tab(self, idx: int):
        if self.tabWidget_main.currentIndex() == idx:
            return True
        return False

    def on_change_dh(self):
        if self.is_default_dh():
            self.set_dh_default()
            return

        robot = self.get_robot_instance()
        if robot:
            self.robot_instance = robot
            joints_count = robot.links_count
            if robot.dh_type == DHType.STANDARD:
                dh_type_str = "Standrad"
            else:
                dh_type_str = "Modified"
            self.label_info.setText(f"機械手臂: {robot.name}, 軸數: {joints_count}, D-H型態: {dh_type_str}")
            # if self.is_current_tab(0):
            self.set_fk_input(joints_count)
            self.set_fk_output(joints_count)
            # if self.is_current_tab(1):
            self.set_ik_input(joints_count)
            self.set_ik_output()
            self.on_change_ik_method()
            # if self.is_current_tab(2):
            self.set_plot_input(joints_count)
            self.set_plot_output([0] * robot.links_count)

    def set_dh_default_fk_io(self):
        self.set_fk_input(2)
        self.set_fk_output(2)
        for i in self.doubleSpinBox_fk_j_list:
            i.setDisabled(True)
        self.pushButton_fk_result.setDisabled(True)
        self.textBrowser_fk_result.clear()

    def set_dh_default_ik_io(self):
        self.set_ik_input(2)
        self.set_ik_output()
        self.comboBox_ik_method.setDisabled(True)
        self.doubleSpinBox_ik_x.setDisabled(True)
        self.doubleSpinBox_ik_y.setDisabled(True)
        self.doubleSpinBox_ik_z.setDisabled(True)
        for i in self.doubleSpinBox_ik_init_list:
            i.setDisabled(True)
        self.pushButton_ik_result.setDisabled(True)
        self.textBrowser_ik_result.clear()

    def set_dh_default_plot_io(self):
        self.set_plot_input(2)
        self.widget_plot_fig.axes[0].clear()
        self.widget_plot_fig.canvas.draw_idle()
        self.pushButton_plot_output.setDisabled(True)
        for i in self.doubleSpinBox_plot_j_list:
            i.setDisabled(True)

    def set_dh_default(self):
        self.robot_instance = None
        self.label_info.setText("請選擇機械手臂D-H")

        if self.is_current_tab(0):
            self.set_dh_default_fk_io()
        if self.is_current_tab(1):
            self.set_dh_default_ik_io()
        if self.is_current_tab(2):
            self.set_dh_default_plot_io()

    def set_fk_input(self, joints_count: int):
        for i in reversed(range(self.horizontalLayout_fk_input.count())):
            self.horizontalLayout_fk_input.itemAt(i).widget().setParent(None)

        self.label_fk_angle = QLabel(self.groupBox_fk_input)
        self.label_fk_angle.setObjectName("label_fk_angle")
        self.label_fk_angle.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_fk_angle.setText("角度: ")

        self.horizontalLayout_fk_input.addWidget(self.label_fk_angle)

        self.doubleSpinBox_fk_j_list = []
        for i in range(joints_count):
            doubleSpinBox_fk_j_n = QDoubleSpinBox(self.groupBox_fk_input)
            doubleSpinBox_fk_j_n.setObjectName(f"doubleSpinBox_fk_j{i+1}")
            doubleSpinBox_fk_j_n.setDecimals(6)
            doubleSpinBox_fk_j_n.setRange(-10000, 10000)
            self.horizontalLayout_fk_input.addWidget(doubleSpinBox_fk_j_n)
            self.doubleSpinBox_fk_j_list.append(doubleSpinBox_fk_j_n)

        self.radioButton_fk_rad = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_rad.setObjectName("radioButton_fk_rad")
        self.radioButton_fk_rad.setChecked(True)
        self.radioButton_fk_rad.setText("弳度 (rad)")

        self.horizontalLayout_fk_input.addWidget(self.radioButton_fk_rad)

        self.radioButton_fk_deg = QRadioButton(self.groupBox_fk_input)
        self.radioButton_fk_deg.setObjectName("radioButton_fk_deg")
        self.radioButton_fk_deg.setChecked(False)
        self.radioButton_fk_deg.setText("角度 (deg)")

        self.horizontalLayout_fk_input.addWidget(self.radioButton_fk_deg)

    def set_fk_output(self, joints_count: int):
        self.spinBox_fk_numjoint.setRange(1, joints_count)
        self.spinBox_fk_numjoint.setValue(joints_count)
        if not self.checkBox_fk_round.isChecked():
            self.spinBox_fk_round.setDisabled(True)
        self.pushButton_fk_result.setDisabled(False)
        self.textBrowser_fk_result.clear()

    def on_click_fk_checkbox_round(self):
        if self.checkBox_fk_round.isChecked():
            self.spinBox_fk_round.setDisabled(False)
            return
        self.spinBox_fk_round.setDisabled(True)

    def get_fk_input_angle(self):
        joints = []
        for i in self.doubleSpinBox_fk_j_list:
            joints.append(i.value())
        return joints

    def get_fk(self):
        robot = self.robot_instance
        if robot:
            angles = self.get_fk_input_angle()
            if self.radioButton_fk_deg.isChecked():
                angles = deg2rad(angles)
            links = robot.forword_kine(angles)

            num_joint = self.spinBox_fk_numjoint.value()
            output_type = self.comboBox_fk_result.currentText()

            link = links.get_joint(num_joint)
            if self.checkBox_fk_round.isChecked():
                link.round(self.spinBox_fk_round.value())
            if output_type == "座標":
                output = link.coord
                output_index = ["x", "y", "z"]
            elif output_type == "zyx歐拉角":
                output = link.zyxeuler
                output_index = ["alpha", "beta", "gamma"]
            elif output_type == "旋轉矩陣":
                output = link.rot
                output_index = False
            elif output_type == "齊次矩陣":
                output = link.matrix
                output_index = False
        else:
            output = []
            output_index = False
        return output, output_index

    def on_calc_fk_result(self):
        fk, output_index = self.get_fk()
        if isinstance(fk, sp.Matrix):
            fk = sp.matrix2numpy(fk)

        df = pd.DataFrame(fk)

        df = df.astype(str)

        if bool(output_index):
            df.index = output_index

        with open(f"{TMP_PATH}/fk_result_browser.html", "w") as f:
            f.write(
                HTML_STRING.format(
                    table=df.to_html(classes="table-style", header=False, index=bool(output_index))
                )
            )
        self.textBrowser_fk_result.setSource(f"{TMP_PATH}/fk_result_browser.html")

    def set_ik_input(self, joints_count):
        self.comboBox_ik_method.setDisabled(False)
        self.doubleSpinBox_ik_x.setDisabled(False)
        self.doubleSpinBox_ik_y.setDisabled(False)
        self.doubleSpinBox_ik_z.setDisabled(False)
        for i in reversed(range(self.horizontalLayout_ik_initAngle.count())):
            self.horizontalLayout_ik_initAngle.itemAt(i).widget().setParent(None)

        self.label_ik_init_angle = QLabel(self.groupBox_ik_input)
        self.label_ik_init_angle.setObjectName("label_ik_init_angle")
        self.label_ik_init_angle.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_ik_init_angle.setText("初始角度: ")

        self.horizontalLayout_ik_initAngle.addWidget(self.label_ik_init_angle)

        self.doubleSpinBox_ik_init_list = []
        for i in range(joints_count):
            doubleSpinBox_ik_j_n = QDoubleSpinBox(self.groupBox_ik_input)
            doubleSpinBox_ik_j_n.setObjectName(f"doubleSpinBox_ik_init_j{i+1}")
            doubleSpinBox_ik_j_n.setDecimals(6)
            doubleSpinBox_ik_j_n.setRange(-100000000, 100000000)
            self.horizontalLayout_ik_initAngle.addWidget(doubleSpinBox_ik_j_n)
            self.doubleSpinBox_ik_init_list.append(doubleSpinBox_ik_j_n)

        self.radioButton_ik_init_rad = QRadioButton(self.groupBox_ik_input)
        self.radioButton_ik_init_rad.setObjectName("radioButton_ik_init_rad")
        self.radioButton_ik_init_rad.setChecked(True)
        self.radioButton_ik_init_rad.setText("弳度 (rad)")

        self.horizontalLayout_ik_initAngle.addWidget(self.radioButton_ik_init_rad)

        self.radioButton_ik_init_deg = QRadioButton(self.groupBox_ik_input)
        self.radioButton_ik_init_deg.setObjectName("radioButton_ik_init_deg")
        self.radioButton_ik_init_deg.setChecked(False)
        self.radioButton_ik_init_deg.setText("角度 (deg)")

        self.horizontalLayout_ik_initAngle.addWidget(self.radioButton_ik_init_deg)

    def set_ik_output(self):
        self.pushButton_ik_result.setDisabled(False)
        if not self.checkBox_ik_round.isChecked():
            self.spinBox_ik_round.setDisabled(True)
        self.textBrowser_ik_result.clear()

    def on_change_ik_method(self):
        if self.comboBox_ik_method.currentText() == "Simplex":
            for i in self.doubleSpinBox_ik_init_list:
                i.setDisabled(False)
        if self.comboBox_ik_method.currentText() == "Pieper":
            for i in self.doubleSpinBox_ik_init_list:
                i.setDisabled(True)

    def on_click_ik_checkbox_round(self):
        if self.checkBox_ik_round.isChecked():
            self.spinBox_ik_round.setDisabled(False)
            return
        self.spinBox_ik_round.setDisabled(True)

    def get_ik(self):
        coord_x = self.doubleSpinBox_ik_x.value()
        coord_y = self.doubleSpinBox_ik_y.value()
        coord_z = self.doubleSpinBox_ik_z.value()
        coord = [coord_x, coord_y, coord_z]
        if self.comboBox_ik_method.currentText() == "Simplex":
            init_angle = []
            for i in self.doubleSpinBox_ik_init_list:
                init_angle.append(i.value())
            if self.radioButton_ik_init_deg.isChecked():
                init_angle = deg2rad(init_angle)
            ik, is_warned, err = self.robot_instance.inverse_kine_simplex(coord, init_angle, save_err=True)
            if is_warned:
                warning_msg_box(f"座標誤差高於0.1({err:.4f}), 此座標「可能」無法到達, 或嘗試調整初始角度")
            else:
                info_msg_box(f"座標誤差為{err:E}")
        elif self.comboBox_ik_method.currentText() == "Pieper":
            try:
                ik = self.robot_instance.inverse_kine_pieper_first_three(coord)
            except DHParameterError:
                warning_msg_box("此DH不符合Pieper準則")
                return
        if isinstance(ik, sp.Matrix):
            ik = sp.matrix2numpy(ik)
        if self.checkBox_ik_round.isChecked():
            ik = np.round(ik, self.spinBox_ik_round.value())
        if ik.ndim > 1:
            return ik
        return ik[None, :]

    def on_calc_ik_result(self):
        ik = self.get_ik()
        if ik is not None:
            if isinstance(ik, sp.Matrix):
                ik = sp.matrix2numpy(ik)

            df = pd.DataFrame(ik)

            df.columns = [f"Joint {i+1}" for i in range(df.shape[1])]

            df.index = [f"sol {i+1}" for i in range(df.shape[0])]
            if df.shape[0] == 1:
                df.index = ["sol"]

            df = df.astype(str)

            with open(f"{TMP_PATH}/ik_result_browser.html", "w") as f:
                f.write(HTML_STRING.format(table=df.to_html(classes="table-style", header=True, index=True)))
            self.textBrowser_ik_result.setSource(f"{TMP_PATH}/ik_result_browser.html")

    def replot_robot(self, joints_angle=None):
        self.widget_plot_fig.axes[0].clear()
        if joints_angle is not None:
            _dh_array = copy.deepcopy(self.robot_instance.dh_array)
            for i in range(_dh_array.shape[0]):
                for j in range(_dh_array.shape[1]):
                    if isinstance(_dh_array[i, j], str):
                        _dh_array[i, j] = np.nan
            longest_link = np.nanmax(np.abs(_dh_array))
            joint_radius = longest_link * 0.05
            # joint_radius = 10
            self.robot_instance.plot(
                joints_angle, joint_radius=joint_radius, qt_ax=self.widget_plot_fig.axes[0], is_plot=False
            )
        self.widget_plot_fig.canvas.draw_idle()

    def set_plot_input(self, joints_count):
        for i in reversed(range(self.horizontalLayout_plot_input.count())):
            self.horizontalLayout_plot_input.itemAt(i).widget().setParent(None)

        self.label_plot_angle = QLabel(self.groupBox_plot_input)
        self.label_plot_angle.setObjectName("label_plot_angle")
        self.label_plot_angle.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_plot_angle.setText("初始角度: ")

        self.horizontalLayout_plot_input.addWidget(self.label_plot_angle)

        self.doubleSpinBox_plot_j_list = []
        for i in range(joints_count):
            doubleSpinBox_plot_j_n = QDoubleSpinBox(self.groupBox_plot_input)
            doubleSpinBox_plot_j_n.setObjectName(f"doubleSpinBox_plot_j{i+1}")
            doubleSpinBox_plot_j_n.setDecimals(6)
            doubleSpinBox_plot_j_n.setRange(-100000, 100000)
            self.horizontalLayout_plot_input.addWidget(doubleSpinBox_plot_j_n)
            self.doubleSpinBox_plot_j_list.append(doubleSpinBox_plot_j_n)

        self.radioButton_plot_rad = QRadioButton(self.groupBox_plot_input)
        self.radioButton_plot_rad.setObjectName("radioButton_plot_rad")
        self.radioButton_plot_rad.setChecked(True)
        self.radioButton_plot_rad.setText("弳度 (rad)")

        self.horizontalLayout_plot_input.addWidget(self.radioButton_plot_rad)

        self.radioButton_plot_deg = QRadioButton(self.groupBox_plot_input)
        self.radioButton_plot_deg.setObjectName("radioButton_plot_deg")
        self.radioButton_plot_deg.setChecked(False)
        self.radioButton_plot_deg.setText("角度 (deg)")

        self.horizontalLayout_plot_input.addWidget(self.radioButton_plot_deg)

    def set_plot_output(self, joints_angle: list):
        self.pushButton_plot_output.setDisabled(False)
        self.replot_robot(joints_angle)

    def on_plot_result(self):
        joints = []
        for i in self.doubleSpinBox_plot_j_list:
            joints.append(i.value())
        if self.radioButton_plot_deg.isChecked():
            joints = deg2rad(joints)
        self.replot_robot(joints)


class DHAddDlg(dialog_dhAdd, QDialog):

    DH_DIST_EMPTY = {"d": [], "theta": [], "a": [], "alpha": []}
    DH_LABEL = ["Theta: ", "d: ", "a: ", "Alpha: "]

    def __init__(self, main_window: MainWindow):
        super().__init__()
        # super().__init__(parent)
        self.main_window = main_window

        self.setupUi(self)
        self.is_std = True
        self.is_rad = True
        self.is_revol = True
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)
        self.revol_list = []

        self.pushButton_addlink.clicked.connect(self.on_add_link)
        self.pushButton_count = 0
        self.buttonBox.accepted.connect(self.on_save_dh)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.radioButton_standard.clicked.connect(self.on_update_text_std)
        self.radioButton_modified.clicked.connect(self.on_update_text_mod)
        self.radioButton_rad.clicked.connect(self.on_update_angle_type_rad)
        self.radioButton_deg.clicked.connect(self.on_update_angle_type_deg)
        self.radioButton_revol.clicked.connect(self.on_update_joint_type_revol)
        self.radioButton_prism.clicked.connect(self.on_update_joint_type_prism)
        self.set_scrollBar_buttom()

    def set_scrollBar_buttom(self):
        self.scrollArea.verticalScrollBar().setSliderPosition(self.scrollArea.verticalScrollBar().maximum())

    def verify_dh_value(self, element: str):
        msg = '輸入數字或 "(文字)"'
        msg_blank = "不可為空白"
        try:
            error_handling_blank(element, msg_blank)
        except BlankValueError:
            raise DHValueError(msg_blank)

        try:
            el = error_handling_float(element, msg)
            return el
        except DHValueError:
            try:
                el = error_handling_str(element, msg)
                el = el[1:-1]
                return el
            except DHValueError:
                raise DHValueError(msg)

    def on_add_link(self):
        try:
            first = self.verify_dh_value(self.lineEdit_first.text())
            second = self.verify_dh_value(self.lineEdit_second.text())
            third = self.verify_dh_value(self.lineEdit_third.text())
            fourth = self.verify_dh_value(self.lineEdit_fourth.text())
        except DHValueError as e:
            print(repr(e))
            warning_msg_box(e.args[-1])
            return

        if self.is_std:
            self.dh_dict["theta"].append(first)
            self.dh_dict["d"].append(second)
            self.dh_dict["a"].append(third)
            self.dh_dict["alpha"].append(fourth)
        else:
            self.dh_dict["alpha"].append(first)
            self.dh_dict["a"].append(second)
            self.dh_dict["d"].append(third)
            self.dh_dict["theta"].append(fourth)

        if self.is_revol:
            self.revol_list.append(True)
        else:
            self.revol_list.append(False)

        self.set_dh_textBrowser(self.dh_dict)
        self.pushButton_count += 1
        if self.pushButton_count > 0:
            self.radioButton_standard.setDisabled(True)
            self.radioButton_modified.setDisabled(True)
            self.radioButton_rad.setDisabled(True)
            self.radioButton_deg.setDisabled(True)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def set_dh_textBrowser(self, t: dict):
        df = pd.DataFrame.from_dict(t)
        if self.is_std:
            df = df[["theta", "d", "a", "alpha"]]
        else:
            df = df[["alpha", "a", "d", "theta"]]
        df.index += 1
        df.index.name = "Links"

        df["is_revol"] = self.revol_list

        with open(f"{TMP_PATH}/dh_browser.html", "w") as f:
            f.write(
                HTML_STRING.format(
                    table=df.to_html(
                        classes="table-style",
                        formatters={
                            "d": lambda x: highlight_str(x),
                            "theta": lambda x: highlight_str(x),
                            "a": lambda x: highlight_str(x),
                            "alpha": lambda x: highlight_str(x),
                        },
                        escape=False,
                    )
                )
            )

        self.textBrowser_dh_list.setSource(f"{TMP_PATH}/dh_browser.html")
        self.set_scrollBar_buttom()

    def on_update_text_std(self):
        if self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[0])
        self.label_second.setText(self.DH_LABEL[1])
        self.label_third.setText(self.DH_LABEL[2])
        self.label_fourth.setText(self.DH_LABEL[3])
        self.is_std = True

    def on_update_text_mod(self):
        if not self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[3])
        self.label_second.setText(self.DH_LABEL[2])
        self.label_third.setText(self.DH_LABEL[1])
        self.label_fourth.setText(self.DH_LABEL[0])
        self.is_std = False

    def on_update_angle_type_rad(self):
        if self.is_rad:
            return
        self.is_rad = True

    def on_update_angle_type_deg(self):
        if not self.is_rad:
            return
        self.is_rad = False

    def on_update_joint_type_revol(self):
        if self.is_revol:
            return
        self.is_revol = True

    def on_update_joint_type_prism(self):
        if not self.is_revol:
            return
        self.is_revol = False

    def on_save_dh(self):
        savedlg = DHSaveDlg(self)
        savedlg.exec()
        self.initialize()

    def initialize(self):
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)
        self.revol_list = []


class DHSaveDlg(dialog_dhSave, QDialog):
    def __init__(self, dh_add: DHAddDlg):
        super().__init__()
        self.setupUi(self)
        check_validated_config(DH_CONFIG_PATH)
        self.dh_add = dh_add
        self.buttonBox.accepted.connect(self.on_save_yaml)

    def on_save_yaml(self):

        try:
            name = self.lineEdit_name.text()
            error_handling_blank(name, "名字不可為空白")
        except BlankValueError as e:
            print(repr(e))
            warning_msg_box(e.args[-1])
            return

        with open(DH_CONFIG_PATH, "r") as file:
            robot_all = json.load(file)

        if self.is_name_duplicate(robot_all):
            warning_msg_box("名字重複")
            return

        robot_new = {
            "robot_name": name,
            "dh": self.dh_add.dh_dict,
            "is_std": self.dh_add.is_std,
            "is_rad": self.dh_add.is_rad,
            "is_revol": self.dh_add.revol_list,
        }

        robot_all.append(robot_new)

        with open(DH_CONFIG_PATH, "w") as file:
            json.dump(robot_all, file, indent=2)

    def is_name_duplicate(self, robot_all: list[dict]):
        robot_all_names = [i["robot_name"] for i in robot_all]
        if robot_all_names:
            if self.lineEdit_name.text() in robot_all_names:
                return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
