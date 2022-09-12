import sys
from typing import Optional
from PySide6.QtCore import Qt
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
from gui_wrapper.ui.ui_main_window import Ui_MainWindow as main_window
from gui_wrapper.ui.ui_dialog_addDH import Ui_Dialog as dialog_dhAdd
from gui_wrapper.ui.ui_dialog_saveDH import Ui_Dialog as dialog_dhSave
from gui_wrapper.config.jsonschema import SCHEMA
from robotck.dh_types import DHAngleType, DHType
import pandas as pd
import json
import os
import copy
import jsonschema
from robotck.robot import Robot

CONFIG_PATH = "./gui_wrapper/config"
DH_CONFIG_PATH = f"{CONFIG_PATH}/dh.json"


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
    msg_box.setWindowTitle("輸入錯誤")

    pixmap = QStyle.SP_MessageBoxWarning
    icon = QDialog().style().standardIcon(pixmap)
    msg_box.setWindowIcon(icon)

    msg_box.setIcon(msg_box.Warning)

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


def robot_dict_to_robot_instance(robot_dict: dict) -> Robot:
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window()
        self.ui.setupUi(self)

        self.ui.doubleSpinBox_fk_j_list = []
        self.ui.pushButton_newDH.clicked.connect(self.open_addDH)
        self.ui.comboBox_dh.currentTextChanged.connect(self.dh_selected_event)

        self.robot_instance: Optional[Robot] = None

        check_validated_config(DH_CONFIG_PATH)

        self.update_dh_setting()

    def open_addDH(self):
        dlog = DHAddDlg(self)
        dlog.exec()
        self.update_dh_setting()

    def update_dh_setting(self):
        self.ui.comboBox_dh.clear()
        self.ui.comboBox_dh.addItem("< 請選擇 D-H >")
        with open(DH_CONFIG_PATH, "r") as file:
            dh_all_dict = json.load(file)
        if dh_all_dict:
            dh_all_names = [i["robot_name"] for i in dh_all_dict]
            self.ui.comboBox_dh.addItems(dh_all_names)

    def get_robot_instance(self):
        with open(DH_CONFIG_PATH, "r") as file:
            robot_all_dict = json.load(file)
        if robot_all_dict:
            robot_dict = [i for i in robot_all_dict if i["robot_name"] == self.ui.comboBox_dh.currentText()]
            if robot_dict:
                robot_dict = robot_dict[0]
                robot = robot_dict_to_robot_instance(robot_dict)
                return robot, robot_dict

    def dh_selected_event(self):
        robot_inst_dict = self.get_robot_instance()
        if robot_inst_dict:
            robot, robot_dict = robot_inst_dict
            self.robot_instance = robot
            joints_count = len(robot_dict["is_revol"])
            if robot_dict["is_std"]:
                dh_type_str = "Standrad"
            else:
                dh_type_str = "Modified"
            self.ui.label_info.setText(
                f"機械手臂: {robot_dict['robot_name']}, 軸數: {joints_count}, D-H型態: {dh_type_str}"
            )
            self.reset_fk_input(joints_count)
        else:
            self.dh_default()

    def dh_default(self):
        self.robot_instance = None
        self.ui.label_info.setText(f"請選擇機械手臂D-H")
        self.reset_fk_input(2)
        for i in self.ui.doubleSpinBox_fk_j_list:
            i.setDisabled(True)

    def reset_fk_input(self, angle_count: int):
        for i in reversed(range(self.ui.horizontalLayout_fk_input.count())):
            self.ui.horizontalLayout_fk_input.itemAt(i).widget().setParent(None)

        self.ui.label_fk_angle = QLabel(self.ui.groupBox_fk_input)
        self.ui.label_fk_angle.setObjectName("label_fk_angle")
        self.ui.label_fk_angle.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.ui.label_fk_angle.setText("角度: ")

        self.ui.horizontalLayout_fk_input.addWidget(self.ui.label_fk_angle)

        self.ui.doubleSpinBox_fk_j_list = []
        for i in range(angle_count):
            doubleSpinBox_fk_j_n = QDoubleSpinBox(self.ui.groupBox_fk_input)
            doubleSpinBox_fk_j_n.setObjectName(f"doubleSpinBox_fk_j{i+1}")
            doubleSpinBox_fk_j_n.setDecimals(6)
            self.ui.horizontalLayout_fk_input.addWidget(doubleSpinBox_fk_j_n)
            self.ui.doubleSpinBox_fk_j_list.append(doubleSpinBox_fk_j_n)

        self.ui.radioButton_fk_rad = QRadioButton(self.ui.groupBox_fk_input)
        self.ui.radioButton_fk_rad.setObjectName("radioButton_fk_rad")
        self.ui.radioButton_fk_rad.setChecked(True)
        self.ui.radioButton_fk_rad.setText("弳度 (rad)")

        self.ui.horizontalLayout_fk_input.addWidget(self.ui.radioButton_fk_rad)

        self.ui.radioButton_fk_deg = QRadioButton(self.ui.groupBox_fk_input)
        self.ui.radioButton_fk_deg.setObjectName("radioButton_fk_deg")
        self.ui.radioButton_fk_deg.setChecked(False)
        self.ui.radioButton_fk_deg.setText("角度 (deg)")

        self.ui.horizontalLayout_fk_input.addWidget(self.ui.radioButton_fk_deg)


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

        self.pushButton_addlink.clicked.connect(self.add_link)
        self.pushButton_count = 0
        self.buttonBox.accepted.connect(self.save_dh)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.radioButton_standard.clicked.connect(self.update_text_std)
        self.radioButton_modified.clicked.connect(self.update_text_mod)
        self.radioButton_rad.clicked.connect(self.update_angle_type_rad)
        self.radioButton_deg.clicked.connect(self.update_angle_type_deg)
        self.radioButton_revol.clicked.connect(self.update_joint_type_revol)
        self.radioButton_prism.clicked.connect(self.update_joint_type_prism)
        self.set_scrollBar_buttom()

    def set_scrollBar_buttom(self):
        self.scrollArea.verticalScrollBar().setSliderPosition(self.scrollArea.verticalScrollBar().maximum())

    def dh_value_valid(self, element: str):
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

    def add_link(self):
        try:
            first = self.dh_value_valid(self.lineEdit_first.text())
            second = self.dh_value_valid(self.lineEdit_second.text())
            third = self.dh_value_valid(self.lineEdit_third.text())
            fourth = self.dh_value_valid(self.lineEdit_fourth.text())
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

        self.update_dh_textBrowser(self.dh_dict)
        self.pushButton_count += 1
        if self.pushButton_count > 0:
            self.radioButton_standard.setDisabled(True)
            self.radioButton_modified.setDisabled(True)
            self.radioButton_rad.setDisabled(True)
            self.radioButton_deg.setDisabled(True)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def update_dh_textBrowser(self, t: dict):
        df = pd.DataFrame.from_dict(t)
        if self.is_std:
            df = df[["theta", "d", "a", "alpha"]]
        else:
            df = df[["alpha", "a", "d", "theta"]]
        df.index += 1
        df.index.name = "Links"

        df["is_revol"] = self.revol_list

        main_folder = f"{CONFIG_PATH}/df_style"

        html_string = """
        <html>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <link rel="stylesheet" type="text/css" href="df_style.css"/>
        <body>
            {table}
        </body>
        </html>.
        """

        with open(f"{main_folder}/dh_browser.html", "w") as f:
            f.write(
                html_string.format(
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

        self.textBrowser_dh_list.setSource(f"{main_folder}/dh_browser.html")
        self.set_scrollBar_buttom()

    def update_text_std(self):
        if self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[0])
        self.label_second.setText(self.DH_LABEL[1])
        self.label_third.setText(self.DH_LABEL[2])
        self.label_fourth.setText(self.DH_LABEL[3])
        self.is_std = True

    def update_text_mod(self):
        if not self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[3])
        self.label_second.setText(self.DH_LABEL[2])
        self.label_third.setText(self.DH_LABEL[1])
        self.label_fourth.setText(self.DH_LABEL[0])
        self.is_std = False

    def update_angle_type_rad(self):
        if self.is_rad:
            return
        self.is_rad = True

    def update_angle_type_deg(self):
        if not self.is_rad:
            return
        self.is_rad = False

    def update_joint_type_revol(self):
        if self.is_revol:
            return
        self.is_revol = True

    def update_joint_type_prism(self):
        if not self.is_revol:
            return
        self.is_revol = False

    def save_dh(self):
        savedlg = DHSaveDlg(self)
        savedlg.exec()
        print("saved")
        self.cancel()

    def cancel(self):
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)
        self.revol_list = []


class DHSaveDlg(dialog_dhSave, QDialog):
    def __init__(self, dh_add: DHAddDlg):
        super().__init__()
        self.setupUi(self)
        check_validated_config(DH_CONFIG_PATH)
        self.dh_add = dh_add
        self.buttonBox.accepted.connect(self.save_yaml)

    def save_yaml(self):

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
