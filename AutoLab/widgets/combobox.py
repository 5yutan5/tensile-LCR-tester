from typing import Iterable, Union

from AutoLab.utils.system import search_ports
from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtWidgets import QComboBox
from serial.tools.list_ports_common import ListPortInfo


class CheckListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._check_dict = {}

    def data(self, index, role):
        """Cell content."""
        text, check = list(self._check_dict.items())[index.row()]
        if role == Qt.DisplayRole:
            return text
        elif role == Qt.CheckStateRole:
            return check

    def rowCount(self, index):
        """Dictionary row number."""
        return len(self._check_dict)

    def columnCount(self, index):
        """Dictionary column number."""
        return 1

    def flags(self, index):
        """Set editable flag."""
        return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled  # type:ignore

    def setData(self, index, value, role):
        """Cell content change"""
        if role != Qt.CheckStateRole:
            return
        key = list(self._check_dict.keys())[index.row()]
        self._check_dict[key] = Qt.Checked if value == Qt.Checked else Qt.Unchecked
        return True

    def set_texts(self, items: Iterable[str]):
        self._check_dict = {item: Qt.Checked for item in items}

    def get_checked_texts(self) -> list[str]:
        return [text for text, check in self._check_dict.items() if check == Qt.Checked]


class CheckCombobox(QComboBox):
    def __init__(self):
        super().__init__()
        self._model = CheckListModel()
        self.setModel(self._model)

    def set_texts(self, texts: Iterable[str]):
        self._model.set_texts(texts)
        self._model.layoutChanged.emit()  # type: ignore

    def get_checked_texts(self) -> list[str]:
        return self._model.get_checked_texts()


class FlexiblePopupCombobox(QComboBox):
    def showPopup(self) -> None:
        width = self.view().sizeHintForColumn(0)
        self.view().setMinimumWidth(width)
        super().showPopup()


class PortCombobox(FlexiblePopupCombobox):
    def __init__(self, filter: str = None):
        super().__init__()
        self._port_infos = []
        self._default_text = "Select Port"
        self._filter = "" if filter is None else filter
        self.addItem(self._default_text)

    @property
    def filter(self) -> str:
        return self._filter

    @filter.setter
    def filter(self, filter: str) -> None:
        self._filter = filter

    def get_current_port_info(self) -> Union[ListPortInfo, None]:
        return (
            None
            if len(self._port_infos) == 0
            else self._port_infos[self.currentIndex()]
        )

    def showPopup(self) -> None:
        self._port_infos.clear()
        self.clear()
        self._port_infos = search_ports(self._filter)
        if len(self._port_infos) == 0:
            self.addItem(self._default_text)
        else:
            self.addItems([str(port.description) for port in self._port_infos])
        super().showPopup()


def test():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app

    app = create_qt_app()
    check_combobox = CheckCombobox()
    check_combobox.show()
    texts = ["test1", "test2", "test3", "test4", "test5"]
    check_combobox.set_texts(texts)
    port_combobox = PortCombobox()
    port_combobox.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
