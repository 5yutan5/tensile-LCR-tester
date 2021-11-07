from tester.AutoLab.widgets.dialog import CriticalErrorMessageBox
from PySide6.QtWidgets import QWidget
from tester.widgets.status import CustomStatusBar


class DeviceErrorMessageBox(CriticalErrorMessageBox):
    def __init__(self, text: str, parent: QWidget = None, statusbar: CustomStatusBar = None):
        super().__init__(text, parent)
        if statusbar is not None:
            statusbar.change_mode(statusbar.Mode.ERROR)


def test():
    import sys

    from tester.AutoLab.utils.qthelpers import create_qt_app

    app = create_qt_app()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
