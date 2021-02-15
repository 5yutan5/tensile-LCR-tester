from dataclasses import dataclass
from typing import Any, Union

from AutoLab.widgets.wrapper_widgets import AHBoxLayout, ALabel, AVBoxLayout
from PySide6.QtCore import QEvent, Qt, Slot
from PySide6.QtGui import QMouseEvent, QPainter
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDoubleSpinBox,
    QLineEdit,
    QScrollArea,
    QSpinBox,
    QStyle,
    QStyleOption,
    QWidget,
)


@dataclass
class SettingProperty:
    title: str
    name: str
    description: str
    type: str
    default: Union[str, bool, int, float, None] = None
    enum: Union[list[Union[str, int]], None] = None
    enum_descriptions: Union[list[str], None] = None
    maximum: Union[int, float, None] = None
    minimum: Union[int, float, None] = None


class SettingLabel(ALabel):
    def __init__(self, text: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.setMinimumWidth(parent.width())
        self.adjustSize()
        self.setWordWrap(True)
        self.setText(text)


class SettingWidget(QWidget):
    def __init__(self, setting_property: SettingProperty, parent=None):
        super().__init__(parent=parent)
        self.setting_property = setting_property
        self.title = setting_property.title
        self.name = setting_property.name
        self.description = setting_property.description
        self.dynamic_widget: QWidget
        self.name_widget = SettingLabel(
            f"{self.title} > <strong>{self.name}</strong>", self
        )
        self.default_style = self.styleSheet()
        self.setup()

    def setup(self):
        self.setAutoFillBackground(True)
        if self.setting_property.type == "boolean":
            self.dynamic_widget = QCheckBox(self.description)
            if (default := self.setting_property.default) is not None:
                self.dynamic_widget.setCheckable(default)  # type: ignore
            v_layout = AVBoxLayout(self)
            v_layout.addWidget(self.name_widget)
            v_layout.addWidget(self.dynamic_widget)
            return
        if self.setting_property.type == "number":
            self.dynamic_widget = QDoubleSpinBox()
            self.dynamic_widget.setFixedWidth(150)
            if (default := self.setting_property.default) is not None:
                self.dynamic_widget.setValue(default)  # type: ignore
        elif self.setting_property.type == "integer":
            self.dynamic_widget = QSpinBox()
            self.dynamic_widget.setFixedWidth(150)
            if (default := self.setting_property.default) is not None:
                self.dynamic_widget.setValue(default)  # type: ignore
        elif self.setting_property.type == "string":
            self.dynamic_widget = QLineEdit()
            self.dynamic_widget.setFixedWidth(300)
            print(self.setting_property.default)
            if (default := self.setting_property.default) is not None:
                self.dynamic_widget.setText(default)  # type: ignore

        v_layout = AVBoxLayout(self)
        v_layout.addWidget(self.name_widget)
        v_layout.addWidget(SettingLabel(self.description, self))
        v_layout.addWidget(self.dynamic_widget)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.dynamic_widget.setFocus()
        return super().mousePressEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet(self.default_style)
        return super().leaveEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        self.setStyleSheet("background: #22303d")
        self.dynamic_widget.setStyleSheet("background: #19232D")
        return super().enterEvent(event)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        style = self.style()
        style.drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class SettingsManager(QDialog):
    def __init__(self, settings: dict[str, Any]):
        super().__init__()
        self.settings = settings
        self.searchbar = QLineEdit()
        self.dynamic_v_layout = AVBoxLayout()
        self.scroll_area = QScrollArea()
        self.setup()

    def setup(self) -> None:
        self.resize(450, 500)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.searchbar.textChanged.connect(self.update)  # type: ignore

        h_layout = AHBoxLayout()
        h_layout.addWidget(self.searchbar)

        for widget in self._create_setting_widgets(""):
            self.dynamic_v_layout.addWidget(widget)
        self.dynamic_v_layout.addStretch()

        widget = QWidget()
        widget.setLayout(self.dynamic_v_layout)
        self.scroll_area.setWidget(widget)
        v_layout = AVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.scroll_area)
        self.setLayout(v_layout)

    def _create_setting_widgets(self, filter: str) -> list[SettingWidget]:
        setting_widgets = []
        for title, setting_properties in self.settings.items():
            for name, setting_property in setting_properties.items():
                if not (
                    filter in title
                    or filter in name
                    or filter in setting_property["description"]
                ):
                    continue
                container = SettingProperty(
                    title=title,
                    name=name,
                    description=setting_property["description"],
                    type=setting_property["type"],
                    default=setting_property.get("default"),
                    enum=setting_property.get("enum"),
                    enum_descriptions=setting_property.get("enum description"),
                    minimum=setting_property.get("minimum"),
                    maximum=setting_property.get("maximum"),
                )
                setting_widgets.append(SettingWidget(container, self))
        return setting_widgets

    @Slot()  # type: ignore
    def update(self) -> None:
        self.dynamic_v_layout = AVBoxLayout()
        for widget in self._create_setting_widgets(self.searchbar.text()):
            self.dynamic_v_layout.addWidget(widget)
        self.dynamic_v_layout.addStretch()
        widget = QWidget()
        widget.setLayout(self.dynamic_v_layout)
        self.scroll_area.setWidget(widget)


