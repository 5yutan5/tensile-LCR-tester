# -*- coding: utf-8 -*-
from AutoLab.widgets.wrapper_widgets import AHBoxLayout, ALabel
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLCDNumber, QTableView, QTableWidget, QWidget


class ListTableModel(QAbstractTableModel):
    def __init__(self, li):
        super().__init__()
        self._list = li
        self._header_index = 0

    @property
    def header_index(self):
        return self._header_index

    @header_index.setter
    def heade_index(self, index):
        self._header_index = index
        print(index)
        self.layoutChanged.emit()  # type: ignore

    @property
    def list_2d(self):
        return self._list

    @list_2d.setter
    def list_2d(self, li):
        self._list = li
        self.layoutChanged.emit()  # type: ignore

    def data(self, index, role):
        """Cell content."""
        if role == Qt.DisplayRole:
            return self._list[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            if self._is_header(index.row()):
                return QColor(Qt.darkGreen)
        elif role == Qt.ForegroundRole:
            if self._is_header(index.row()):
                return QColor(Qt.white)

    def rowCount(self, index):
        """List column number."""
        return len(self._list)

    def columnCount(self, index):
        """List column number."""
        return len(self._list[0])

    def headerData(self, section, orientation, role):
        """Set header data."""
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Vertical:
            return f"{section+1}(Header)" if self._is_header(section) else section + 1
        else:
            return section + 1

    def flags(self, index):
        """Set editable flag."""
        if self._is_lower_header(index.row()):
            return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def _is_header(self, row_index):
        return self._header_index == row_index

    def _is_lower_header(self, row_index):
        return row_index <= self._header_index

    def set_list(self, li):
        self._list = li
        self.layoutChanged.emit()  # type: ignore


class ListTableView(QTableView):
    selected = Signal(QModelIndex)

    def __init__(self, li=[[""] * 5] * 5):
        super().__init__()
        self.setModel(ListTableModel(li))
        self.setSortingEnabled(False)
        self.setShortcutEnabled(False)
        self.setCornerButtonEnabled(False)

    def selected_Area(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 0:
            return None
        rows = [index.row() + 1 for index in indexes]
        columns = [index.column() + 1 for index in indexes]
        return min(rows), max(rows), min(columns), max(columns)


class Indicator(QWidget):
    def __init__(self, unit):
        super().__init__()
        self.unit = ALabel(unit)
        self.lcd = QLCDNumber(6)
        self._initLayout()

    def _initLayout(self):
        self.setMinimumHeight(60)
        hLayout = AHBoxLayout()
        hLayout.addWidget(self.lcd)
        hLayout.addWidget(self.unit)
        self.setLayout(hLayout)

    def display(self, value: float):
        self.lcd.display(str(value))


class SensorDataTable(QTableWidget):
    h_header = ["Voltage", "Resistance"]
    VOLTAGE_INDEX = 0
    RESISTANCE_INDEX = 1

    def __init__(self, channel_num: int):
        super().__init__(channel_num, len(self.h_header))
        self.setHorizontalHeaderLabels(self.h_header)
        self.setVerticalHeaderLabels([f"ch{i+1}" for i in range(channel_num)])

        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                unit = "V" if column < 1 else "kΩ"
                self.setCellWidget(row, column, Indicator(unit))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.adjustSize()
        self.setFixedSize(self.width() + 13, self.maximumHeight())
        self.setCornerButtonEnabled(False)

    def update(self, voltages: list[float], resistances: list[float]):
        for i, (voltage, resistance) in enumerate(zip(voltages, resistances)):
            self.cellWidget(i, self.VOLTAGE_INDEX).display(str(voltage))
            self.cellWidget(i, self.RESISTANCE_INDEX).display(str(resistance))


def test():
    """Run ListTableView test"""
    import sys

    from AutoLab.utils.qthelpers import create_qt_app

    app = create_qt_app()
    table_view = ListTableView()
    table_view.resize(900, 300)
    table_view.show()
    sensor_data_table = SensorDataTable(5)
    sensor_data_table.update([1, 2, 3], [1, 2, 3])
    sensor_data_table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
