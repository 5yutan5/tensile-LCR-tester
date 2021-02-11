from DeviceController.hioki_lcrmeter import PARAMETER
from PyQt5.QtWidgets import QComboBox


class IM3536ParameterCombobox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(PARAMETER.keys())

    def set_none_disabled(self, is_enable: bool) -> None:
        if is_enable:
            current_text = self.currentText()
            self.clear()
            self.addItems(PARAMETER.keys())
            self.removeItem(0)
            self.setCurrentText(current_text)
