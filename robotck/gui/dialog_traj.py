import numpy as np
import pandas as pd
from PySide6.QtCore import QUrl
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit

from ..base import deg2rad
from .uic.ui_dialog_traj import Ui_Dialog as dialog_traj
from .utils import HTML_STRING, TMP_PATH


class TrajDlg(dialog_traj, QDialog):
    def __init__(self, main_window, joints_count):
        super().__init__()
        self.main_window = main_window
        self.joints_count = joints_count
        self.setupUi(self)
        self.is_rad = True
        self.is_cartesian = True
        self.points = None

        self.radioButton_deg.clicked.connect(self.on_clicked_angle_type)
        self.radioButton_rad.clicked.connect(self.on_clicked_angle_type)
        self.radioButton_objective_cartesian.clicked.connect(self.on_clicked_objective_space)
        self.radioButton_objective_joint.clicked.connect(self.on_clicked_objective_space)
        self.pushButton_add.clicked.connect(self.on_clicked_add)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.rejected.connect(self.on_cancel)

        self.set_input_label_ui()
        self.set_input_value_ui()
        self.on_clicked_objective_space()
        self.on_clicked_angle_type()

    def on_clicked_angle_type(self):
        if self.radioButton_rad.isChecked():
            self.is_rad = True
            return
        self.is_rad = False

    def on_clicked_objective_space(self):
        if self.radioButton_objective_cartesian.isChecked():
            self.is_cartesian = True
            self.points = np.empty((0, 3))
        else:
            self.is_cartesian = False
            self.points = np.empty((0, self.joints_count))
        self.set_input_label_ui()
        self.set_input_value_ui()

    def on_clicked_add(self):
        if self.is_cartesian:
            line_count = 3
        else:
            line_count = self.joints_count
        line_value = []
        for i in range(line_count):
            _t = self.verticalLayout_input_value.itemAt(i).widget().text()
            _v = float(_t)
            if not self.is_rad:
                _v = deg2rad(_v)
            line_value.append(float(_t))
        line_value = np.array([line_value])
        self.points = np.vstack((self.points, line_value))
        self.set_points_textBrowser()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def set_input_label_ui(self):
        label_parent = self.label_x.parent()
        for i in reversed(range(self.verticalLayout_input_label.count())):
            if isinstance(self.verticalLayout_input_label.itemAt(i).widget(), QLabel):
                self.verticalLayout_input_label.itemAt(i).widget().setParent(None)
        if self.is_cartesian:
            label_x = QLabel(label_parent)
            label_x.setObjectName("label_x")
            label_x.setText("X:")
            label_x.setMaximumHeight(20)
            label_x.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.verticalLayout_input_label.addWidget(label_x)

            label_y = QLabel(label_parent)
            label_y.setObjectName("label_y")
            label_y.setText("Y:")
            label_y.setMaximumHeight(20)
            label_y.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.verticalLayout_input_label.addWidget(label_y)

            label_z = QLabel(label_parent)
            label_z.setObjectName("label_z")
            label_z.setText("Z:")
            label_z.setMaximumHeight(20)
            label_z.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.verticalLayout_input_label.addWidget(label_z)
            return

        for i in range(self.joints_count):
            label_joint = QLabel(label_parent)
            label_joint.setObjectName(f"label_joint{i+1}")
            label_joint.setText(f"joint {i+1}")
            label_joint.setMaximumHeight(20)
            label_joint.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.verticalLayout_input_label.addWidget(label_joint)

    def set_input_value_ui(self):
        value_parent = self.lineEdit.parent()
        for i in reversed(range(self.verticalLayout_input_value.count())):
            if isinstance(self.verticalLayout_input_value.itemAt(i).widget(), QLineEdit):
                self.verticalLayout_input_value.itemAt(i).widget().setParent(None)
        if self.is_cartesian:
            input_count = 3
        else:
            input_count = self.joints_count
        for i in range(input_count):
            line = QLineEdit(value_parent)
            line.setObjectName(f"lineEdit_{i+1}")
            self.verticalLayout_input_value.addWidget(line)

    def set_points_textBrowser(self):
        df = pd.DataFrame(self.points)
        df.index += 1

        with open(f"{TMP_PATH}/traj_browser.html", "w") as f:
            f.write(
                HTML_STRING.format(
                    table=df.to_html(
                        classes="table-style",
                        escape=False,
                        header=False,
                    )
                )
            )
        _path = QUrl.fromLocalFile(f"{TMP_PATH}/traj_browser.html")
        self.textBrowser.clear()
        self.textBrowser.setSource(_path)

    def on_cancel(self):
        self.points = np.empty((0, 3))
