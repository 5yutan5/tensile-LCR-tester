from enum import Enum, auto

from PySide6.QtCore import QMargins, QPoint, Signal
from PySide6.QtGui import QContextMenuEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QStatusBar, QWidget

from tester.AutoLab.utils.icon_manager import IconNames, create_qicon
from tester.AutoLab.utils.qthelpers import create_action, create_timer, create_tool_button
from tester.AutoLab.utils.system import cpu_usage, phymem_usage
from tester.AutoLab.widgets.wrapper_widgets import AAction, AHBoxLayout, AMenu


class StatusBarWidget(QWidget):
    """The StatusBarWidget class provides a status bar widget for use status bars.
    The permanent text is displayed on the left and the temporary text is displayed
    on the right.

    You can check the status change in real time by changing the temporary text
    regularly.

    Parameters
    ----------
    status_name : str
        The name of status. This name is used in the widget list that appears when
        you right-click on the status bar.
    tool_tip : str, default None
        The tool tip text when hover widget.
    is_text_beside_icon : bool, default False
        Whether to put icon beside text.

    Attributes
    ----------
    status_name : str
        The name of status.
    """

    sig_clicked = Signal()
    """This signal is emmitted when the widget is clicked.
    """

    def __init__(self, status_name: str, tool_tip: str = None, is_text_beside_icon: bool = False):
        super().__init__()
        self._tool_btn = create_tool_button(is_text_beside_icon=is_text_beside_icon)
        self._permanent_text = ""
        self._temporary_text = ""
        self.status_name = status_name
        self.update_tool_tip(status_name if tool_tip is None else tool_tip)
        # Make self.sig_clicked fire when clicked of ToolButton fires.
        self._tool_btn.clicked.connect(self.sig_clicked.emit)  # type: ignore

        # setup layout
        h_layout = AHBoxLayout(self)
        h_layout.addWidget(self._tool_btn)
        h_layout.setContentsMargins(QMargins(0, 0, 0, 0))

    def update_icon(self, icon: QIcon) -> None:
        """Update icon of this widget. This method changes the display of the gui.

        Parameters
        ----------
        icon : QIcon
            QIcon.
        """
        self._tool_btn.setIcon(icon)

    def update_permanent_text(self, text: str) -> None:
        """Update permanent text. This method changes the display of the gui.

        Parameters
        ----------
        text : str
            The permantent text. It should be text that describes what the status is.
        """
        self._permanent_text = text
        self._tool_btn.setText(self._permanent_text + self._temporary_text)

    def update_temporary_text(self, text: str) -> None:
        """Update temporary text. This method changes the display of the gui.

        Parameters
        ----------
        text : str
            Text of temporary text. It should be text that describes the current text.
        """
        self._temporary_text = text
        self._tool_btn.setText(self._permanent_text + self._temporary_text)

    def update_tool_tip(self, tip: str) -> None:
        """Update tool tip of this widget. This method changes the display of the gui.

        Parameters
        ----------
        tip : str
            A tooltip to display when hovering this widget.
        """
        self._tool_btn.setToolTip(tip)


