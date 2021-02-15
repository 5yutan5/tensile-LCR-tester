from AutoLab.widgets.wrapper_widgets import AHBoxLayout
from PySide6.QtCore import QMargins, Qt, Slot
from PySide6.QtWidgets import QLineEdit, QSlider, QSpinBox, QWidget


class IntSlider(QWidget):
    """THe IntSlider class provides controller with a handle which can be pulled back
    and forth to change the **integer**.
    """

    def __init__(self):
        super().__init__()
        self._slider = QSlider(Qt.Horizontal)
        self._spinbox = QSpinBox()

        # setup signal
        self._slider.valueChanged.connect(self._value_changed)  # type: ignore
        self._spinbox.valueChanged.connect(self._value_changed)  # type: ignore

        # setup layout
        h_layout = AHBoxLayout(self)
        h_layout.addWidget(self._slider)
        h_layout.addWidget(self._spinbox)

    @property
    def current_value(self) -> int:
        return self._spinbox.value()

    @property
    def range(self) -> tuple[int, int]:
        return (self._slider.minimum(), self._slider.maximum())

    @range.setter
    def range(self, range: tuple[int, int]) -> None:
        self._slider.setRange(*range)
        self._spinbox.setRange(*range)

    @Slot(int)  # type: ignore
    def _value_changed(self, value: int) -> None:
        sender = self.sender()
        if sender is self._slider:
            self._spinbox.blockSignals(True)
            self._spinbox.setValue(value)
            self._spinbox.blockSignals(False)
        elif sender is self._spinbox:
            self._slider.blockSignals(True)
            self._slider.setValue(value)
            self._slider.blockSignals(False)

    def update_current_value(self, num: int) -> None:
        """Update current number of this widget. This method changes the display of the gui.

        Parameters
        ----------
        num : int
            Integer.
        """
        self._spinbox.setValue(num)


class PathLine(QWidget):
    """The PathLine class provides file or directory path display."""

    def __init__(self):
        super().__init__()
        self._line_edit = QLineEdit()
        self._line_edit.setReadOnly(True)

        # setup layout
        h_layout = AHBoxLayout(self)
        h_layout.addWidget(self._line_edit)
        h_layout.setContentsMargins(QMargins(0, 0, 0, 0))

    def update_path(self, path_name: str):
        """Update path of this widget. This method changes the display of the gui.

        Parameters
        ----------
        path_name : str
            The name of path.
        """
        self._line_edit.setText(path_name)
        # Moves the cursor position to the beginning of the line.
        self._line_edit.setCursorPosition(0)
