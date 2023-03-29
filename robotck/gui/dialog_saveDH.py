from PySide6.QtWidgets import QDialog
import json
from .uic.ui_dialog_saveDH import Ui_Dialog as dialog_dhSave
from .exception import BlankValueError
from .msg_box import warning_msg_box
from .utils import DH_CONFIG_PATH, check_validated_config, error_handling_blank


class DHSaveDlg(dialog_dhSave, QDialog):
    def __init__(self, dh_add):
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
