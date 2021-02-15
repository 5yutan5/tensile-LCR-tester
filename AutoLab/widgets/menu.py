from AutoLab.utils.icon_manager import IconNames, create_qicon
from AutoLab.widgets.wrapper_widgets import AMenu
from PySide6.QtWidgets import QWidget


class CheckMenu(AMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)

    def set_checked_dict(self, dic: dict[str, int]):
        for text, is_checked in dic.items():
            if is_checked:
                self.addAction(create_qicon(IconNames.CHECK_MARK), text)  # type: ignore
            else:
                self.addAction(text)  # type: ignore
