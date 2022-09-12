import sys
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyle
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

        self.ui.pushButton_newDH.clicked.connect(self.open_addDH)

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
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)

        self.pushButton_addlink.clicked.connect(self.add_link)
        self.pushButton_count = 0
        self.buttonBox.accepted.connect(self.save_dh)
        self.radioButton_standard.clicked.connect(self.update_text_std)
        self.radioButton_modified.clicked.connect(self.update_text_mod)
        self.radioButton_rad.clicked.connect(self.update_angle_type_rad)
        self.radioButton_deg.clicked.connect(self.update_angle_type_deg)
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

        self.update_dh_textBrowser(self.dh_dict)
        self.pushButton_count += 1
        if self.pushButton_count > 0:
            self.radioButton_standard.setDisabled(True)
            self.radioButton_modified.setDisabled(True)
            self.radioButton_rad.setDisabled(True)
            self.radioButton_deg.setDisabled(True)

    def update_dh_textBrowser(self, t: dict):
        df = pd.DataFrame.from_dict(t)
        if self.is_std:
            df = df[["theta", "d", "a", "alpha"]]
        else:
            df = df[["alpha", "a", "d", "theta"]]
        df.index += 1
        df.index.name = "Links"

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

    def save_dh(self):
        savedlg = DHSaveDlg(self)
        savedlg.exec()
        print("saved")
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)

    def cancel(self):
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)


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
            dh_all = json.load(file)

        if self.is_name_duplicate(dh_all):
            warning_msg_box("名字重複")
            return

        dh_new = {
            "robot_name": name,
            "dh": self.dh_add.dh_dict,
            "is_std": self.dh_add.is_std,
            "is_rad": self.dh_add.is_rad,
        }

        dh_all.append(dh_new)

        with open(DH_CONFIG_PATH, "w") as file:
            json.dump(dh_all, file, indent=2)

    def is_name_duplicate(self, dh_all: list[dict]):
        dh_all_names = [i["robot_name"] for i in dh_all]
        if dh_all_names:
            if self.lineEdit_name.text() in dh_all_names:
                return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
