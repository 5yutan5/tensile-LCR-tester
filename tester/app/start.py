import sys

import qdarktheme

from tester.app.mainwindow import MainWindow
from tester.AutoLab.utils.qthelpers import create_qt_app


def main():
    app = create_qt_app()
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
