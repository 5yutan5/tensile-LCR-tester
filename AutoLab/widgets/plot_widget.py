import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication


class RealTimePlotWidget(pg.PlotWidget):
    _COLOR_CHART = {
        "black": "k",
        "blue": "b",
        "bright blue-green": "c",
        "bright pink": "m",
        "green": "g",
        "red": "r",
        "white": "w",
        "yellow": "y",
    }
    _STYLE_LABEL = {
        "font-size": "20px",
        "font-weight": "bold",
        "color": "dimgray",
        "font-family": "Arial",
    }
    _STYLE_CURVE = [
        _COLOR_CHART["red"],
        _COLOR_CHART["blue"],
        _COLOR_CHART["yellow"],
        _COLOR_CHART["bright pink"],
        _COLOR_CHART["green"],
    ]

    def __init__(self, y_range: int, y_label: str):
        super().__init__()
        self.x_range = 20
        self._curve_num = 1

        self.setXRange(0, self.x_range)
        self.setYRange(0, y_range)
        self.plotItem.setLabel("left", y_label, **self._STYLE_LABEL)
        self.plotItem.setLabel("bottom", "time[s]", **self._STYLE_LABEL)
        self.plotItem.hideButtons()
        self.plotItem.showGrid(x=True, y=True)
        self.plotItem.addLegend()
        self.plotItem.setMenuEnabled(False)
        self.plotItem.setMouseEnabled(False, False)
        self.enableMouse(False)
        self._createCurves()

    def _createCurves(self):
        for i in range(self._curve_num):
            pen = pg.mkPen(color=self._STYLE_CURVE[i], width=2)
            self.plot(pen=pen, name=f"ch{i+1}")

    def update(self, x_list: list[float], y_dict: dict[str, list[np.ndarray]]):
        for i, yData in enumerate(y_dict.values()):
            self.plotItem.getViewBox().addedItems[i].setData(x_list, yData)
        x_end = self.x_range if x_list[-1] < self.x_range else x_list[-1]
        self.setXRange(x_list[0], x_end)
        QApplication.processEvents()

    def clear_curve(self):
        self.plotItem.clear()
        self._createCurves()
        self.setXRange(0, self.x_range)


def test():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app

    app = create_qt_app()
    graph = RealTimePlotWidget(5, "Voltage")
    graph.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
