from AutoLab.utils.icon_manager import IconName, icon
from AutoLab.utils.qthelpers import (add_qLabel, create_action,
                                     create_push_button, create_timer,
                                     create_tool_button,
                                     popup_exception_message)
from AutoLab.widgets.combobox import PortCombobox
from AutoLab.widgets.util import IntSlider
from LCR_LinearStage.device.hioki_lcrmeter import LCRMeterIM3536
from LCR_LinearStage.device.manager import DeviceStatus
from LCR_LinearStage.device.optoSigma_stage_controller import \
    StageControllerShot702
from LCR_LinearStage.widgets.dialog import DeviceErrorMessageBox
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtWidgets import (QButtonGroup, QComboBox, QDialog, QFormLayout,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QSizePolicy, QVBoxLayout, QWidget)
from serial import SerialException


class DeviceConnectingManager(QDialog):
    def __init__(
        self,
        parent: QWidget,
        lcrmeter: LCRMeterIM3536,
        lcrmeter_status: DeviceStatus,
        stage_controller: StageControllerShot702,
        stage_controller_status: DeviceStatus,
    ) -> None:
        super().__init__(parent=parent)
        self._lcrmeter = lcrmeter
        self._lcrmeter_status = lcrmeter_status
        self._stage_controller = stage_controller
        self._stage_controller_status = stage_controller_status

        self._lcr_combobox_port = PortCombobox(LCRMeterIM3536.PORT_FILTER)
        self._lcr_combobox_baudrate = QComboBox()
        self._lcr_t_button_connect = create_tool_button(is_text_beside_icon=True)
        # self._stage_combobox_port = PortCombobox(StageControllerShot702.PORT_FILTER)
        self._stage_combobox_port = PortCombobox('')
        self._stage_t_button_connect = create_tool_button(is_text_beside_icon=True)

        self._action_connect_lcr = create_action(
            self,
            text="Connect Port",
            icon=icon(IconName.ADD_CONNECTION),
            triggered=self._connect_lcr,
        )
        self._action_disconnect_lcr = create_action(
            self,
            text="Disconnect Port",
            icon=icon(IconName.DISCONNECT),
            triggered=self._disconnect_lcr
        )
        self._action_connect_stage_controller = create_action(
            self,
            text="Connect Port",
            icon=icon(IconName.ADD_CONNECTION),
            triggered=self._connect_stage_controller,
        )
        self._action_disconnect_stage_controller = create_action(
            self,
            text="Disconnect Port",
            icon=icon(IconName.DISCONNECT),
            triggered=self._disconnect_stage_controller
        )

        self._setup()

    def _setup(self):
        self._lcr_combobox_baudrate.addItems(LCRMeterIM3536.BAUDRATES)
        self._lcr_combobox_baudrate.setCurrentText(str(self._lcrmeter_status.baudrate))
        if (description := self._lcrmeter_status.description) is not None:
            self._lcr_combobox_port.setCurrentText(description)
        if (description := self._stage_controller_status.description) is not None:
            self._stage_combobox_port.setCurrentText(description)

        self._lcr_t_button_connect.setDefaultAction(
            self._action_disconnect_lcr
            if self._lcrmeter_status.is_connecting
            else self._action_connect_lcr
        )
        self._stage_t_button_connect.setDefaultAction(
            self._action_disconnect_stage_controller
            if self._stage_controller_status.is_connecting
            else self._action_connect_stage_controller
        )
        self._lcr_combobox_port.currentTextChanged.connect(self._lcrmeter_port_changed)
        self._stage_combobox_port.currentTextChanged.connect(
            self._stage_controller_port_changed
        )

        # setup layout
        f_layout_lcr = QFormLayout()
        f_layout_lcr.addRow("Port", self._lcr_combobox_port)
        f_layout_lcr.addRow("Baudrate", self._lcr_combobox_baudrate)
        f_layout_lcr.addWidget(self._lcr_t_button_connect)
        group_lcr = QGroupBox("LCRMeter")
        group_lcr.setLayout(f_layout_lcr)

        f_layout_stage = QFormLayout()
        f_layout_stage.addRow("Port    ", self._stage_combobox_port)
        f_layout_stage.addWidget(self._stage_t_button_connect)
        group_stage = QGroupBox("Linear Stage")
        group_stage.setLayout(f_layout_stage)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(group_lcr)
        v_layout.addWidget(group_stage)

        self.setMinimumWidth(500)

    @pyqtSlot()
    def _connect_lcr(self):
        try:
            self._lcrmeter.open(
                self._lcrmeter_status.port, self._lcrmeter_status.baudrate
            )
        except SerialException as e:
            DeviceErrorMessageBox(str(e), self).exec()
        else:
            self._lcr_t_button_connect.setDefaultAction(self._action_disconnect_lcr)
            self._lcrmeter_status.is_connecting = True

    @pyqtSlot()
    def _disconnect_lcr(self):
        try:
            self._lcrmeter.close()
        except SerialException as e:
            DeviceErrorMessageBox(str(e), self).exec()
        else:
            self._lcr_t_button_connect.setDefaultAction(self._action_connect_lcr)
            self._lcrmeter_status.is_connecting = False

    @pyqtSlot()
    def _connect_stage_controller(self):
        try:
            self._stage_controller.open(self._stage_controller_status.port)
        except SerialException as e:
            DeviceErrorMessageBox(str(e), self).exec()
        else:
            self._stage_t_button_connect.setDefaultAction(
                self._action_disconnect_stage_controller
            )
            self._stage_controller_status.is_connecting = True

    @pyqtSlot()
    def _disconnect_stage_controller(self):
        try:
            self._stage_controller.close()
        except SerialException as e:
            DeviceErrorMessageBox(str(e), self).exec()
        else:
            self._stage_t_button_connect.setDefaultAction(
                self._action_connect_stage_controller
            )
            self._stage_controller_status.is_connecting = False

    @pyqtSlot()
    def _lcrmeter_port_changed(self):
        port_info = self._lcr_combobox_port.get_current_port_info()
        if port_info is not None:
            self._lcrmeter_status.description = port_info.description
            self._lcrmeter_status.port = port_info.device

    @pyqtSlot()
    def _stage_controller_port_changed(self):
        port_info = self._stage_combobox_port.get_current_port_info()
        if port_info is not None:
            self._stage_controller_status.description = port_info.description
            self._stage_controller_status.port = port_info.device


