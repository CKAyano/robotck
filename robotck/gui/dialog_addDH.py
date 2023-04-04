import copy

import pandas as pd
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QDialog, QDialogButtonBox

# from .main_window import MainWindow
from .dialog_saveDH import DHSaveDlg
from .exception import DHValueError
from .msg_box import warning_msg_box
from .uic.ui_dialog_addDH import Ui_Dialog as dialog_dhAdd
from .utils import (
    HTML_STRING,
    TMP_PATH,
    error_handling_blank,
    error_handling_float,
    error_handling_str,
    highlight_str,
)


class DHAddDlg(dialog_dhAdd, QDialog):

    DH_DIST_EMPTY = {"d": [], "theta": [], "a": [], "alpha": []}
    DH_LABEL = ["Theta: ", "d: ", "a: ", "Alpha: "]

    def __init__(self, main_window):
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
        error_handling_blank(element, msg_blank)
        try:
            el = error_handling_float(element, msg)
            return el
        except DHValueError:
            el = error_handling_str(element, msg)
            el = el[1:-1]
            return el

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
        _path = QUrl.fromLocalFile(f"{TMP_PATH}/dh_browser.html")
        self.textBrowser_dh_list.clear()
        self.textBrowser_dh_list.setSource(_path)
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
