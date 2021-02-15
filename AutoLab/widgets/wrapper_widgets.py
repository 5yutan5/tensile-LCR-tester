from PySide6.QtCore import QObject, Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMenu, QPushButton,
                               QToolBar, QToolButton, QVBoxLayout, QWidget)


class AAction(QAction):
    """AAction class wrapper to handle cross platform patches."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AHBoxLayout(QHBoxLayout):
    """AHBoxLayout class wrapper to handle cross platform patches"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)  # type: ignore


class ALabel(QLabel):
    """AHBoxLayout class wrapper to handle cross platform patches"""
    def __init__(self, text: str = None, parent: QWidget = None) -> None:
        super().__init__(text=text, parent=parent) # type: ignore


class AMenu(QMenu):
    """AMenu class wrapper to handle cross platform patches"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)  # type: ignore


class APushButton(QPushButton):
    """APushButton class wrapper to handle cross plat form patches."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor().setShape(Qt.PointingHandCursor)


class ATimer(QTimer):
    """ATimer class wrapper to handle cross platform patches."""

    def __init__(self, parent: QObject):
        super().__init__(parent=parent)


class AToolBar(QToolBar):
    """AToolBar class wrapper to handle cross platform patches."""

    def __init__(self, parent: QWidget, title: str = None) -> None:
        super().__init__(parent=parent)  # type: ignore
        self.setMovable(False)


class AToolButton(QToolButton):
    """AToolButton class wrapper to handle cross plat form patches."""

    def __init__(self):
        super().__init__()
        self.cursor().setShape(Qt.PointingHandCursor)


class AVBoxLayout(QVBoxLayout):
    """AVBoxLayout class wrapper to handle cross platform patches"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)  # type: ignore
