from enum import Enum, auto

from AutoLab.utils.icon_manager import IconNames, create_qicon
from AutoLab.widgets.status import StatusBar, StatusBarWidget
from PySide6.QtWidgets import QMainWindow


class MeasureModeStatus(StatusBarWidget):
    def __init__(self):
        super().__init__("Measure Mode")

    def change_cycle_mode(self):
        self.update_icon(create_qicon(IconNames.DYNAMIC_GROUP))
        self.update_tool_tip("Cycle Mode")

    def change_lcr_mode(self):
        self.update_icon(create_qicon(IconNames.DYNAMIC))
        self.update_tool_tip("Only LCR Mode")

    def change_step_mode(self):
        self.update_icon(create_qicon(IconNames.DYNAMIC_GROUP))
        self.update_tool_tip("Step Mode")


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
            self.setStyleSheet("")
        elif mode is self.Mode.ERROR:
            self.setStyleSheet("background: red")
        self._mode = mode
