from AutoLab.widgets.wrapper_widgets import ATimer
from PySide6.QtCore import QObject, QTimerEvent


class CountTimer(ATimer):
    """The CounterTimer class The provides repetitive and single-shot timers. And this
    timer remembers the number of timeouts. You can check the `current count` property
    by checking the current count property. The count resets when the timer stops.

    Parameters
    ----------
    parent : QObject
        Parent of this Timer.

    Attributes
    ----------
    enable_counter : bool
        A state that indicates whether to count.
    """

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self._counter = 0
        self.enable_counter = True

    @property
    def current_count(self) -> int:
        return self._counter

    def _increment(self) -> None:
        """Increment `self._counter`, When `self.enable_count` is True."""
        if self.enable_counter:
            self._counter += 1
        else:
            pass

    def stop(self) -> None:
        """Override Qt method to reset `self._counter` to 0.
        """
        super().stop()
        self._counter = 0

    def timerEvent(self, event: QTimerEvent) -> None:
        """Override Qt method to increment `self._counter`.
        """
        self._increment()
        return super().timerEvent(event)
