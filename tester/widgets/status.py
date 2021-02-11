from enum import Enum, auto

import qdarkstyle
from AutoLab.widgets.action_handler import StatusBar
from PyQt5.QtWidgets import QMainWindow


class CustomStatusBar(StatusBar):
    class Mode(Enum):
        ENABLEMEASURE = auto()
        DISABLEMEASURE = auto()
        ERROR = auto()

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self._mode = CustomStatusBar.Mode.DISABLEMEASURE

    def current_mode(self) -> Mode:
        return self._mode

    def change_mode(self, mode: Mode):
        if mode is self.Mode.ENABLEMEASURE:
            self.setStyleSheet("background: green")
        elif mode is self.Mode.DISABLEMEASURE:
            self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))
        elif mode is self.Mode.ERROR:
            self.setStyleSheet("background: red")
        self._mode = mode
