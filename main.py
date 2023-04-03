import sys

from PySide6.QtWidgets import QApplication

from robotck.gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
