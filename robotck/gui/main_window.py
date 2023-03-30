import copy
import json
from typing import Optional
import numpy as np
import pandas as pd
import sympy as sp
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDoubleSpinBox, QMainWindow

from ..base import DHParameterError, Robot, deg2rad, DHType
from .dialog_addDH import DHAddDlg
from .msg_box import info_msg_box, warning_msg_box
from .uic.ui_main_window import Ui_MainWindow as main_window
from .utils import (
    DH_CONFIG_PATH,
    HTML_STRING,
    ICON_PATH,
    TMP_PATH,
    check_validated_config,
    get_robot_instance_from_robot_dict,
    mkdir_if_folder_not_exist,
)


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

        mkdir_if_folder_not_exist()
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

        self.pushButton_plot_output.clicked.connect(self.on_plot_result)

    @staticmethod
    def set_input_ui(layout, doubleSpinBox_list: list, doubleSpinBox_objname, joints_count):
        groupBox = layout.parentWidget()

        for i in reversed(range(layout.count())):
            if isinstance(layout.itemAt(i).widget(), QDoubleSpinBox):
                layout.itemAt(i).widget().setParent(None)

        doubleSpinBox_list.clear()
        for i in range(joints_count):
            doubleSpinBox_fk_j_n = QDoubleSpinBox(groupBox)
            doubleSpinBox_fk_j_n.setObjectName(f"{doubleSpinBox_objname}{i+1}")
            doubleSpinBox_fk_j_n.setDecimals(6)
            doubleSpinBox_fk_j_n.setRange(-10000, 10000)
            layout.addWidget(doubleSpinBox_fk_j_n)
            doubleSpinBox_list.append(doubleSpinBox_fk_j_n)

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
        # idx start at 0
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
            self.set_fk_input(joints_count)
            self.set_fk_output(joints_count)

            self.set_ik_input(joints_count)
            self.set_ik_output()
            self.on_change_ik_method()

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
        self.set_input_ui(
            self.horizontalLayout_fk_input_doubleSpinBox,
            self.doubleSpinBox_fk_j_list,
            "doubleSpinBox_fk_j",
            joints_count,
        )

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
        _path = QUrl.fromLocalFile(f"{TMP_PATH}/fk_result_browser.html")
        self.textBrowser_fk_result.clear()
        self.textBrowser_fk_result.setSource(_path)

    def set_ik_input(self, joints_count):
        self.comboBox_ik_method.setDisabled(False)
        self.doubleSpinBox_ik_x.setDisabled(False)
        self.doubleSpinBox_ik_y.setDisabled(False)
        self.doubleSpinBox_ik_z.setDisabled(False)
        self.set_input_ui(
            self.horizontalLayout_ik_initAngle_doubleSpinBox,
            self.doubleSpinBox_ik_init_list,
            "doubleSpinBox_ik_init_j",
            joints_count,
        )

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
            if self.radioButton_ik_deg.isChecked():
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
            _path = QUrl.fromLocalFile(f"{TMP_PATH}/ik_result_browser.html")
            self.textBrowser_ik_result.clear()
            self.textBrowser_ik_result.setSource(_path)

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
        self.set_input_ui(
            self.horizontalLayout_plot_input_doubleSpinBox,
            self.doubleSpinBox_plot_j_list,
            "doubleSpinBox_plot_j",
            joints_count,
        )

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
