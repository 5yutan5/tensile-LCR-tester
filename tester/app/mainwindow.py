from pathlib import Path

from AutoLab.utils.icon_manager import IconNames, create_qicon
from AutoLab.utils.qthelpers import create_action
from AutoLab.widgets.dialog import CSVSaveFileDialog
from AutoLab.widgets.status import (
    CPUStatus,
    DeviceConnectStatus,
    MeasureStatus,
    MemoryStatus,
)
from DeviceController.hioki_lcrmeter import LCRMeterIM3536
from DeviceController.optoSigma_stage_controller import StageControllerShot702
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QMainWindow
from tester.app.mainwindow_ui import MainWindowUI
from tester.app.mode.context import ModeContext
from tester.config.manager import get_settings
from tester.device.manager import DeviceStatus
from tester.widgets.manager import DeviceConnectingManager, StageControlManager
from tester.widgets.status import MeasureModeStatus


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
            icon=create_qicon(IconNames.CABLE_WHITE),
            triggered=self.open_device_connectiong_manager,
        )
        self.action_open_control_dialog = create_action(
            self,
            text="Open Stage Control Manager",
            icon=create_qicon(IconNames.MOVE_WHITE),
            triggered=lambda: StageControlManager(
                self.stage_controller, self.stage_controller_status, self
            ).exec_(),
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
        self.action_mode_lcr_state = create_action(
            self, text="LCR Meter ON", toggled=self.change_lcr_state
        )
        self.action_run = create_action(
            self,
            text="Run Only LCR Meter",
            icon=create_qicon(IconNames.PLAY_ARROR_GREEN),
            enable=True,
            shortcut="F5",
        )
        self.action_stop = create_action(
            self,
            text="Stop",
            icon=create_qicon(IconNames.STOP_RED),
            enable=False,
            shortcut="Shift+F5",
        )
        self.action_continue = create_action(
            self,
            text="Continue",
            icon=create_qicon(IconNames.LOOP_WHITE),
            enable=False,
            shortcut="F10",
        )
        self.action_open_filedialog = create_action(
            self,
            text="Open File Dialog",
            icon=create_qicon(IconNames.FOLDER_OPEN_SKIN),
            triggered=self.open_filedialog,
        )

        # status bar widget
        self.status_widget_device_lcr = DeviceConnectStatus("LCR Meter")
        self.status_widget_device_stage = DeviceConnectStatus("Stage Controller")
        self.status_widget_measure = MeasureStatus()
        self.status_widget_measure_mode = MeasureModeStatus()

        # action group
        self.actiongroup_measure_mode = QActionGroup(self)
        self.actiongroup_play = QActionGroup(self)

        self.setup()

    def setup(self):
        self.ui.setup_ui(self, self.settings)
        self.resize(1100, 600)
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
        self.ui.tab_lcr.checkbox_parmanent.stateChanged.connect(  # type:ignore
            self.change_lcr_parmanent
        )

        # toolbar
        self.addToolBar(self.ui.toolbar_dialog)
        self.addToolBar(self.ui.toolbar_run)
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
        self.status_widget_device_lcr.sig_clicked.connect(  # type: ignore
            self.open_device_connectiong_manager
        )
        self.status_widget_device_stage.sig_clicked.connect(  # type: ignore
            self.open_device_connectiong_manager
        )
        self.status_widget_measure.sig_clicked.connect(  # type: ignore
            lambda: self.ui.statusbar.popup_actions(self.actiongroup_play.actions())
        )
        self.status_widget_measure_mode.sig_clicked.connect(  # type: ignore
            lambda: self.ui.statusbar.popup_actions(
                self.actiongroup_measure_mode.actions()
            ),
        )
        self.ui.statusbar.add_status(MemoryStatus(), self.ui.statusbar.Align.LEFT)
        self.ui.statusbar.add_status(CPUStatus(), self.ui.statusbar.Align.LEFT)
        self.ui.statusbar.add_status(self.status_widget_measure_mode)
        self.ui.statusbar.add_status(self.status_widget_device_lcr)
        self.ui.statusbar.add_status(self.status_widget_device_stage)
        self.ui.statusbar.add_status(self.status_widget_measure)

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
        self.status_widget_measure_mode.change_lcr_mode()

    @Slot()  # type: ignore
    def open_device_connectiong_manager(self):
        DeviceConnectingManager(
            self,
            lcrmeter=self.lcrmeter,
            lcrmeter_status=self.lcrmeter_status,
            stage_controller=self.stage_controller,
            stage_controller_status=self.stage_controller_status,
        ).exec_()
        if self.ui.statusbar.current_mode() is self.ui.statusbar.Mode.ERROR:
            self.actiongroup_play.setEnabled(False)
            self.actiongroup_measure_mode.setEnabled(False)
            return
        if (
            self.lcrmeter_status.is_connecting
            and self.stage_controller_status.is_connecting
        ):
            self.status_widget_device_lcr.change_connecting()
            self.status_widget_device_stage.change_connecting()
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.actiongroup_play.setEnabled(True)
            self.actiongroup_measure_mode.setEnabled(True)
            self.action_mode_lcr_state.setEnabled(True)
        elif self.lcrmeter_status.is_connecting:
            self.status_widget_device_lcr.change_connecting()
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.actiongroup_play.setEnabled(True)
            self.action_mode_only_lcr.setChecked(True)
            self.actiongroup_measure_mode.setEnabled(False)
        elif self.stage_controller_status.is_connecting:
            self.status_widget_device_stage.change_connecting()
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.ENABLEMEASURE)
            self.actiongroup_measure_mode.setEnabled(True)
            self.action_mode_only_lcr.setChecked(False)
            self.actiongroup_play.setEnabled(True)
            self.action_mode_lcr_state.setChecked(False)
            self.action_mode_lcr_state.setEnabled(False)
        else:
            self.status_widget_device_lcr.change_disconnecting()
            self.status_widget_device_stage.change_disconnecting()
            self.ui.statusbar.change_mode(self.ui.statusbar.Mode.DISABLEMEASURE)
            self.action_mode_only_lcr.setChecked(True)
            self.actiongroup_measure_mode.setEnabled(True)
            self.actiongroup_play.setEnabled(False)

    @Slot()  # type: ignore
    def open_filedialog(self):
        fileDialog = CSVSaveFileDialog()
        if not fileDialog.exec_():
            return
        path = Path(fileDialog.selectedFiles()[0])
        self.ui.tab_main.pathname_line.update_path(str(path.absolute()))
        self.ui.tab_main.checkbox_save_to_file.setEnabled(True)
        self.ui.tab_main.checkbox_save_to_file.setChecked(True)

    @Slot(int)  # type: ignore
    def change_lcr_parmanent(self, state: int) -> None:
        self.ui.tab_lcr.spinbox_measurements_num.setEnabled(
            False if state == Qt.Checked else True
        )

    @Slot(bool)  # type: ignore
    def change_measure_mode(self, is_checked) -> None:
        mode_context = ModeContext(self)
        if self.sender() is self.action_mode_step and is_checked:
            mode_context.change_mode(mode_context.MODE.Step)
        elif self.sender() is self.action_mode_cycle and is_checked:
            mode_context.change_mode(mode_context.MODE.Cycle)
        elif self.sender() is self.action_mode_only_lcr and is_checked:
            mode_context.change_mode(mode_context.MODE.LCR)

    @Slot(bool)  # type: ignore
    def change_lcr_state(self, is_checked: bool) -> None:
        if is_checked:
            self.action_mode_lcr_state.setText("LCR Meter ON")
            self.ui.tab_lcr.group_only_lcr.setEnabled(True)
        else:
            self.action_mode_lcr_state.setText("LCR Meter OFF")
            self.ui.tab_lcr.group_only_lcr.setEnabled(False)


def test():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app

    app = create_qt_app()
    win = MainWindow()
    win.show()
    win.action_open_device_connecting_magager.trigger()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