class BaseTimerStatus(StatusBarWidget):
    """The StatusBarWidget class provides a status bar widget for use status bars.
    When the specified time elapses, the slot connected to timeout of Timer will fire.

    Parameters
    ----------
    status_name : str
        The name of the status. This name is used in the widget list that appears
        when you right-click on the status bar.
    tool_tip : str, default None
        The tool tip text when hover widget.
    interval : int, default 2000
        Unit is millisecond. The interval to update `temporary text`.

    See Also
    --------
    MemoryStatus : Class inherited by this class.
    CPUStatus : Class inherited by this class.
    """

    def __init__(self, status_name: str, tool_tip: str = None, interval: int = 2000):
        super().__init__(status_name, tool_tip)
        self._interval = interval
        self._timer = create_timer(self, timeout=self._update_status)
        self._timer.start(self._interval)

    def _update_status(self):
        """Update temporary text. This method changes the display of the gui."""
        self.update_temporary_text(self.get_text())

    def get_text(self) -> str:
        """Return formatted text value. This method is called by QTimer at the intervals
        specified and change the temporary text.

        Returns
        -------
        str
            The text to display in the status widget.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError


class MemoryStatus(BaseTimerStatus):
    """The MemoryStatus class provides a status bar widget for use status bars.
    It displays the memory usage while updating it regularly.

    Parameters
    ----------
    interval : int, default 2000
        Unit is millisecond. The interval to update `temporary text`.
    """

    def __init__(self, interval: int = 2000) -> None:
        super().__init__(status_name="Memory", interval=interval)
        self.update_permanent_text("Mem: ")

    def get_text(self) -> str:
        """Return the memory usage.

        Returns
        -------
        str
            The memory usage of the PC.
        """
        return f"{phymem_usage()}%"


class CPUStatus(BaseTimerStatus):
    """The CPUStatus class provides a status bar widget for use status bars.
    It displays the CPU usage while updating it regularly.

    Parameters
    ----------
    interval : int, default 2000
        Unit is millisecond. The interval to update `temporary text`.
    """

    def __init__(self, interval: int = 2000) -> None:
        super().__init__(status_name="CPU", interval=interval)
        self.update_permanent_text("CPU: ")

    def get_text(self) -> str:
        """Return the CPU usage.

        Returns
        -------
        str
            The CPU usage of the PC.
        """
        return f"{cpu_usage()}%"


class MeasureStatus(StatusBarWidget):
    """The MeasureStatus class provides a status bar widget for use status bars.
    It displays the measure statue.

    Switching modes changes this widget icon and tools.
    Executing `change_running ()` switch to running mode.
    Executing `change_stopping()` switch to stopping mode.
    """

    def __init__(self):
        super().__init__(status_name="Measure State")
        self.change_stopping()

    def change_running(self):
        """Switch to running mode of this widget."""
        self.update_icon(create_qicon(IconNames.PLAY_CIRCLE_GREEN))
        self.update_tool_tip("Running")

    def change_stopping(self):
        """Switch to stopping mode of this widget."""
        self.update_icon(create_qicon(IconNames.PAUSE_CIRCLE_RED))
        self.update_tool_tip("Stopping")


class DeviceConnectStatus(StatusBarWidget):
    """DeviceConnectStatus class provides a status bar widget for use status bars.
    It displays the device statue.

    Switching modes changes this widget icon and tools.
    Executing `change_connecting ()` switch to tonnecting mode.
    Executing `change_disconnecting()` switch to disconnecting mode.

    Parameters
    ----------
    device_name : str
        The name of device. Set the name of the device for which you want to view
        status.
    """

    def __init__(self, device_name: str):
        super().__init__(status_name=f"{device_name} Connect State")
        self._device_name = device_name
        self.change_disconnecting()

    def change_connecting(self):
        """Switch to connecting mode of this widget."""
        self.update_icon(create_qicon(IconNames.CONNECT_PLUGGED_WHITE))
        self.update_tool_tip(f"{self._device_name} Connecting")

    def change_disconnecting(self):
        """Switch to disconnecting mode of this widget."""
        self.update_icon(create_qicon(IconNames.CONNECT_UNPLUGGED_WHITE))
        self.update_tool_tip(f"{self._device_name} Disconnecting")


class StatusBar(QStatusBar):
    """The QStatusBar class provides a horizontal bar suitable for presenting status
    information. Right-clicking on the status bar will display a list of statuses that
    have been added to the status bar. Click on the displayed list to show or hide the
    status.

    Parameters
        ----------
        mainwindow : QMainWindow
            The main window that displays this status bar. This status bar automatically
            added to the mainwindow widget set in the argument.
    """

    class Align(Enum):
        LEFT = auto()
        RIGHT = auto()

    def __init__(self, mainwindow: QMainWindow):
        super().__init__(parent=mainwindow)
        # {key: value} = {status name: is shecked}
        self._checked_dict = {}
        # {key: value} = {status name: status}
        self._status_dict = {}
        self._mainwindow = mainwindow
        mainwindow.setStatusBar(self)

    def contextMenuEvent(self, event: QContextMenuEvent):
        """Override Qt method to pop up a list of statuses and change visible of
        status.
        """
        menu = AMenu(self)
        for text, is_checked in self._checked_dict.items():
            action = create_action(
                parent=self,
                text=text,
                is_checkable=True,
                is_checked=is_checked,
            )
            menu.addAction(action)  # type: ignore
        # Display popup menu on places of right-clicked.
        selected_action = menu.exec_(self.mapToGlobal(event.pos()))  # type: ignore
        if selected_action is not None:
            action_text = selected_action.text()
            is_check = self._checked_dict[action_text]
            self._checked_dict[action_text] = not is_check
            if is_check:
                self._status_dict[action_text].hide()
            else:
                self._status_dict[action_text].show()

    def add_status(
        self,
        status_bar_widget: StatusBarWidget,
        align: Align = Align.RIGHT,
    ):
        """Add status bar widget to the status bar. Set the status bar widget on either
        the right or left edge of the status bar.

        Parameters
        ----------
        status_bar_widget : StatusBarWidget
            The Status bar widget to add to the status bar.
        align : Align, default Align.RIGHT
            The display position of the status bar widget.
            * LEFT : Show status left side.
            * RIGHT : Show status right side.
        """
        if align == self.Align.RIGHT:
            self.addPermanentWidget(status_bar_widget)
        elif align == self.Align.LEFT:
            self.addWidget(status_bar_widget)
        self._checked_dict[status_bar_widget.status_name] = True
        self._status_dict[status_bar_widget.status_name] = status_bar_widget

    def popup_actions(self, actions: list[AAction]):
        """Popup argument actions. A popup appear at the bottom right of the window.

        Parameters
        ----------
        actions : list[AAction]
            Actions that pop up.
        """
        menu = AMenu(self)
        menu.addActions(actions)
        menu.adjustSize()
        x_pos_end_of_mainwindow = self._mainwindow.pos().x() + self._mainwindow.width()
        x = x_pos_end_of_mainwindow - menu.width()
        y_pos_end_of_mainwindow = self._mainwindow.pos().y() + self.pos().y()
        adjust_y = 30
        y = y_pos_end_of_mainwindow - menu.height() + adjust_y
        menu.exec_(QPoint(x, y))