class StageControlManager(QDialog):
    def __init__(
        self,
        controller: StageControllerShot702,
        controller_status: DeviceStatus,
        parent: QWidget = None
    ):
        super().__init__(parent=parent)
        self._controller = controller
        self._controller_status = controller_status
        self._lcd_position = QLabel()
        self._int_slider = IntSlider()
        self._t_button_up = create_tool_button(
            arrow_type=Qt.UpArrow,
            fixed_height=50,
            fixed_width=50,
            toggled=self.up_stage,
        )
        self._t_button_down = create_tool_button(
            arrow_type=Qt.DownArrow,
            fixed_height=50,
            fixed_width=50,
            toggled=self.down_stage,
        )
        self._t_button_stop = create_tool_button(
            fixed_width=50,
            fixed_height=50,
            icon=icon(IconName.STOP_STAGE),
            icon_size=QSize(48, 48),
            toggled=self.stop_stage,
        )
        self._p_button_fix_zero = create_push_button(
            clicked=self.fix_zero, text="Fix Zero"
        )
        self._p_button_move_machine_zero = create_push_button(
            clicked=self.move_to_machine_zero, text="Move Machine Zero-Point"
        )
        self._p_button_set_speed = create_push_button(
            clicked=self.set_stage_speed, fixed_width=100, text="Set"
        )

        # timer
        self.timer_measure_position = create_timer(
            parent=self, timeout=self.measure_position
        )

        # setup
        self._int_slider.set_range(1, 50000)
        button_group = QButtonGroup(self)
        button_group.addButton(self._t_button_up)
        button_group.addButton(self._t_button_stop)
        button_group.addButton(self._t_button_down)
        button_group.setExclusive(True)

        # setup layout
        v_layout_control = QVBoxLayout()
        v_layout_control.addWidget(self._t_button_up)
        v_layout_control.addWidget(self._t_button_stop)
        v_layout_control.addWidget(self._t_button_down)
        v_layout_control.setAlignment(Qt.AlignHCenter)
        group_control = QGroupBox("Control")
        group_control.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        group_control.setLayout(v_layout_control)

        h_layout_position = QHBoxLayout()
        h_layout_position.addWidget(add_qLabel(self._lcd_position, "μm"))
        group_position = QGroupBox("Current Position")
        group_position.setLayout(h_layout_position)

        v_layout_origin = QVBoxLayout()
        v_layout_origin.addWidget(self._p_button_fix_zero)
        v_layout_origin.addWidget(self._p_button_move_machine_zero)
        group_origin = QGroupBox("Origin")
        group_origin.setLayout(v_layout_origin)

        v_layout_speed = QVBoxLayout()
        v_layout_speed.addWidget(add_qLabel(self._int_slider, "μm/msec"))
        v_layout_speed.addWidget(self._p_button_set_speed, alignment=Qt.AlignRight)
        group_speed = QGroupBox("Speed Setting")
        group_speed.setLayout(v_layout_speed)

        g_layout = QGridLayout()
        g_layout.addWidget(group_control, 1, 1, 2, 1)
        g_layout.addWidget(group_position, 1, 2)
        g_layout.addWidget(group_origin, 2, 2)
        g_layout.addWidget(group_speed, 3, 1, 1, 2)
        self.setLayout(g_layout)

    @pyqtSlot(bool)
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def up_stage(self, is_checked) -> None:
        if is_checked:
            self._controller.jog(self._controller.DirectionMode.PLUS)
            self.timer_measure_position.start(60)

    @pyqtSlot(bool)
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def down_stage(self, is_checked) -> None:
        if is_checked:
            self._controller.jog(self._controller.DirectionMode.MINUS)
            self.timer_measure_position.start(60)

    @pyqtSlot(bool)
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def stop_stage(self, is_checked) -> None:
        if is_checked:
            self._controller.stop()
            self.timer_measure_position.start(60)

    @pyqtSlot()
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def move_to_machine_zero(self) -> None:
        self._controller.move_stage_to_zero()
        self.timer_measure_position.start(60)

    @pyqtSlot()
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def fix_zero(self) -> None:
        self._controller.fix_zero()
        self._lcd_position.setText(str(self._controller.get_position()))

    @pyqtSlot()
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def set_stage_speed(self) -> None:
        max_speed = self._int_slider.get_value()
        self._controller.set_stage_speed(
            max_speed, max_speed, 100, self._controller.SpeedMode.MOVE
        )
        self._controller.set_stage_speed(
            max_speed, max_speed, 100, self._controller.SpeedMode.RETURN_ORIGIN
        )

    @pyqtSlot()
    @popup_exception_message(DeviceErrorMessageBox, SerialException)
    def measure_position(self) -> None:
        self._lcd_position.setText(str(self._controller.get_position()))
        if self._controller.is_ready():
            self.timer_measure_position.stop()


def test():
    import sys

    from AutoLab.utils.qthelpers import qapplication

    app = qapplication()
    # stage_controller = StageControllerShot702()
    # jog_controller = StageControlDialog(stage_controller)
    # jog_controller.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test()
