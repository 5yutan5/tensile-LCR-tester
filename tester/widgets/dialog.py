from AutoLab.widgets.dialog import CriticalErrorMessageBox
from LCR_LinearStage.widgets.status import CustomStatusBar
from PyQt5.QtWidgets import QWidget


class DeviceErrorMessageBox(CriticalErrorMessageBox):
    def __init__(
        self, text: str, parent: QWidget = None, statusbar: CustomStatusBar = None
    ):
        super().__init__(text, parent)
        if statusbar is not None:
            statusbar.change_mode(statusbar.Mode.ERROR)


def test():
    import sys

    from AutoLab.utils.qthelpers import qapplication

    app = qapplication()
    sys.exit(app.exec())


if __name__ == "__main__":
    test()
