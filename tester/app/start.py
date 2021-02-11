import sys

import qdarkstyle
from AutoLab.utils.qthelpers import qapplication
from LCR_LinearStage.app.mainwindow import MainWindow


def start():
    app = qapplication()
    style = app.styleSheet()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5") + style)
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec())


if __name__ == "__main__":
    start()
