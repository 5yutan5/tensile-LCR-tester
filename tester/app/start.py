import sys

import tester.app.style_rc
from AutoLab.utils.qthelpers import create_qt_app
from tester.app.mainwindow import MainWindow
from tester.app.style import darkstyle


def main():
    app = create_qt_app()
    app.setStyleSheet(darkstyle)
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
