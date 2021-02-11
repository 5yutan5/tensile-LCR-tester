from pathlib import Path

from AutoLab.utils.icon_manager import IconName, icon
from AutoLab.utils.qthelpers import create_action
from AutoLab.widgets.dialog import CSVSaveFileDialog
from AutoLab.widgets.status import CPUStatus, MemoryStatus
from LCR_LinearStage.app.mainwindow_ui import MainWindowUI
from LCR_LinearStage.app.mode.context import ModeContext
from LCR_LinearStage.config.manager import get_settings
from LCR_LinearStage.device.hioki_lcrmeter import LCRMeterIM3536
from LCR_LinearStage.device.manager import DeviceStatus
from LCR_LinearStage.device.optoSigma_stage_controller import \
    StageControllerShot702
from LCR_LinearStage.widgets.manager import (DeviceConnectingManager,
                                             StageControlManager)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QActionGroup, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI()
        self.settings = get_settings()
        self.lcrmeter = LCRMeterIM3536()
        self.stage_controller = StageControllerShot702()

        # device status
        self.lcrmeter_status = DeviceStatus(
            baudrate=self.settings.lcr_meter.baudrate,
            description=None,
            is_connecting=False,
            port=None,
        )
        self.stage_controller_status = DeviceStatus(
            baudrate=None, description=None, is_connecting=False, port=None
        )

        # action
        self.action_open_device_connecting_magager = create_action(
            self,
            text="Open Device Connecting Manager",
            icon=icon(IconName.ADD_BEHAVIOR),
            triggered=self.open_device_connectiong_manager,
        )
        self.action_open_control_dialog = create_action(
            self,
            text="Open Stage Control Manager",
            icon=icon(IconName.EXPAND_ARROW),
            triggered=lambda: StageControlManager(
                self.stage_controller, self.stage_controller_status, self
            ).exec(),
        )
        self.action_lcr_connect_state = create_action(
            self,
            text="LCRMeter Disconnecting",
            icon=icon(IconName.CONNECT_UNPLUGGED),
            triggered=self.popup_lcr_connect_menu,
            name="LCRMeter Connect State",
        )
        self.action_stage_connect_state = create_action(
            self,
            text="Stage Controller Distonnecting",
            icon=icon(IconName.CONNECT_UNPLUGGED),
            triggered=self.popup_stage_connect_menu,
            name="Stage Controller Connect State",
        )
        self.action_mode_step = create_action(
            self, text="Step Mode", toggled=self.change_measure_mode
        )
        self.action_mode_cycle = create_action(
            self, text="Cycle Mode", toggled=self.change_measure_mode
        )
        self.action_mode_only_lcr = create_action(
            self, text="Only LCR Meter", toggled=self.change_measure_mode
        )
        self.action_measure_mode_state = create_action(
            self,
            text="Measure Mode State",
            icon=icon(IconName.DYNAMIC),
            triggered=lambda: self.ui.statusbar.popup_actions(
                self.actiongroup_measure_mode.actions()
            ),
        )
        self.action_mode_lcr_state = create_action(
            self, text="LCR Meter ON", toggled=self.change_lcr_state
        )
        self.action_run = create_action(
            self,
            text="Run Only LCR Meter",
            icon=icon(IconName.RUN),
            enable=True,
            shortcut="F5",
        )
        self.action_stop = create_action(
            self,
            text="Stop",
            icon=icon(IconName.STOP),
            enable=False,
            shortcut="Shift+F5",
        )
        self.action_continue = create_action(
            self,
            text="Continue",
            icon=icon(IconName.CONTINUE),
            enable=False,
            shortcut="F10",
        )
        self.action_memory = create_action(self, text="Memory", name="Memory")
        self.action_cpu = create_action(self, text="CPU", name="CPU")
        self.action_running_state = create_action(
            self,
            text="Stopping",
            icon=icon(IconName.STATUS_RUN),
            triggered=lambda: self.ui.statusbar.popup_actions(
                self.actiongroup_play.actions()
            ),
            name="Running State",
        )
        self.action_open_filedialog = create_action(
            self,
            text="Open File Dialog",
            icon=icon(IconName.OPEN_FOLDER),
            triggered=self.open_filedialog,
        )

        # action group
        self.actiongroup_measure_mode = QActionGroup(self)
        self.actiongroup_play = QActionGroup(self)

        self.setup()

    def setup(self):
        self.ui.setup_ui(self, self.settings)
        self.setMinimumWidth(1100)
        self.move(50, 50)

        # tab test
        self.ui.tab_main.t_button_open_filedialog.setDefaultAction(
            self.action_open_filedialog
        )
        self.ui.tab_main.t_button_step_mode.setDefaultAction(self.action_mode_step)
        self.ui.tab_main.t_button_cycle_mode.setDefaultAction(self.action_mode_cycle)
        self.ui.tab_main.t_button_only_lcr_mode.setDefaultAction(
            self.action_mode_only_lcr
        )
        self.ui.tab_main.t_button_lcr_state.setDefaultAction(self.action_mode_lcr_state)

        # tab lcr
        self.ui.tab_lcr.checkbox_parmanent.stateChanged.connect(
            self.change_lcr_parmanent
        )

        # toolbar
        self.ui.toolbar_dialog.addActions(
            [
                self.action_open_device_connecting_magager,
                self.action_open_control_dialog,
            ]
        )
        self.ui.toolbar_run.addSeparator()
        self.ui.toolbar_run.addActions(
            [self.action_run, self.action_stop, self.action_continue]
        )

        # statusbar
        self.ui.statusbar.add_status(self.action_memory, MemoryStatus, "left")
        self.ui.statusbar.add_status(self.action_cpu, CPUStatus, "left")
        self.ui.statusbar.add_status(self.action_measure_mode_state)
        self.ui.statusbar.add_status(self.action_lcr_connect_state)
        self.ui.statusbar.add_status(self.action_stage_connect_state)
        self.ui.statusbar.add_status(self.action_running_state)

        # actiongroup
        self.actiongroup_measure_mode.addAction(self.action_mode_step)
        self.actiongroup_measure_mode.addAction(self.action_mode_cycle)
        self.actiongroup_measure_mode.addAction(self.action_mode_only_lcr)
        self.actiongroup_measure_mode.setExclusive(True)

        self.actiongroup_play.addAction(self.action_run)
        self.actiongroup_play.addAction(self.action_stop)
        self.actiongroup_play.addAction(self.action_continue)
        self.actiongroup_play.setEnabled(False)

        # select mode
        self.action_mode_step.setChecked(True)
        self.action_mode_lcr_state.setChecked(True)

    @pyqtSlot()
    def open_device_connectiong_manager(self):
        DeviceConnectingManager(
            self,
            lcrmeter=self.lcrmeter,
            lcrmeter_status=self.lcrmeter_status,
            stage_controller=self.stage_controller,
            stage_controller_status=self.stage_controller_status,
        ).exec()
        if self.ui.statusbar.current_mode() is self.ui.statusbar.Mode.ERROR:
            self.actiongroup_play.setEnabled(False)
            self.actiongroup_measure_mode.setEnabled(False)
            return
        if (
            self.lcrmeter_status.is_connecting
            and self.stage_controller_status.is_connecting
        ):
            self.action_lcr_connect_state.setIcon(icon(IconName.CONNECT_PLUGGED))
            self.action_stage_connect_state.setIcon(icon(IconName.CONNECT_PLUGGED))
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.action_lcr_connect_state.setText("LCRMeter Connecting")
            self.action_stage_connect_state.setText("Stage Controller Connecting")
            self.actiongroup_play.setEnabled(True)
            self.actiongroup_measure_mode.setEnabled(True)
            self.action_mode_lcr_state.setEnabled(True)
        elif self.lcrmeter_status.is_connecting:
            self.action_lcr_connect_state.setIcon(icon(IconName.CONNECT_PLUGGED))
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.action_lcr_connect_state.setText("LCRMeter Connecting")
            self.actiongroup_play.setEnabled(True)
            self.action_mode_only_lcr.setChecked(True)
            self.actiongroup_measure_mode.setEnabled(False)
        elif self.stage_controller_status.is_connecting:
            self.action_stage_connect_state.setIcon(icon(IconName.CONNECT_PLUGGED))
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.action_stage_connect_state.setText("Stage Controller Connecting")
            self.actiongroup_measure_mode.setEnabled(True)
            self.action_mode_only_lcr.setChecked(False)
            self.actiongroup_play.setEnabled(True)
            self.action_mode_lcr_state.setChecked(False)
            self.action_mode_lcr_state.setEnabled(False)
        else:
            self.action_lcr_connect_state.setIcon(icon(IconName.CONNECT_UNPLUGGED))
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.DISABLEMEASURE)
            self.action_lcr_connect_state.setText("LCRMeter Disconnecting")
            self.action_stage_connect_state.setText("Stage Controller Disconnecting")
            self.action_mode_only_lcr.setChecked(True)
            self.actiongroup_measure_mode.setEnabled(True)
            self.actiongroup_play.setEnabled(False)

    @pyqtSlot()
    def popup_lcr_connect_menu(self):
        self.ui.statusbar.popup_actions([self.action_open_device_connecting_magager])

    @pyqtSlot()
    def popup_stage_connect_menu(self):
        self.ui.statusbar.popup_actions([self.action_open_device_connecting_magager])

    @pyqtSlot()
    def open_filedialog(self):
        fileDialog = CSVSaveFileDialog()
        if not fileDialog.exec():
            return
        path = Path(fileDialog.selectedFiles()[0])
        self.ui.tab_main.pathname_line.set_path(str(path.absolute()))
        self.ui.tab_main.checkbox_save_to_file.setEnabled(True)
        self.ui.tab_main.checkbox_save_to_file.setChecked(True)

    @pyqtSlot(int)
    def change_lcr_parmanent(self, state: int) -> None:
        self.ui.tab_lcr.spinbox_measurements_num.setEnabled(
            False if state == Qt.Checked else True
        )

    @pyqtSlot(bool)
    def change_measure_mode(self, is_checked) -> None:
        mode_context = ModeContext(self)
        if self.sender() is self.action_mode_step and is_checked:
            mode_context.change_mode(mode_context.MODE.Step)
        elif self.sender() is self.action_mode_cycle and is_checked:
            mode_context.change_mode(mode_context.MODE.Cycle)
        elif self.sender() is self.action_mode_only_lcr and is_checked:
            mode_context.change_mode(mode_context.MODE.LCR)

    @pyqtSlot(bool)
    def change_lcr_state(self, is_checked: bool) -> None:
        if is_checked:
            self.action_mode_lcr_state.setText("LCR Meter ON")
            self.ui.tab_lcr.group_only_lcr.setEnabled(True)
        else:
            self.action_mode_lcr_state.setText("LCR Meter OFF")
            self.ui.tab_lcr.group_only_lcr.setEnabled(False)


def test():
    import sys

    import qdarkstyle
    from AutoLab.utils.qthelpers import qapplication

    app = qapplication()
    style = app.styleSheet()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5") + style)
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec())


if __name__ == "__main__":
    test()
