# from LCR_LinearStage.app.mainwindow import MainWindow
from io import TextIOWrapper

from AutoLab.utils.icon_manager import IconName, icon
from AutoLab.utils.qthelpers import create_timer, reconnect_slot, sleep_nonblock_window
from LCR_LinearStage.device.hioki_lcrmeter import PARAMETER, LCRMeterIM3536
from LCR_LinearStage.device.optoSigma_stage_controller import StageControllerShot702
from LCR_LinearStage.widgets.dialog import DeviceErrorMessageBox
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from serial import SerialException
from serial.serialutil import PortNotOpenError


class MeasureHandler:
    def __init__(
        self,
        lcr_meter: LCRMeterIM3536,
        stage_controller: StageControllerShot702,
        time_increment: int,
        enable_time: bool = False,
        enable_lcr_measure: bool = False,
        enable_stage_measure: bool = False,
        enable_lcr_acquire_monitor_data: bool = False,
    ) -> None:
        self.lcr_meter = lcr_meter
        self.stage_controller = stage_controller
        self.time = 0
        self.time_increment = time_increment
        self.enable_time = enable_time
        self.enable_lcr_measure = enable_lcr_measure
        self.enable_stage_measure = enable_stage_measure
        self.enable_lcr_acquire_monitor_data = enable_lcr_acquire_monitor_data

    def create_header(
        self,
        lcr_param1: str = None,
        lcr_param2: str = None,
        lcr_param3: str = None,
        lcr_param4: str = None,
    ) -> str:
        header = ""
        if self.enable_time:
            header += "Time[msec],"
        if self.enable_stage_measure:
            header += "Position[μm],"
        if self.enable_lcr_measure:
            for param in (lcr_param1, lcr_param2, lcr_param3, lcr_param4):
                if param is not None:
                    header += f"{param},"
            if self.enable_lcr_acquire_monitor_data:
                header += "AC Vmoni, AC Imoni, DC Vmoni, DC Imoni"
        return header

    def measure(self) -> str:
        data = ""
        if self.enable_time:
            self.time += self.time_increment
            data += str(self.time)
        if self.enable_stage_measure:
            data += "," + str(self.stage_controller.get_position())
        if self.enable_lcr_measure:
            data += "," + self.lcr_meter.trigger()  # type: ignore
            if self.enable_lcr_acquire_monitor_data:
                data += "," + self.lcr_meter.get_monitor_values()
        return data


