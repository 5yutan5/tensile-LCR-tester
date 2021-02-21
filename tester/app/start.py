import sys

from AutoLab.utils.qthelpers import create_qt_app
from AutoLab.utils.style_manager import add_style_sheet, load_style_sheet
from tester.app.mainwindow import MainWindow


def main():
    app = create_qt_app()
    style_sheet = load_style_sheet("dark_theme")
    add_style_sheet(app, style_sheet)
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
