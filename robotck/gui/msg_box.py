from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QStyle,
)


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