def test_setting_widget():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app
    from PySide6.QtWidgets import QFormLayout

    app = create_qt_app()
    app.setStyleSheet(
        app.styleSheet() + "*{font-size: 17px; font-family: Consolas;}"
        "SettingWidget::hover{background: gray;}"
    )
    setting_container = SettingProperty(
        title="Test",
        name="setting1",
        description="This is test setting",
        type="integer",
    )
    setting_widget1 = SettingWidget(setting_container)
    setting_widget2 = SettingWidget(setting_container)
    f_layout = QFormLayout()
    f_layout.addRow(setting_widget1)
    f_layout.addRow(setting_widget2)
    widget = QWidget()
    widget.setLayout(f_layout)
    widget.show()
    sys.exit(app.exec_())


def test_settings_manager():
    import sys

    from AutoLab.utils.qthelpers import create_qt_app

    test_settings = {
        "Console": {
            "Maximum Number Of Line": {
                "description": "Control maximum number of lines",
                "type": "integer",
                "default": 100,
                "minimum": 1,
                "maximum": 100000,
            },
            "setting name test2": {
                "description": "This is test setting 2",
                "type": "integer",
                "default": 10,
                "number range": [1, 20],
            },
        },
        "Title_Test2": {
            "Connecting Speed": {
                "description": "Setting Serial Connecting Speed",
                "type": "string",
                "default": "Fast",
            },
            "setting name test2": {
                "description": "This is test setting 2",
                "type": "integer",
                "default": 10,
                "number range": [1, 20],
            },
        },
        "Stage Controller": {
            "Acceleration and Deceleration Time": {
                "description": "Time of Acceleration and Deceleration [msec]",
                "type": "integer",
                "default": 10,
                "minimum": 1,
                "maximum": 1000,
            },
            "Judge Rady Interval": {
                "description": "Judgment interval of stage controller preparation [msec]",
                "type": "integer",
                "default": 70,
                "minimum": 0,
                "maximum": 100,
            },
            "Minimum Speed": {
                "description": "Minimum Move Speed [μ/sec]",
                "type": "integer",
                "default": 500,
                "minimum": 1,
                "maximum": 50000,
            },
            "Speed": {
                "description": "Move Speed [μm/sec]",
                "type": "integer",
                "default": 10000,
                "minimum": 50000,
                "maximum": 1,
            },
        },
    }

    app = create_qt_app()
    app.setStyleSheet(
        app.styleSheet() + "*{font-size: 17px; font-family: Consolas;}"
        "SettingWidget::hover{background: gray;}"
    )
    settings_manager = SettingsManager(test_settings)
    settings_manager.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_settings_manager()
