from enum import Enum

from LCR_LinearStage.app.mode.state import CycleMode, LCRMode, ModeState, StepMode
from PyQt5.QtWidgets import QMainWindow


class ModeContext:
    class MODE(Enum):
        Step = StepMode
        Cycle = CycleMode
        LCR = LCRMode

    def __init__(self, mainwindow: QMainWindow):
        self._mode_state: ModeState
        self._mainwindow = mainwindow

    def change_mode(self, mode: MODE):
        self._mode_state = mode.value(self._mainwindow)
        self._mode_state.setup()
        self._mode_state.reconnect_slot()
