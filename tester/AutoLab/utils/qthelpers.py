import functools
from typing import Type

from PySide6.QtCore import SLOT, QEventLoop, QObject, QSize, Qt
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget

from tester.AutoLab.utils.style_manager import add_style_sheet, load_style_sheet
from tester.AutoLab.widgets.dialog import CriticalErrorMessageBox
from tester.AutoLab.widgets.timer import CountTimer
from tester.AutoLab.widgets.wrapper_widgets import AAction, AHBoxLayout, ALabel, APushButton, ATimer, AToolButton


def add_unit(widget: QWidget, text: str) -> QWidget:
    h_layout = AHBoxLayout()
    h_layout.addWidget(widget)
    h_layout.addWidget(ALabel(text))
    widget_with_label = QWidget()
    widget_with_label.setLayout(h_layout)
    return widget_with_label


def create_action(
    parent: QObject,
    text: str = None,
    icon: QIcon = None,
    toggled=None,
    triggered=None,
    name: str = None,
    shortcut: str = None,
    is_checked: bool = False,
    is_checkable: bool = False,
    enable: bool = True,
) -> AAction:
    action = AAction(parent)
    if text is not None:
        action.setText(text)
    if triggered is not None:
        action.triggered.connect(triggered)  # type: ignore
    if toggled is not None:
        action.toggled.connect(toggled)  # type: ignore
        action.setCheckable(True)
    if icon is not None:
        action.setIcon(icon)
    if name is not None:
        action.setObjectName(name)
    if shortcut is not None:
        action.setShortcut(QKeySequence(shortcut))  # type: ignore
    action.setChecked(is_checked)
    action.setCheckable(is_checkable)
    action.setEnabled(enable)
    return action


def create_push_button(
    clicked=None,
    fixed_width: int = None,
    fixed_height: int = None,
    icon: QIcon = None,
    text: str = None,
    toggled=None,
):
    button = APushButton()
    if clicked is not None:
        button.clicked.connect(clicked)  # type:ignore
    if fixed_height is not None:
        button.setFixedHeight(fixed_height)
    if fixed_width is not None:
        button.setFixedWidth(fixed_width)
    if icon is not None:
        button.setIcon(icon)
    if text is not None:
        button.setText(text)
    if toggled is not None:
        button.toggled.connect(toggled)  # type: ignore
        button.setCheckable(True)
    return button


def create_qt_app(app_name: str = None) -> QApplication:
    if app_name is None:
        app_name = "AutoLab"
    autolabApplication = QApplication
    app = autolabApplication.instance()
    if app is None:
        app = autolabApplication([app_name])
        app.setApplicationName(app_name)
        style_sheet = load_style_sheet("basic_style")
        add_style_sheet(app, style_sheet)
    return app  # type: ignore


def create_timer(parent, timeout=None, enable_counter: bool = False, timer_type: Qt.TimerType = None):
    timer = CountTimer(parent)
    if timeout is not None:
        timer.timeout.connect(timeout)  # type: ignore
    if timer_type is not None:
        timer.setTimerType(timer_type)
    timer.enable_counter = enable_counter
    return timer


def create_tool_button(  # noqa: C901
    arrow_type: Qt.ArrowType = None,
    fixed_height: int = None,
    fixed_width: int = None,
    icon: QIcon = None,
    icon_size: QSize = None,
    is_text_beside_icon: bool = False,
    text: str = None,
    toggled=None,
    triggered=None,
    object_name: str = None,
):
    button = AToolButton()
    if arrow_type is not None:
        button.setArrowType(arrow_type)
    if fixed_height is not None:
        button.setFixedHeight(fixed_height)
    if fixed_width is not None:
        button.setFixedWidth(fixed_width)
    if icon is not None:
        button.setIcon(icon)
    if icon_size is not None:
        button.setIconSize(icon_size)
    if is_text_beside_icon:
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    if text is not None:
        button.setText(text)
    if toggled is not None:
        button.toggled.connect(toggled)  # type: ignore
        button.setCheckable(True)
    if triggered is not None:
        button.triggered.connect(triggered)  # type: ignore
    if object_name is not None:
        button.setObjectName(object_name)
    return button


def popup_exception_message(
    message_box: Type[CriticalErrorMessageBox],
    exception: Type[Exception],
    parent: QWidget = None,
):
    def _popup_exception_message(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exception as e:
                message_box(text=str(e), parent=parent).exec_()

        return wrapper

    return _popup_exception_message


def reconnect_slot(signal, new_slot, old_slot=None) -> None:
    if old_slot is not None:
        signal.disconnect(old_slot)
    else:
        signal.disconnect()
    signal.connect(new_slot)


def sleep_nonblock_window(msec: int) -> None:
    loop = QEventLoop()
    ATimer.singleShot(msec, Qt.PreciseTimer, loop, SLOT("quit()"))  # type:ignore
    loop.exec_()
