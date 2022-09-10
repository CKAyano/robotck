import sys
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyle
from ui.ui_main_window import Ui_MainWindow as main_window
from ui.ui_dialog_addDH import Ui_Dialog as dialog_dhAdd
from ui.ui_dialog_saveDH import Ui_Dialog as dialog_dhSave
import pandas as pd
import json
import os
import copy


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
        f'<p style="background-color:grey; color:white; font-weight: bold">{val}</p>'
        if is_str_style(val)
        else val
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


class DHValueError(ValueError):
    pass


class BlankValueError(ValueError):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window()
        self.ui.setupUi(self)

        self.ui.pushButton_newDH.clicked.connect(self.open_addDH)

    def open_addDH(self):
        dlog = DHAddDlg(self)
        dlog.exec()

    def dh_setting_update(self):
        pass


class DHAddDlg(dialog_dhAdd, QDialog):

    DH_DIST_EMPTY = {"d": [], "theta": [], "a": [], "alpha": []}
    DH_LABEL = ["Theta: ", "d: ", "a: ", "Alpha: "]

    def __init__(self, main_window: MainWindow):
        super().__init__()
        # super().__init__(parent)
        self.main_window = main_window

        self.setupUi(self)
        self.is_std = True
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)

        self.pushButton_addlink.clicked.connect(self.add_link)
        self.pushButton_count = 0
        self.buttonBox.accepted.connect(self.save_dh)
        self.radioButton_standard.clicked.connect(self.update_text_std)
        self.radioButton_modified.clicked.connect(self.update_text_mod)
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

    def update_dh_textBrowser(self, t: dict):
        df = pd.DataFrame.from_dict(t)
        if self.is_std:
            df = df[["theta", "d", "a", "alpha"]]
        else:
            df = df[["alpha", "a", "d", "theta"]]
        df.index += 1
        df.index.name = "Links"

        main_folder = "./gui-wrapper/config/df_style"

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
                            "d": lambda x: highlight_str(str(x)),
                            "theta": lambda x: highlight_str(str(x)),
                            "a": lambda x: highlight_str(str(x)),
                            "alpha": lambda x: highlight_str(str(x)),
                        },
                        escape=False,
                    )
                )
            )

        self.textBrowser.setSource(f"{main_folder}/dh_browser.html")
        self.set_scrollBar_buttom()

    def update_text_std(self):
        print(self.is_std)
        if self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[0])
        self.label_second.setText(self.DH_LABEL[1])
        self.label_third.setText(self.DH_LABEL[2])
        self.label_fourth.setText(self.DH_LABEL[3])
        self.is_std = True

    def update_text_mod(self):
        print(self.is_std)
        if not self.is_std:
            return
        self.label_first.setText(self.DH_LABEL[3])
        self.label_second.setText(self.DH_LABEL[2])
        self.label_third.setText(self.DH_LABEL[1])
        self.label_fourth.setText(self.DH_LABEL[0])
        self.is_std = False

    def save_dh(self):
        savedlg = DHSaveDlg(self)
        savedlg.exec()
        print("saved")
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)
        print(DHAddDlg.DH_DIST_EMPTY)
        print(self.dh_dict)

    def cancel(self):
        self.dh_dict = copy.deepcopy(DHAddDlg.DH_DIST_EMPTY)


class DHSaveDlg(dialog_dhSave, QDialog):
    def __init__(self, dh_add: DHAddDlg):
        super().__init__()
        self.setupUi(self)
        self.dh_add = dh_add
        self.buttonBox.accepted.connect(self.save_yaml)

    def blank_name_valid(self, name: str):
        if is_blank(name):
            raise BlankValueError("名字不可空白")

    def save_yaml(self):
        try:
            name = self.lineEdit_name.text()
            error_handling_blank(name, "名字不可為空白")
        except BlankValueError as e:
            print(repr(e))
            warning_msg_box(e.args[-1])
            return

        json_path = "./gui-wrapper/config/dh.json"

        if not os.path.exists(json_path) or os.stat(json_path).st_size == 0:
            with open(json_path, "w") as file:
                file.write("[]")

        with open(json_path, "r") as file:
            dh_all = json.load(file)

        dh_new = {"robot_name": name, "dh": self.dh_add.dh_dict}

        try:
            dh_all.append(dh_new)
        except AttributeError as e:
            print(repr(e))
            warning_msg_box("D-H設定檔格式錯誤")
            return

        with open(json_path, "w") as file:
            json.dump(dh_all, file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
