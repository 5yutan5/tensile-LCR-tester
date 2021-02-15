from AutoLab.utils.qthelpers import add_unit, create_tool_button
from AutoLab.widgets.utility_widgets import IntSlider, PathLine
from AutoLab.widgets.wrapper_widgets import AHBoxLayout, AToolBar, AVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QMainWindow,
    QPlainTextEdit,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QWidget,
)
from tester.config.manager import Settings
from tester.widgets.combobox import IM3536ParameterCombobox
from tester.widgets.status import CustomStatusBar


class TabMain(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # member
        self.pathname_line = PathLine()
        self.checkbox_save_to_file = QCheckBox("Save to File")

        self.t_button_open_filedialog = create_tool_button(is_text_beside_icon=True)
        self.t_button_step_mode = create_tool_button(fixed_width=250)
        self.t_button_cycle_mode = create_tool_button(fixed_width=250)
        self.t_button_only_lcr_mode = create_tool_button(fixed_width=250)
        self.t_button_lcr_state = create_tool_button(fixed_width=250)
        self.spinbox_interval = QSpinBox()

        self.group_save = QGroupBox("Save")
        self.group_mode = QGroupBox("Mode")
        self.group_lcr_state = QGroupBox("LCR Meter")
        self.group_measure_interval = QGroupBox("Measurement Interval")

        # setup
        self.spinbox_interval.setRange(1, 100000)
        self.checkbox_save_to_file.setEnabled(False)

        # setup layout
        f_layout_save = QFormLayout()
        f_layout_save.addRow("File Path", self.pathname_line)
        f_layout_save.addWidget(self.t_button_open_filedialog)
        f_layout_save.addRow(self.checkbox_save_to_file)
        self.group_save.setLayout(f_layout_save)

        v_layout_mode = AVBoxLayout()
        v_layout_mode.addWidget(self.t_button_step_mode)
        v_layout_mode.addWidget(self.t_button_cycle_mode)
        v_layout_mode.addWidget(self.t_button_only_lcr_mode)
        v_layout_mode.setAlignment(Qt.AlignHCenter)
        self.group_mode.setLayout(v_layout_mode)

        v_layout_lcr_state = AVBoxLayout()
        v_layout_lcr_state.addWidget(self.t_button_lcr_state)
        v_layout_lcr_state.setAlignment(Qt.AlignHCenter)
        self.group_lcr_state.setLayout(v_layout_lcr_state)

        f_layout_repeat = QFormLayout()
        f_layout_repeat.addRow("Interval", add_unit(self.spinbox_interval, "msec"))
        self.group_measure_interval.setLayout(f_layout_repeat)

        v_layout = AVBoxLayout(self)
        v_layout.addWidget(self.group_save)
        v_layout.addWidget(self.group_mode)
        v_layout.addWidget(self.group_lcr_state)
        v_layout.addWidget(self.group_measure_interval)


class TabLCR(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # member
        self.combobox_parameter1 = IM3536ParameterCombobox()
        self.combobox_parameter2 = IM3536ParameterCombobox()
        self.combobox_parameter3 = IM3536ParameterCombobox()
        self.combobox_parameter4 = IM3536ParameterCombobox()
        self.spinbox_measurements_num = QSpinBox()
        self.checkbox_parmanent = QCheckBox("Parmanent Measurement")
        self.checkbox_acquire_monitor_data = QCheckBox(
            "Acquire Voltage/Current Monitor Values"
        )

        self.group_parameter = QGroupBox("Parameter")
        self.group_only_lcr = QGroupBox("Only LCR Meter Mode")
        self.group_option = QGroupBox("Option")

        # setup
        self.combobox_parameter1.setCurrentText("Rs   (Equivalent series resistance)")
        self.combobox_parameter1.set_none_disabled(True)
        self.spinbox_measurements_num.setRange(1, 1000000000)
        self.checkbox_acquire_monitor_data.setChecked(True)
        self.checkbox_parmanent.setChecked(True)
        self.spinbox_measurements_num.setEnabled(False)
        self.group_only_lcr.setEnabled(False)

        # stup layout
        f_layout_parameter = QFormLayout()
        f_layout_parameter.addRow("1", self.combobox_parameter1)
        f_layout_parameter.addRow("2", self.combobox_parameter2)
        f_layout_parameter.addRow("3", self.combobox_parameter3)
        f_layout_parameter.addRow("4", self.combobox_parameter4)
        self.group_parameter.setLayout(f_layout_parameter)

        f_layout_only_lcr = QFormLayout()
        f_layout_only_lcr.addRow(self.checkbox_parmanent)
        f_layout_only_lcr.addRow(
            "Number of Measurements", self.spinbox_measurements_num
        )
        self.group_only_lcr.setLayout(f_layout_only_lcr)

        f_layout_option = QFormLayout()
        f_layout_option.addRow(self.checkbox_acquire_monitor_data)
        self.group_option.setLayout(f_layout_option)

        v_layout = AVBoxLayout(self)
        v_layout.addWidget(self.group_parameter)
        v_layout.addWidget(self.group_only_lcr)
        v_layout.addWidget(self.group_option)


class TabStageStep(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.spinbox_distance = QSpinBox()
        self.spinbox_step_num = QSpinBox()
        self.int_slider = IntSlider()
        self.spinbox_stop_interval = QSpinBox()

        # setup
        self.spinbox_distance.setRange(1, 100000)
        self.spinbox_step_num.setRange(1, 100000)
        self.int_slider.range = 1, 50000
        self.spinbox_stop_interval.setRange(0, 10000)

        # setup layout
        f_layout = QFormLayout(self)
        f_layout.addRow("Displacement", add_unit(self.spinbox_distance, "μm"))
        f_layout.addRow("Number of Steps", add_unit(self.spinbox_step_num, "times"))
        f_layout.addRow("Speed", add_unit(self.int_slider, "μm/sec"))
        f_layout.addRow("Stop Interval", add_unit(self.spinbox_stop_interval, "msec"))


class TabStageCycle(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.spinbox_distance = QSpinBox()
        self.spinbox_cycle_num = QSpinBox()
        self.int_slider = IntSlider()
        self.spinbox_stop_interval = QSpinBox()

        # setup
        self.spinbox_distance.setRange(1, 100000)
        self.spinbox_cycle_num.setRange(1, 100000)
        self.int_slider.range = 1, 50000
        self.spinbox_stop_interval.setRange(0, 10000)

        # setup layout
        f_layout = QFormLayout(self)
        f_layout.addRow("Displacement", add_unit(self.spinbox_distance, "μm"))
        f_layout.addRow("Number of Cycle", add_unit(self.spinbox_cycle_num, "times"))
        f_layout.addRow("Speed", add_unit(self.int_slider, "μm/sec"))
        f_layout.addRow("Stop Interval", add_unit(self.spinbox_stop_interval, "msec"))


class MainWindowUI:
    def setup_ui(self, win: QMainWindow, settings: Settings) -> None:
        self.statusbar = CustomStatusBar(win)
        self.toolbar_dialog = AToolBar(win)
        self.toolbar_run = AToolBar(win)
        self.tab = QTabWidget()
        self.tab_main = TabMain()
        self.tab_lcr = TabLCR()
        self.tab_stage_step = TabStageStep()
        self.tab_stage_cycle = TabStageCycle()
        self.console = QPlainTextEdit()
        self.group_measurements_data = QGroupBox("Measurements Data")

        self.tab.addTab(self.tab_main, "Test")
        self.tab.addTab(self.tab_lcr, "LCR Meter")
        self.tab.addTab(self.tab_stage_step, "Stage Controller")
        self.tab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QPlainTextEdit.NoWrap)

        # setup settings
        self.console.setMaximumBlockCount(settings.console.maximum_number_of_line)
        self.tab_main.spinbox_interval.setValue(settings.main.measure_interval)
        self.tab_stage_step.int_slider.update_current_value(
            settings.stage_controller.maximum_speed
        )
        self.tab_stage_cycle.int_slider.update_current_value(
            settings.stage_controller.maximum_speed
        )

        # setup layout
        v_layout = AVBoxLayout()
        v_layout.addWidget(self.console)
        self.group_measurements_data.setLayout(v_layout)

        h_layout = AHBoxLayout()
        h_layout.addWidget(self.tab)
        h_layout.addWidget(self.group_measurements_data)
        central_widget = QWidget()
        central_widget.setLayout(h_layout)
        win.setCentralWidget(central_widget)


def test():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app
    from tester.config.manager import get_settings

    app = create_qt_app()
    win = QMainWindow()
    settings = get_settings()
    MainWindowUI().setup_ui(win, settings)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