class ModeState(QObject):
    def __init__(self, mainwindow: QMainWindow) -> None:
        super().__init__(mainwindow)
        self.mainwindow = mainwindow
        self.timer_measure = create_timer(mainwindow)
        self.file_object: TextIOWrapper
        self.measure_handler: MeasureHandler

    def measure(self) -> None:
        pass

    def run(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def continue_run(self) -> None:
        self.timer_measure.enable_counter = False

    def stop(self) -> None:
        self.timer_measure.stop()
        self.mainwindow.action_running_state.setIcon(icon(IconName.STATUS_RUN))
        self.mainwindow.action_running_state.setText("Stopping")
        self.mainwindow.action_run.setEnabled(True)
        self.mainwindow.action_stop.setEnabled(False)
        self.mainwindow.action_continue.setEnabled(False)
        self.mainwindow.action_open_device_connecting_magager.setEnabled(True)
        try:
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                self.file_object.close()
        except Exception as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()

    def setup_lcr(self) -> None:
        settings_lcr = self.mainwindow.settings.lcr_meter
        tab_lcr = self.mainwindow.ui.tab_lcr
        self.mainwindow.lcrmeter.set_options(
            timeout=settings_lcr.timeout,
            display_monitor=True,
            measure_output_auto=True,
            speed=settings_lcr.communication_speed,
        )
        self.mainwindow.lcrmeter.set_parameters(
            param1=PARAMETER[tab_lcr.combobox_parameter1.currentText()],
            param2=PARAMETER[tab_lcr.combobox_parameter2.currentText()],
            param3=PARAMETER[tab_lcr.combobox_parameter3.currentText()],
            param4=PARAMETER[tab_lcr.combobox_parameter4.currentText()],
        )

    def reconnect_slot(self) -> None:
        reconnect_slot(self.mainwindow.action_run.triggered, self.run)
        reconnect_slot(self.mainwindow.action_stop.triggered, self.stop)
        reconnect_slot(self.mainwindow.action_continue.triggered, self.continue_run)


class StageMode(ModeState):
    def __init__(self, mainwindow: QMainWindow) -> None:
        super().__init__(mainwindow)
        self.timer_move_stage = create_timer(mainwindow)
        self.timer_measure.timeout.connect(self.measure)
        self.move_counter = 0

    @pyqtSlot()
    def measure(self) -> None:
        try:
            data = self.measure_handler.measure()
            self.mainwindow.ui.console.appendPlainText(data)
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                data += "\n"
                self.file_object.write(data)
        except (PortNotOpenError, SerialException) as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
            self.mainwindow.action_stop.trigger()

    def setup(self) -> None:
        self.mainwindow.action_measure_mode_state.setIcon(icon(IconName.DYNAMIC_GROUP))
        if self.mainwindow.lcrmeter_status.is_connecting:
            self.mainwindow.action_mode_lcr_state.setEnabled(True)
        else:
            self.mainwindow.action_mode_lcr_state.setChecked(False)

    @pyqtSlot()
    def stop(self) -> None:
        super().stop()
        self.timer_move_stage.stop()
        self.move_counter = 0
        try:
            self.mainwindow.stage_controller.stop()
        except (PortNotOpenError, SerialException) as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()


class StepMode(StageMode):
    def __init__(self, mainwindow: QMainWindow) -> None:
        super().__init__(mainwindow)
        self.timer_move_stage.timeout.connect(self._move_stage)

    @pyqtSlot()
    def _move_stage(self) -> None:
        try:
            tab_step = self.mainwindow.ui.tab_stage_step
            if self.mainwindow.stage_controller.is_ready():
                stop_interval = tab_step.spinbox_stop_interval.value()
                if not stop_interval == 0 and not self.move_counter == 0:
                    sleep_nonblock_window(stop_interval)
                self.move_counter += 1
                self.mainwindow.stage_controller.move_stage(
                    tab_step.spinbox_distance.value() * self.move_counter
                )
                if self.move_counter == tab_step.spinbox_step_num.value() + 1:
                    self.mainwindow.action_stop.trigger()
        except SerialException as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
            self.mainwindow.action_stop.trigger()

    @pyqtSlot()
    def run(self) -> None:
        settings_stage = self.mainwindow.settings.stage_controller
        tab_lcr = self.mainwindow.ui.tab_lcr
        try:
            if self.mainwindow.action_mode_lcr_state.isChecked():
                self.setup_lcr()
            self.mainwindow.stage_controller.initialize()
            self.mainwindow.stage_controller.set_stage_speed(
                settings_stage.minimum_speed,
                self.mainwindow.ui.tab_stage_step.int_slider.get_value(),
                settings_stage.acceleration_and_deceleration_time,
            )
            self.mainwindow.stage_controller.fix_zero()
            self.measure_handler = MeasureHandler(
                lcr_meter=self.mainwindow.lcrmeter,
                stage_controller=self.mainwindow.stage_controller,
                time_increment=self.mainwindow.ui.tab_main.spinbox_interval.value(),
                enable_time=True,
                enable_lcr_measure=self.mainwindow.ui.tab_main.t_button_lcr_state.isChecked(),
                enable_lcr_acquire_monitor_data=tab_lcr.checkbox_acquire_monitor_data.isChecked(),
                enable_stage_measure=True,
            )
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                self.file_object = open(
                    file=self.mainwindow.ui.tab_main.pathname_line.text(),
                    mode="w",
                    encoding="utf-8",
                )
                header = self.measure_handler.create_header(
                    lcr_param1=PARAMETER[tab_lcr.combobox_parameter1.currentText()],
                    lcr_param2=PARAMETER[tab_lcr.combobox_parameter2.currentText()],
                    lcr_param3=PARAMETER[tab_lcr.combobox_parameter3.currentText()],
                    lcr_param4=PARAMETER[tab_lcr.combobox_parameter4.currentText()],
                )
                self.file_object.write(header + "\n")
        except SerialException as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
        else:
            self.mainwindow.action_running_state.setIcon(icon(IconName.LOADING))
            self.mainwindow.action_running_state.setText("Running")
            self.mainwindow.ui.console.clear()
            self.timer_measure.enable_counter = True
            self.timer_measure.start(
                self.mainwindow.ui.tab_main.spinbox_interval.value()
            )
            self.timer_move_stage.start(settings_stage.judge_busy_interval)
            self.mainwindow.action_run.setEnabled(False)
            self.mainwindow.action_stop.setEnabled(True)
            self.mainwindow.action_open_device_connecting_magager.setEnabled(False)

    def setup(self) -> None:
        super().setup()
        self.mainwindow.ui.tab.removeTab(2)
        self.mainwindow.ui.tab.addTab(
            self.mainwindow.ui.tab_stage_step, "Stage Controller"
        )


class CycleMode(StageMode):
    def __init__(self, mainwindow: QMainWindow) -> None:
        super().__init__(mainwindow)
        self.timer_move_stage.timeout.connect(self._move_stage)

    @pyqtSlot()
    def _move_stage(self) -> None:
        try:
            tab_cycle = self.mainwindow.ui.tab_stage_cycle
            if self.mainwindow.stage_controller.is_ready():
                stop_interval = tab_cycle.spinbox_stop_interval.value()
                if not stop_interval == 0 and not self.move_counter == 0:
                    sleep_nonblock_window(stop_interval)
                self.move_counter += 1
                self.mainwindow.stage_controller.move_stage(
                    0
                    if self.move_counter & 1 == 0
                    else tab_cycle.spinbox_distance.value()
                )
                if self.move_counter == tab_cycle.spinbox_cycle_num.value() * 2 + 1:
                    self.mainwindow.action_stop.trigger()
        except SerialException as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
            self.mainwindow.action_stop.trigger()

    @pyqtSlot()
    def run(self) -> None:
        settings_stage = self.mainwindow.settings.stage_controller
        tab_lcr = self.mainwindow.ui.tab_lcr
        try:
            if self.mainwindow.action_mode_lcr_state.isChecked():
                self.setup_lcr()
            self.mainwindow.stage_controller.initialize()
            self.mainwindow.stage_controller.set_stage_speed(
                settings_stage.minimum_speed,
                self.mainwindow.ui.tab_stage_cycle.int_slider.get_value(),
                settings_stage.acceleration_and_deceleration_time,
            )
            self.mainwindow.stage_controller.fix_zero()
            self.measure_handler = MeasureHandler(
                lcr_meter=self.mainwindow.lcrmeter,
                stage_controller=self.mainwindow.stage_controller,
                time_increment=self.mainwindow.ui.tab_main.spinbox_interval.value(),
                enable_time=True,
                enable_lcr_measure=self.mainwindow.ui.tab_main.t_button_lcr_state.isChecked(),
                enable_lcr_acquire_monitor_data=tab_lcr.checkbox_acquire_monitor_data.isChecked(),
                enable_stage_measure=True,
            )
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                self.file_object = open(
                    file=self.mainwindow.ui.tab_main.pathname_line.text(),
                    mode="w",
                    encoding="utf-8",
                )
                header = self.measure_handler.create_header(
                    lcr_param1=PARAMETER[tab_lcr.combobox_parameter1.currentText()],
                    lcr_param2=PARAMETER[tab_lcr.combobox_parameter2.currentText()],
                    lcr_param3=PARAMETER[tab_lcr.combobox_parameter3.currentText()],
                    lcr_param4=PARAMETER[tab_lcr.combobox_parameter4.currentText()],
                )
                self.file_object.write(header + "\n")
        except SerialException as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
        else:
            self.mainwindow.action_running_state.setIcon(icon(IconName.LOADING))
            self.mainwindow.action_running_state.setText("Running")
            self.mainwindow.ui.console.clear()
            self.timer_measure.enable_counter = True
            self.timer_measure.start(
                self.mainwindow.ui.tab_main.spinbox_interval.value()
            )
            self.timer_move_stage.start(settings_stage.judge_busy_interval)
            self.mainwindow.action_run.setEnabled(False)
            self.mainwindow.action_stop.setEnabled(True)
            self.mainwindow.action_continue.setEnabled(True)
            self.mainwindow.action_open_device_connecting_magager.setEnabled(False)

    def setup(self) -> None:
        super().setup()
        self.mainwindow.ui.tab.removeTab(2)
        self.mainwindow.ui.tab.addTab(
            self.mainwindow.ui.tab_stage_cycle, "Stage Controller"
        )


class LCRMode(ModeState):
    def __init__(self, mainwindow: QMainWindow) -> None:
        super().__init__(mainwindow)
        self.timer_measure.timeout.connect(self.measure)

    @pyqtSlot()
    def measure(self) -> None:
        try:
            tab_lcr = self.mainwindow.ui.tab_lcr
            data = self.measure_handler.measure()
            self.mainwindow.ui.console.appendPlainText(data)
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                data += "\n"
                self.file_object.write(data)
            if self.timer_measure.counter == tab_lcr.spinbox_measurements_num.value():
                self.mainwindow.action_stop.trigger()
        except (PortNotOpenError, SerialException) as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
            self.mainwindow.action_stop.trigger()

    @pyqtSlot()
    def run(self) -> None:
        tab_lcr = self.mainwindow.ui.tab_lcr
        try:
            self.setup_lcr()
            self.measure_handler = MeasureHandler(
                lcr_meter=self.mainwindow.lcrmeter,
                stage_controller=self.mainwindow.stage_controller,
                time_increment=self.mainwindow.ui.tab_main.spinbox_interval.value(),
                enable_time=True,
                enable_lcr_measure=True,
                enable_lcr_acquire_monitor_data=tab_lcr.checkbox_acquire_monitor_data.isChecked(),
            )
            if self.mainwindow.ui.tab_main.checkbox_save_to_file.isChecked():
                self.file_object = open(
                    file=self.mainwindow.ui.tab_main.pathname_line.text(),
                    mode="w",
                    encoding="utf-8",
                )
                header = self.measure_handler.create_header(
                    lcr_param1=PARAMETER[tab_lcr.combobox_parameter1.currentText()],
                    lcr_param2=PARAMETER[tab_lcr.combobox_parameter2.currentText()],
                    lcr_param3=PARAMETER[tab_lcr.combobox_parameter3.currentText()],
                    lcr_param4=PARAMETER[tab_lcr.combobox_parameter4.currentText()],
                )
                self.file_object.write(header + "\n")
        except SerialException as e:
            DeviceErrorMessageBox(
                str(e), self.mainwindow, self.mainwindow.ui.statusbar
            ).exec()
        else:
            self.mainwindow.action_running_state.setIcon(icon(IconName.LOADING))
            self.mainwindow.action_running_state.setText("Running")
            self.mainwindow.ui.console.clear()
            if not self.mainwindow.ui.tab_lcr.checkbox_parmanent.isChecked():
                self.timer_measure.enable_counter = True
            else:
                self.timer_measure.enable_counter = False
            self.timer_measure.start(
                self.mainwindow.ui.tab_main.spinbox_interval.value()
            )
            self.mainwindow.action_run.setEnabled(False)
            self.mainwindow.action_stop.setEnabled(True)
            self.mainwindow.action_continue.setEnabled(True)
            self.mainwindow.action_open_device_connecting_magager.setEnabled(False)

    def setup(self) -> None:
        self.mainwindow.action_mode_lcr_state.setChecked(True)
        self.mainwindow.action_mode_lcr_state.setEnabled(False)
        self.mainwindow.action_measure_mode_state.setIcon(icon(IconName.DYNAMIC))
