darkstyle = """
/* ---------------------------------------------------------------------------

    Created by the qtsass compiler v0.1.1

    The definitions are in the "qdarkstyle.qss._styles.scss" module

    WARNING! All changes made in this file will be lost!

--------------------------------------------------------------------------- */
/* QDarkStyleSheet -----------------------------------------------------------

This is the main style sheet, the palette has nine colors.

It is based on three selecting colors, three greyish (background) colors
plus three whitish (foreground) colors. Each set of widgets of the same
type have a header like this:

    ------------------
    GroupName --------
    ------------------

And each widget is separated with a header like this:

    QWidgetName ------

This makes more easy to find and change some css field. The basic
configuration is described bellow.

    BACKGROUND -----------

        Light   (unpressed)
        Normal  (border, disabled, pressed, checked, toolbars, menus)
        Dark    (background)

    FOREGROUND -----------

        Light   (texts/labels)
        Normal  (not used yet)
        Dark    (disabled texts)

    SELECTION ------------

        Light  (selection/hover/active)
        Normal (selected)
        Dark   (selected disabled)

If a stranger configuration is required because of a bugfix or anything
else, keep the comment on the line above so nobody changes it, including the
issue number.

*/
/*

See Qt documentation:

  - https://doc.qt.io/qt-5/stylesheet.html
  - https://doc.qt.io/qt-5/stylesheet-reference.html
  - https://doc.qt.io/qt-5/stylesheet-examples.html

--------------------------------------------------------------------------- */
/* QWidget ----------------------------------------------------------------

--------------------------------------------------------------------------- */
QWidget {
  background-color: #19232D;
  border: 0px solid #32414B;
  padding: 0px;
  color: #F0F0F0;
  selection-background-color: #1464A0;
  selection-color: #F0F0F0;
}

QWidget:disabled {
  background-color: #19232D;
  color: #787878;
  selection-background-color: #14506E;
  selection-color: #787878;
}

QWidget::item:selected {
  background-color: #1464A0;
}

QWidget::item:hover {
  background-color: #148CD2;
  color: #32414B;
}

/* QMainWindow ------------------------------------------------------------

This adjusts the splitter in the dock widget, not qsplitter
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmainwindow

--------------------------------------------------------------------------- */
QMainWindow::separator {
  background-color: #32414B;
  border: 0px solid #19232D;
  spacing: 0px;
  padding: 2px;
}

QMainWindow::separator:hover {
  background-color: #505F69;
  border: 0px solid #148CD2;
}

QMainWindow::separator:horizontal {
  width: 5px;
  margin-top: 2px;
  margin-bottom: 2px;
  image: url(":/qss_icons/rc/toolbar_separator_vertical.png");
}

QMainWindow::separator:vertical {
  height: 5px;
  margin-left: 2px;
  margin-right: 2px;
  image: url(":/qss_icons/rc/toolbar_separator_horizontal.png");
}

/* QToolTip ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtooltip

--------------------------------------------------------------------------- */
QToolTip {
  background-color: #148CD2;
  border: 1px solid #19232D;
  color: #19232D;
  /* Remove padding, for fix combo box tooltip */
  padding: 0px;
  /* Remove opacity, fix #174 - may need to use RGBA */
}

/* QStatusBar -------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qstatusbar

--------------------------------------------------------------------------- */
QStatusBar {
  border: 1px solid #32414B;
  /* Fixes Spyder #9120, #9121 */
  background: #32414B;
  /* Fixes #205, white vertical borders separating items */
}

QStatusBar::item {
  border: none;
}

QStatusBar QToolTip {
  background-color: #148CD2;
  border: 1px solid #19232D;
  color: #19232D;
  /* Remove padding, for fix combo box tooltip */
  padding: 0px;
  /* Reducing transparency to read better */
  opacity: 230;
}

QStatusBar QLabel {
  /* Fixes Spyder #9120, #9121 */
  background: transparent;
}

/* QCheckBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcheckbox

--------------------------------------------------------------------------- */
QCheckBox {
  background-color: #19232D;
  color: #F0F0F0;
  spacing: 4px;
  outline: none;
  padding-top: 4px;
  padding-bottom: 4px;
}

QCheckBox:focus {
  border: none;
}

QCheckBox QWidget:disabled {
  background-color: #19232D;
  color: #787878;
}

QCheckBox::indicator {
  margin-left: 4px;
  height: 16px;
  width: 16px;
}

QCheckBox::indicator:unchecked {
  image: url(":/qss_icons/rc/checkbox_unchecked.png");
}

QCheckBox::indicator:unchecked:hover, QCheckBox::indicator:unchecked:focus, QCheckBox::indicator:unchecked:pressed {
  border: none;
  image: url(":/qss_icons/rc/checkbox_unchecked_focus.png");
}

QCheckBox::indicator:unchecked:disabled {
  image: url(":/qss_icons/rc/checkbox_unchecked_disabled.png");
}

QCheckBox::indicator:checked {
  image: url(":/qss_icons/rc/checkbox_checked.png");
}

QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:focus, QCheckBox::indicator:checked:pressed {
  border: none;
  image: url(":/qss_icons/rc/checkbox_checked_focus.png");
}

QCheckBox::indicator:checked:disabled {
  image: url(":/qss_icons/rc/checkbox_checked_disabled.png");
}

QCheckBox::indicator:indeterminate {
  image: url(":/qss_icons/rc/checkbox_indeterminate.png");
}

QCheckBox::indicator:indeterminate:disabled {
  image: url(":/qss_icons/rc/checkbox_indeterminate_disabled.png");
}

QCheckBox::indicator:indeterminate:focus, QCheckBox::indicator:indeterminate:hover, QCheckBox::indicator:indeterminate:pressed {
  image: url(":/qss_icons/rc/checkbox_indeterminate_focus.png");
}

/* QGroupBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qgroupbox

--------------------------------------------------------------------------- */
QGroupBox {
  font-weight: bold;
  border: 1px solid #32414B;
  border-radius: 4px;
  padding: 4px;
  margin-top: 16px;
}

QGroupBox::title {
  subcontrol-origin: margin;
  subcontrol-position: top left;
  left: 3px;
  padding-left: 3px;
  padding-right: 5px;
  padding-top: 8px;
  padding-bottom: 16px;
}

QGroupBox::indicator {
  margin-left: 2px;
  height: 16px;
  width: 16px;
}

QGroupBox::indicator:unchecked {
  border: none;
  image: url(":/qss_icons/rc/checkbox_unchecked.png");
}

QGroupBox::indicator:unchecked:hover, QGroupBox::indicator:unchecked:focus, QGroupBox::indicator:unchecked:pressed {
  border: none;
  image: url(":/qss_icons/rc/checkbox_unchecked_focus.png");
}

QGroupBox::indicator:unchecked:disabled {
  image: url(":/qss_icons/rc/checkbox_unchecked_disabled.png");
}

QGroupBox::indicator:checked {
  border: none;
  image: url(":/qss_icons/rc/checkbox_checked.png");
}

QGroupBox::indicator:checked:hover, QGroupBox::indicator:checked:focus, QGroupBox::indicator:checked:pressed {
  border: none;
  image: url(":/qss_icons/rc/checkbox_checked_focus.png");
}

QGroupBox::indicator:checked:disabled {
  image: url(":/qss_icons/rc/checkbox_checked_disabled.png");
}

/* QRadioButton -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qradiobutton

--------------------------------------------------------------------------- */
QRadioButton {
  background-color: #19232D;
  color: #F0F0F0;
  spacing: 4px;
  padding: 0px;
  border: none;
  outline: none;
}

QRadioButton:focus {
  border: none;
}

QRadioButton:disabled {
  background-color: #19232D;
  color: #787878;
  border: none;
  outline: none;
}

QRadioButton QWidget {
  background-color: #19232D;
  color: #F0F0F0;
  spacing: 0px;
  padding: 0px;
  outline: none;
  border: none;
}

QRadioButton::indicator {
  border: none;
  outline: none;
  margin-left: 4px;
  height: 16px;
  width: 16px;
}

QRadioButton::indicator:unchecked {
  image: url(":/qss_icons/rc/radio_unchecked.png");
}

QRadioButton::indicator:unchecked:hover, QRadioButton::indicator:unchecked:focus, QRadioButton::indicator:unchecked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/rc/radio_unchecked_focus.png");
}

QRadioButton::indicator:unchecked:disabled {
  image: url(":/qss_icons/rc/radio_unchecked_disabled.png");
}

QRadioButton::indicator:checked {
  border: none;
  outline: none;
  image: url(":/qss_icons/rc/radio_checked.png");
}

QRadioButton::indicator:checked:hover, QRadioButton::indicator:checked:focus, QRadioButton::indicator:checked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/rc/radio_checked_focus.png");
}

QRadioButton::indicator:checked:disabled {
  outline: none;
  image: url(":/qss_icons/rc/radio_checked_disabled.png");
}

/* QMenuBar ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenubar

--------------------------------------------------------------------------- */
QMenuBar {
  background-color: #32414B;
  padding: 2px;
  border: 1px solid #19232D;
  color: #F0F0F0;
}

QMenuBar:focus {
  border: 1px solid #148CD2;
}

QMenuBar::item {
  background: transparent;
  padding: 4px;
}

QMenuBar::item:selected {
  padding: 4px;
  background: transparent;
  border: 0px solid #32414B;
}

QMenuBar::item:pressed {
  padding: 4px;
  border: 0px solid #32414B;
  background-color: #148CD2;
  color: #F0F0F0;
  margin-bottom: 0px;
  padding-bottom: 0px;
}

/* QMenu ------------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenu

--------------------------------------------------------------------------- */
QMenu {
  border: 0px solid #32414B;
  color: #F0F0F0;
  margin: 0px;
}

QMenu::separator {
  height: 1px;
  background-color: #505F69;
  color: #F0F0F0;
}

QMenu::icon {
  margin: 0px;
  padding-left: 8px;
}

QMenu::item {
  background-color: #32414B;
  padding: 4px 24px 4px 24px;
  /* Reserve space for selection border */
  border: 1px transparent #32414B;
}

QMenu::item:selected {
  color: #F0F0F0;
}

QMenu::indicator {
  width: 12px;
  height: 12px;
  padding-left: 6px;
  /* non-exclusive indicator = check box style indicator (see QActionGroup::setExclusive) */
  /* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
}

QMenu::indicator:non-exclusive:unchecked {
  image: url(":/qss_icons/rc/checkbox_unchecked.png");
}

QMenu::indicator:non-exclusive:unchecked:selected {
  image: url(":/qss_icons/rc/checkbox_unchecked_disabled.png");
}

QMenu::indicator:non-exclusive:checked {
  image: url(":/qss_icons/rc/checkbox_checked.png");
}

QMenu::indicator:non-exclusive:checked:selected {
  image: url(":/qss_icons/rc/checkbox_checked_disabled.png");
}

QMenu::indicator:exclusive:unchecked {
  image: url(":/qss_icons/rc/radio_unchecked.png");
}

QMenu::indicator:exclusive:unchecked:selected {
  image: url(":/qss_icons/rc/radio_unchecked_disabled.png");
}

QMenu::indicator:exclusive:checked {
  image: url(":/qss_icons/rc/radio_checked.png");
}

QMenu::indicator:exclusive:checked:selected {
  image: url(":/qss_icons/rc/radio_checked_disabled.png");
}

QMenu::right-arrow {
  margin: 5px;
  image: url(":/qss_icons/rc/arrow_right.png");
  height: 12px;
  width: 12px;
}

/* QAbstractItemView ------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcombobox

--------------------------------------------------------------------------- */
QAbstractItemView {
  alternate-background-color: #19232D;
  color: #F0F0F0;
  border: 1px solid #32414B;
  border-radius: 4px;
}

QAbstractItemView QLineEdit {
  padding: 2px;
}

/* QAbstractScrollArea ----------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qabstractscrollarea

--------------------------------------------------------------------------- */
QAbstractScrollArea {
  background-color: #19232D;
  border: 1px solid #32414B;
  border-radius: 4px;
  padding: 2px;
  /* fix #159 */
  min-height: 1.25em;
  /* fix #159 */
  color: #F0F0F0;
}

QAbstractScrollArea:disabled {
  color: #787878;
}

/* QScrollArea ------------------------------------------------------------

--------------------------------------------------------------------------- */
QScrollArea QWidget QWidget:disabled {
  background-color: #19232D;
}

/* QScrollBar -------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qscrollbar

--------------------------------------------------------------------------- */
QScrollBar:horizontal {
  height: 16px;
  margin: 2px 16px 2px 16px;
  border: 1px solid #32414B;
  border-radius: 4px;
  background-color: #19232D;
}

QScrollBar:vertical {
  background-color: #19232D;
  width: 16px;
  margin: 16px 2px 16px 2px;
  border: 1px solid #32414B;
  border-radius: 4px;
}

QScrollBar::handle:horizontal {
  background-color: #787878;
  border: 1px solid #32414B;
  border-radius: 4px;
  min-width: 8px;
}

QScrollBar::handle:horizontal:hover {
  background-color: #148CD2;
  border: 1px solid #148CD2;
  border-radius: 4px;
  min-width: 8px;
}

QScrollBar::handle:horizontal:focus {
  border: 1px solid #1464A0;
}

QScrollBar::handle:vertical {
  background-color: #787878;
  border: 1px solid #32414B;
  min-height: 8px;
  border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
  background-color: #148CD2;
  border: 1px solid #148CD2;
  border-radius: 4px;
  min-height: 8px;
}

QScrollBar::handle:vertical:focus {
  border: 1px solid #1464A0;
}

QScrollBar::add-line:horizontal {
  margin: 0px 0px 0px 0px;
  border-image: url(":/qss_icons/rc/arrow_right_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: right;
  subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
  border-image: url(":/qss_icons/rc/arrow_right.png");
  height: 12px;
  width: 12px;
  subcontrol-position: right;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/rc/arrow_down_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
  border-image: url(":/qss_icons/rc/arrow_down.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
  margin: 0px 3px 0px 3px;
  border-image: url(":/qss_icons/rc/arrow_left_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: left;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
  border-image: url(":/qss_icons/rc/arrow_left.png");
  height: 12px;
  width: 12px;
  subcontrol-position: left;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/rc/arrow_up_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on {
  border-image: url(":/qss_icons/rc/arrow_up.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
  background: none;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
  background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
  background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  background: none;
}

/* QTextEdit --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-specific-widgets

--------------------------------------------------------------------------- */
QTextEdit {
  background-color: #19232D;
  color: #F0F0F0;
  border-radius: 4px;
  border: 1px solid #32414B;
}

QTextEdit:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QTextEdit:focus {
  border: 1px solid #1464A0;
}

QTextEdit:selected {
  background: #1464A0;
  color: #32414B;
}

/* QPlainTextEdit ---------------------------------------------------------

--------------------------------------------------------------------------- */
QPlainTextEdit {
  background-color: #19232D;
  color: #F0F0F0;
  border-radius: 4px;
  border: 1px solid #32414B;
}

QPlainTextEdit:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QPlainTextEdit:focus {
  border: 1px solid #1464A0;
}

QPlainTextEdit:selected {
  background: #1464A0;
  color: #32414B;
}

/* QSizeGrip --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qsizegrip

--------------------------------------------------------------------------- */
QSizeGrip {
  background: transparent;
  width: 12px;
  height: 12px;
  image: url(":/qss_icons/rc/window_grip.png");
}

/* QStackedWidget ---------------------------------------------------------

--------------------------------------------------------------------------- */
QStackedWidget {
  padding: 2px;
  border: 1px solid #32414B;
  border: 1px solid #19232D;
}

/* QToolBar ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbar

--------------------------------------------------------------------------- */
QToolBar {
  background-color: #32414B;
  border-bottom: 1px solid #19232D;
  padding: 2px;
  font-weight: bold;
  spacing: 2px;
}

QToolBar QToolButton {
  background-color: #32414B;
  border: 1px solid #32414B;
}

QToolBar QToolButton:hover {
  border: 1px solid #148CD2;
}

QToolBar QToolButton:checked {
  border: 1px solid #19232D;
  background-color: #19232D;
}

QToolBar QToolButton:checked:hover {
  border: 1px solid #148CD2;
}

QToolBar::handle:horizontal {
  width: 16px;
  image: url(":/qss_icons/rc/toolbar_move_horizontal.png");
}

QToolBar::handle:vertical {
  height: 16px;
  image: url(":/qss_icons/rc/toolbar_move_vertical.png");
}

QToolBar::separator:horizontal {
  width: 16px;
  image: url(":/qss_icons/rc/toolbar_separator_horizontal.png");
}

QToolBar::separator:vertical {
  height: 16px;
  image: url(":/qss_icons/rc/toolbar_separator_vertical.png");
}

QToolButton#qt_toolbar_ext_button {
  background: #32414B;
  border: 0px;
  color: #F0F0F0;
  image: url(":/qss_icons/rc/arrow_right.png");
}

/* QAbstractSpinBox -------------------------------------------------------

--------------------------------------------------------------------------- */
QAbstractSpinBox {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  /* This fixes 103, 111 */
  padding-top: 2px;
  /* This fixes 103, 111 */
  padding-bottom: 2px;
  padding-left: 4px;
  padding-right: 4px;
  border-radius: 4px;
  /* min-width: 5px; removed to fix 109 */
}

QAbstractSpinBox:up-button {
  background-color: transparent #19232D;
  subcontrol-origin: border;
  subcontrol-position: top right;
  border-left: 1px solid #32414B;
  border-bottom: 1px solid #32414B;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin: 1px;
  width: 12px;
  margin-bottom: -1px;
}

QAbstractSpinBox::up-arrow, QAbstractSpinBox::up-arrow:disabled, QAbstractSpinBox::up-arrow:off {
  image: url(":/qss_icons/rc/arrow_up_disabled.png");
  height: 8px;
  width: 8px;
}

QAbstractSpinBox::up-arrow:hover {
  image: url(":/qss_icons/rc/arrow_up.png");
}

QAbstractSpinBox:down-button {
  background-color: transparent #19232D;
  subcontrol-origin: border;
  subcontrol-position: bottom right;
  border-left: 1px solid #32414B;
  border-top: 1px solid #32414B;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin: 1px;
  width: 12px;
  margin-top: -1px;
}

QAbstractSpinBox::down-arrow, QAbstractSpinBox::down-arrow:disabled, QAbstractSpinBox::down-arrow:off {
  image: url(":/qss_icons/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QAbstractSpinBox::down-arrow:hover {
  image: url(":/qss_icons/rc/arrow_down.png");
}

QAbstractSpinBox:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QAbstractSpinBox:focus {
  border: 1px solid #1464A0;
}

QAbstractSpinBox:selected {
  background: #1464A0;
  color: #32414B;
}

/* ------------------------------------------------------------------------ */
/* DISPLAYS --------------------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QLabel -----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qframe

--------------------------------------------------------------------------- */
QLabel {
  background-color: #19232D;
  border: 0px solid #32414B;
  padding: 2px;
  margin: 0px;
  color: #F0F0F0;
}

QLabel:disabled {
  background-color: #19232D;
  border: 0px solid #32414B;
  color: #787878;
}

/* QTextBrowser -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qabstractscrollarea

--------------------------------------------------------------------------- */
QTextBrowser {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-radius: 4px;
}

QTextBrowser:disabled {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #787878;
  border-radius: 4px;
}

QTextBrowser:hover, QTextBrowser:!hover, QTextBrowser:selected, QTextBrowser:pressed {
  border: 1px solid #32414B;
}

/* QGraphicsView ----------------------------------------------------------

--------------------------------------------------------------------------- */
QGraphicsView {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-radius: 4px;
}

QGraphicsView:disabled {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #787878;
  border-radius: 4px;
}

QGraphicsView:hover, QGraphicsView:!hover, QGraphicsView:selected, QGraphicsView:pressed {
  border: 1px solid #32414B;
}

/* QCalendarWidget --------------------------------------------------------

--------------------------------------------------------------------------- */
QCalendarWidget {
  border: 1px solid #32414B;
  border-radius: 4px;
}

QCalendarWidget:disabled {
  background-color: #19232D;
  color: #787878;
}

/* QLCDNumber -------------------------------------------------------------

--------------------------------------------------------------------------- */
QLCDNumber {
  background-color: #19232D;
  color: #F0F0F0;
}

QLCDNumber:disabled {
  background-color: #19232D;
  color: #787878;
}

/* QProgressBar -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qprogressbar

--------------------------------------------------------------------------- */
QProgressBar {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-radius: 4px;
  text-align: center;
}

QProgressBar:disabled {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #787878;
  border-radius: 4px;
  text-align: center;
}

QProgressBar::chunk {
  background-color: #1464A0;
  color: #19232D;
  border-radius: 4px;
}

QProgressBar::chunk:disabled {
  background-color: #14506E;
  color: #787878;
  border-radius: 4px;
}

/* ------------------------------------------------------------------------ */
/* BUTTONS ---------------------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QPushButton ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qpushbutton

--------------------------------------------------------------------------- */
QPushButton {
  background-color: #505F69;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-radius: 4px;
  padding: 3px;
  outline: none;
  /* Issue #194 - Special case of QPushButton inside dialogs, for better UI */
  min-width: 80px;
}

QPushButton:disabled {
  background-color: #32414B;
  border: 1px solid #32414B;
  color: #787878;
  border-radius: 4px;
  padding: 3px;
}

QPushButton:checked {
  background-color: #32414B;
  border: 1px solid #32414B;
  border-radius: 4px;
  padding: 3px;
  outline: none;
}

QPushButton:checked:disabled {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #787878;
  border-radius: 4px;
  padding: 3px;
  outline: none;
}

QPushButton:checked:selected {
  background: #1464A0;
  color: #32414B;
}

QPushButton::menu-indicator {
  subcontrol-origin: padding;
  subcontrol-position: bottom right;
  bottom: 4px;
}

QPushButton:pressed {
  background-color: #19232D;
  border: 1px solid #19232D;
}

QPushButton:pressed:hover {
  border: 1px solid #148CD2;
}

QPushButton:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QPushButton:selected {
  background: #1464A0;
  color: #32414B;
}

QPushButton:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QPushButton:focus {
  border: 1px solid #1464A0;
}

/* QToolButton ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbutton

--------------------------------------------------------------------------- */
QToolButton {
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 4px;
  margin: 0px;
  padding: 2px;
  /* The subcontrols below are used only in the DelayedPopup mode */
  /* The subcontrols below are used only in the MenuButtonPopup mode */
  /* The subcontrol below is used only in the InstantPopup or DelayedPopup mode */
}

QToolButton:checked {
  background-color: transparent;
  border: 1px solid #1464A0;
}

QToolButton:checked:disabled {
  border: 1px solid #14506E;
}

QToolButton:pressed {
  margin: 1px;
  background-color: transparent;
  border: 1px solid #1464A0;
}

QToolButton:disabled {
  border: none;
}

QToolButton:hover {
  border: 1px solid #148CD2;
}

QToolButton[popupMode="0"] {
  /* Only for DelayedPopup */
  padding-right: 2px;
}

QToolButton[popupMode="1"] {
  /* Only for MenuButtonPopup */
  padding-right: 20px;
}

QToolButton[popupMode="1"]::menu-button {
  border: none;
}

QToolButton[popupMode="1"]::menu-button:hover {
  border: none;
  border-left: 1px solid #148CD2;
  border-radius: 0;
}

QToolButton[popupMode="2"] {
  /* Only for InstantPopup */
  padding-right: 2px;
}

QToolButton::menu-button {
  padding: 2px;
  border-radius: 4px;
  border: 1px solid #32414B;
  width: 12px;
  outline: none;
}

QToolButton::menu-button:hover {
  border: 1px solid #148CD2;
}

QToolButton::menu-button:checked:hover {
  border: 1px solid #148CD2;
}

QToolButton::menu-indicator {
  image: url(":/qss_icons/rc/arrow_down.png");
  height: 8px;
  width: 8px;
  top: 0;
  /* Exclude a shift for better image */
  left: -2px;
  /* Shift it a bit */
}

QToolButton::menu-arrow {
  image: url(":/qss_icons/rc/arrow_down.png");
  height: 8px;
  width: 8px;
}

QToolButton::menu-arrow:hover {
  image: url(":/qss_icons/rc/arrow_down_focus.png");
}

/* QCommandLinkButton -----------------------------------------------------

--------------------------------------------------------------------------- */
QCommandLinkButton {
  background-color: transparent;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-radius: 4px;
  padding: 0px;
  margin: 0px;
}

QCommandLinkButton:disabled {
  background-color: transparent;
  color: #787878;
}

/* ------------------------------------------------------------------------ */
/* INPUTS - NO FIELDS ----------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QComboBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcombobox

--------------------------------------------------------------------------- */
QComboBox {
  border: 1px solid #32414B;
  border-radius: 4px;
  selection-background-color: #1464A0;
  padding-left: 4px;
  padding-right: 36px;
  /* 4 + 16*2 See scrollbar size */
  /* Fixes #103, #111 */
  min-height: 1.5em;
  /* padding-top: 2px;     removed to fix #132 */
  /* padding-bottom: 2px;  removed to fix #132 */
  /* min-width: 75px;      removed to fix #109 */
  /* Needed to remove indicator - fix #132 */
}

QComboBox QAbstractItemView {
  border: 1px solid #32414B;
  border-radius: 0;
  background-color: #19232D;
  selection-background-color: #1464A0;
}

QComboBox QAbstractItemView:hover {
  background-color: #19232D;
  color: #F0F0F0;
}

QComboBox QAbstractItemView:selected {
  background: #1464A0;
  color: #32414B;
}

QComboBox QAbstractItemView:alternate {
  background: #19232D;
}

QComboBox:disabled {
  background-color: #19232D;
  color: #787878;
}

QComboBox:hover {
  border: 1px solid #148CD2;
}

QComboBox:focus {
  border: 1px solid #1464A0;
}

QComboBox:on {
  selection-background-color: #1464A0;
}

QComboBox::indicator {
  border: none;
  border-radius: 0;
  background-color: transparent;
  selection-background-color: transparent;
  color: transparent;
  selection-color: transparent;
  /* Needed to remove indicator - fix #132 */
}

QComboBox::indicator:alternate {
  background: #19232D;
}

QComboBox::item:alternate {
  background: #19232D;
}

QComboBox::item:checked {
  font-weight: bold;
}

QComboBox::item:selected {
  border: 0px solid transparent;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 12px;
  border-left: 1px solid #32414B;
}

QComboBox::down-arrow {
  image: url(":/qss_icons/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QComboBox::down-arrow:on, QComboBox::down-arrow:hover, QComboBox::down-arrow:focus {
  image: url(":/qss_icons/rc/arrow_down.png");
}

/* QSlider ----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qslider

--------------------------------------------------------------------------- */
QSlider:disabled {
  background: #19232D;
}

QSlider:focus {
  border: none;
}

QSlider::groove:horizontal {
  background: #32414B;
  border: 1px solid #32414B;
  height: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::groove:vertical {
  background: #32414B;
  border: 1px solid #32414B;
  width: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::add-page:vertical {
  background: #1464A0;
  border: 1px solid #32414B;
  width: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::add-page:vertical :disabled {
  background: #14506E;
}

QSlider::sub-page:horizontal {
  background: #1464A0;
  border: 1px solid #32414B;
  height: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::sub-page:horizontal:disabled {
  background: #14506E;
}

QSlider::handle:horizontal {
  background: #787878;
  border: 1px solid #32414B;
  width: 8px;
  height: 8px;
  margin: -8px 0px;
  border-radius: 4px;
}

QSlider::handle:horizontal:hover {
  background: #148CD2;
  border: 1px solid #148CD2;
}

QSlider::handle:horizontal:focus {
  border: 1px solid #1464A0;
}

QSlider::handle:vertical {
  background: #787878;
  border: 1px solid #32414B;
  width: 8px;
  height: 8px;
  margin: 0 -8px;
  border-radius: 4px;
}

QSlider::handle:vertical:hover {
  background: #148CD2;
  border: 1px solid #148CD2;
}

QSlider::handle:vertical:focus {
  border: 1px solid #1464A0;
}

/* QLineEdit --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qlineedit

--------------------------------------------------------------------------- */
QLineEdit {
  background-color: #19232D;
  padding-top: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-bottom: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-left: 4px;
  padding-right: 4px;
  border-style: solid;
  border: 1px solid #32414B;
  border-radius: 4px;
  color: #F0F0F0;
}

QLineEdit:disabled {
  background-color: #19232D;
  color: #787878;
}

QLineEdit:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QLineEdit:focus {
  border: 1px solid #1464A0;
}

QLineEdit:selected {
  background-color: #1464A0;
  color: #32414B;
}

/* QTabWiget --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtabwidget-and-qtabbar

--------------------------------------------------------------------------- */
QTabWidget {
  padding: 2px;
  selection-background-color: #32414B;
}

QTabWidget QWidget {
  /* Fixes #189 */
  border-radius: 4px;
}

QTabWidget::pane {
  border: 1px solid #32414B;
  border-radius: 4px;
  margin: 0px;
  /* Fixes double border inside pane with pyqt5 */
  padding: 0px;
}

QTabWidget::pane:selected {
  background-color: #32414B;
  border: 1px solid #1464A0;
}

/* QTabBar ----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtabwidget-and-qtabbar

--------------------------------------------------------------------------- */
QTabBar {
  qproperty-drawBase: 0;
  border-radius: 4px;
  margin: 0px;
  padding: 2px;
  border: 0;
  /* left: 5px; move to the right by 5px - removed for fix */
}

QTabBar::close-button {
  border: 0;
  margin: 2px;
  padding: 2px;
  image: url(":/qss_icons/rc/window_close.png");
}

QTabBar::close-button:hover {
  image: url(":/qss_icons/rc/window_close_focus.png");
}

QTabBar::close-button:pressed {
  image: url(":/qss_icons/rc/window_close_pressed.png");
}

/* QTabBar::tab - selected ------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtabwidget-and-qtabbar

--------------------------------------------------------------------------- */
QTabBar::tab {
  /* !selected and disabled ----------------------------------------- */
  /* selected ------------------------------------------------------- */
}

QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid #14506E;
  color: #787878;
  background-color: #32414B;
}

QTabBar::tab:bottom:selected:disabled {
  border-top: 3px solid #14506E;
  color: #787878;
  background-color: #32414B;
}

QTabBar::tab:left:selected:disabled {
  border-right: 3px solid #14506E;
  color: #787878;
  background-color: #32414B;
}

QTabBar::tab:right:selected:disabled {
  border-left: 3px solid #14506E;
  color: #787878;
  background-color: #32414B;
}

QTabBar::tab:top:!selected:disabled {
  border-bottom: 3px solid #19232D;
  color: #787878;
  background-color: #19232D;
}

QTabBar::tab:bottom:!selected:disabled {
  border-top: 3px solid #19232D;
  color: #787878;
  background-color: #19232D;
}

QTabBar::tab:left:!selected:disabled {
  border-right: 3px solid #19232D;
  color: #787878;
  background-color: #19232D;
}

QTabBar::tab:right:!selected:disabled {
  border-left: 3px solid #19232D;
  color: #787878;
  background-color: #19232D;
}

QTabBar::tab:top:!selected {
  border-bottom: 2px solid #19232D;
  margin-top: 2px;
}

QTabBar::tab:bottom:!selected {
  border-top: 2px solid #19232D;
  margin-bottom: 3px;
}

QTabBar::tab:left:!selected {
  border-left: 2px solid #19232D;
  margin-right: 2px;
}

QTabBar::tab:right:!selected {
  border-right: 2px solid #19232D;
  margin-left: 2px;
}

QTabBar::tab:top {
  background-color: #32414B;
  color: #F0F0F0;
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  min-width: 5px;
  border-bottom: 3px solid #32414B;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}

QTabBar::tab:top:selected {
  background-color: #505F69;
  color: #F0F0F0;
  border-bottom: 3px solid #1464A0;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}

QTabBar::tab:top:!selected:hover {
  border: 1px solid #148CD2;
  border-bottom: 3px solid #148CD2;
  /* Fixes spyder-ide/spyder#9766 */
  padding-left: 4px;
  padding-right: 4px;
}

QTabBar::tab:bottom {
  color: #F0F0F0;
  border-top: 3px solid #32414B;
  background-color: #32414B;
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  min-width: 5px;
}

QTabBar::tab:bottom:selected {
  color: #F0F0F0;
  background-color: #505F69;
  border-top: 3px solid #1464A0;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
}

QTabBar::tab:bottom:!selected:hover {
  border: 1px solid #148CD2;
  border-top: 3px solid #148CD2;
  /* Fixes spyder-ide/spyder#9766 */
  padding-left: 4px;
  padding-right: 4px;
}

QTabBar::tab:left {
  color: #F0F0F0;
  background-color: #32414B;
  margin-top: 2px;
  padding-left: 2px;
  padding-right: 2px;
  padding-top: 4px;
  padding-bottom: 4px;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  min-height: 5px;
}

QTabBar::tab:left:selected {
  color: #F0F0F0;
  background-color: #505F69;
  border-right: 3px solid #1464A0;
}

QTabBar::tab:left:!selected:hover {
  border: 1px solid #148CD2;
  border-right: 3px solid #148CD2;
  padding: 0px;
}

QTabBar::tab:right {
  color: #F0F0F0;
  background-color: #32414B;
  margin-top: 2px;
  padding-left: 2px;
  padding-right: 2px;
  padding-top: 4px;
  padding-bottom: 4px;
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
  min-height: 5px;
}

QTabBar::tab:right:selected {
  color: #F0F0F0;
  background-color: #505F69;
  border-left: 3px solid #1464A0;
}

QTabBar::tab:right:!selected:hover {
  border: 1px solid #148CD2;
  border-left: 3px solid #148CD2;
  padding: 0px;
}

QTabBar QToolButton {
  /* Fixes #136 */
  background-color: #32414B;
  height: 12px;
  width: 12px;
}

QTabBar QToolButton:pressed {
  background-color: #32414B;
}

QTabBar QToolButton:pressed:hover {
  border: 1px solid #148CD2;
}

QTabBar QToolButton::left-arrow:enabled {
  image: url(":/qss_icons/rc/arrow_left.png");
}

QTabBar QToolButton::left-arrow:disabled {
  image: url(":/qss_icons/rc/arrow_left_disabled.png");
}

QTabBar QToolButton::right-arrow:enabled {
  image: url(":/qss_icons/rc/arrow_right.png");
}

QTabBar QToolButton::right-arrow:disabled {
  image: url(":/qss_icons/rc/arrow_right_disabled.png");
}

/* QDockWiget -------------------------------------------------------------

--------------------------------------------------------------------------- */
QDockWidget {
  outline: 1px solid #32414B;
  background-color: #19232D;
  border: 1px solid #32414B;
  border-radius: 4px;
  titlebar-close-icon: url(":/qss_icons/rc/window_close.png");
  titlebar-normal-icon: url(":/qss_icons/rc/window_undock.png");
}

QDockWidget::title {
  /* Better size for title bar */
  padding: 6px;
  spacing: 4px;
  border: none;
  background-color: #32414B;
}

QDockWidget::close-button {
  background-color: #32414B;
  border-radius: 4px;
  border: none;
}

QDockWidget::close-button:hover {
  image: url(":/qss_icons/rc/window_close_focus.png");
}

QDockWidget::close-button:pressed {
  image: url(":/qss_icons/rc/window_close_pressed.png");
}

QDockWidget::float-button {
  background-color: #32414B;
  border-radius: 4px;
  border: none;
}

QDockWidget::float-button:hover {
  image: url(":/qss_icons/rc/window_undock_focus.png");
}

QDockWidget::float-button:pressed {
  image: url(":/qss_icons/rc/window_undock_pressed.png");
}

/* QTreeView QListView QTableView -----------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtreeview
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qlistview
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtableview

--------------------------------------------------------------------------- */
QTreeView:branch:selected, QTreeView:branch:hover {
  background: url(":/qss_icons/rc/transparent.png");
}

QTreeView:branch:has-siblings:!adjoins-item {
  border-image: url(":/qss_icons/rc/branch_line.png") 0;
}

QTreeView:branch:has-siblings:adjoins-item {
  border-image: url(":/qss_icons/rc/branch_more.png") 0;
}

QTreeView:branch:!has-children:!has-siblings:adjoins-item {
  border-image: url(":/qss_icons/rc/branch_end.png") 0;
}

QTreeView:branch:has-children:!has-siblings:closed, QTreeView:branch:closed:has-children:has-siblings {
  border-image: none;
  image: url(":/qss_icons/rc/branch_closed.png");
}

QTreeView:branch:open:has-children:!has-siblings, QTreeView:branch:open:has-children:has-siblings {
  border-image: none;
  image: url(":/qss_icons/rc/branch_open.png");
}

QTreeView:branch:has-children:!has-siblings:closed:hover, QTreeView:branch:closed:has-children:has-siblings:hover {
  image: url(":/qss_icons/rc/branch_closed_focus.png");
}

QTreeView:branch:open:has-children:!has-siblings:hover, QTreeView:branch:open:has-children:has-siblings:hover {
  image: url(":/qss_icons/rc/branch_open_focus.png");
}

QTreeView::indicator:checked,
QListView::indicator:checked {
  image: url(":/qss_icons/rc/checkbox_checked.png");
}

QTreeView::indicator:checked:hover, QTreeView::indicator:checked:focus, QTreeView::indicator:checked:pressed,
QListView::indicator:checked:hover,
QListView::indicator:checked:focus,
QListView::indicator:checked:pressed {
  image: url(":/qss_icons/rc/checkbox_checked_focus.png");
}

QTreeView::indicator:unchecked,
QListView::indicator:unchecked {
  image: url(":/qss_icons/rc/checkbox_unchecked.png");
}

QTreeView::indicator:unchecked:hover, QTreeView::indicator:unchecked:focus, QTreeView::indicator:unchecked:pressed,
QListView::indicator:unchecked:hover,
QListView::indicator:unchecked:focus,
QListView::indicator:unchecked:pressed {
  image: url(":/qss_icons/rc/checkbox_unchecked_focus.png");
}

QTreeView::indicator:indeterminate,
QListView::indicator:indeterminate {
  image: url(":/qss_icons/rc/checkbox_indeterminate.png");
}

QTreeView::indicator:indeterminate:hover, QTreeView::indicator:indeterminate:focus, QTreeView::indicator:indeterminate:pressed,
QListView::indicator:indeterminate:hover,
QListView::indicator:indeterminate:focus,
QListView::indicator:indeterminate:pressed {
  image: url(":/qss_icons/rc/checkbox_indeterminate_focus.png");
}

QTreeView,
QListView,
QTableView,
QColumnView {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  gridline-color: #32414B;
  border-radius: 4px;
}

QTreeView:disabled,
QListView:disabled,
QTableView:disabled,
QColumnView:disabled {
  background-color: #19232D;
  color: #787878;
}

QTreeView:selected,
QListView:selected,
QTableView:selected,
QColumnView:selected {
  background-color: #1464A0;
  color: #32414B;
}

QTreeView:hover,
QListView:hover,
QTableView:hover,
QColumnView:hover {
  background-color: #19232D;
  border: 1px solid #148CD2;
}

QTreeView::item:pressed,
QListView::item:pressed,
QTableView::item:pressed,
QColumnView::item:pressed {
  background-color: #1464A0;
}

QTreeView::item:selected:hover,
QListView::item:selected:hover,
QTableView::item:selected:hover,
QColumnView::item:selected:hover {
  background: #1464A0;
  color: #19232D;
}

QTreeView::item:selected:active,
QListView::item:selected:active,
QTableView::item:selected:active,
QColumnView::item:selected:active {
  background-color: #1464A0;
}

QTreeView::item:!selected:hover,
QListView::item:!selected:hover,
QTableView::item:!selected:hover,
QColumnView::item:!selected:hover {
  outline: 0;
  color: #148CD2;
  background-color: #32414B;
}

QTableCornerButton::section {
  background-color: #19232D;
  border: 1px transparent #32414B;
  border-radius: 0px;
}

/* QHeaderView ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qheaderview

--------------------------------------------------------------------------- */
QHeaderView {
  background-color: #32414B;
  border: 0px transparent #32414B;
  padding: 0px;
  margin: 0px;
  border-radius: 0px;
}

QHeaderView:disabled {
  background-color: #32414B;
  border: 1px transparent #32414B;
  padding: 2px;
}

QHeaderView::section {
  background-color: #32414B;
  color: #F0F0F0;
  padding: 2px;
  border-radius: 0px;
  text-align: left;
}

QHeaderView::section:checked {
  color: #F0F0F0;
  background-color: #1464A0;
}

QHeaderView::section:checked:disabled {
  color: #787878;
  background-color: #14506E;
}

QHeaderView::section::horizontal {
  padding-left: 4px;
  padding-right: 4px;
  border-left: 1px solid #19232D;
}

QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one {
  border-left: 1px solid #32414B;
}

QHeaderView::section::horizontal:disabled {
  color: #787878;
}

QHeaderView::section::vertical {
  padding-left: 4px;
  padding-right: 4px;
  border-top: 1px solid #19232D;
}

QHeaderView::section::vertical::first, QHeaderView::section::vertical::only-one {
  border-top: 1px solid #32414B;
}

QHeaderView::section::vertical:disabled {
  color: #787878;
}

QHeaderView::down-arrow {
  /* Those settings (border/width/height/background-color) solve bug */
  /* transparent arrow background and size */
  background-color: #32414B;
  border: none;
  height: 12px;
  width: 12px;
  padding-left: 2px;
  padding-right: 2px;
  image: url(":/qss_icons/rc/arrow_down.png");
}

QHeaderView::up-arrow {
  background-color: #32414B;
  border: none;
  height: 12px;
  width: 12px;
  padding-left: 2px;
  padding-right: 2px;
  image: url(":/qss_icons/rc/arrow_up.png");
}

/* QToolBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbox

--------------------------------------------------------------------------- */
QToolBox {
  padding: 0px;
  border: 0px;
  border: 1px solid #32414B;
}

QToolBox:selected {
  padding: 0px;
  border: 2px solid #1464A0;
}

QToolBox::tab {
  background-color: #19232D;
  border: 1px solid #32414B;
  color: #F0F0F0;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

QToolBox::tab:disabled {
  color: #787878;
}

QToolBox::tab:selected {
  background-color: #505F69;
  border-bottom: 2px solid #1464A0;
}

QToolBox::tab:selected:disabled {
  background-color: #32414B;
  border-bottom: 2px solid #14506E;
}

QToolBox::tab:!selected {
  background-color: #32414B;
  border-bottom: 2px solid #32414B;
}

QToolBox::tab:!selected:disabled {
  background-color: #19232D;
}

QToolBox::tab:hover {
  border-color: #148CD2;
  border-bottom: 2px solid #148CD2;
}

QToolBox QScrollArea QWidget QWidget {
  padding: 0px;
  border: 0px;
  background-color: #19232D;
}

/* QFrame -----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qframe
https://doc.qt.io/qt-5/qframe.html#-prop
https://doc.qt.io/qt-5/qframe.html#details
https://stackoverflow.com/questions/14581498/qt-stylesheet-for-hline-vline-color

--------------------------------------------------------------------------- */
/* (dot) .QFrame  fix #141, #126, #123 */
.QFrame {
  border-radius: 4px;
  border: 1px solid #32414B;
  /* No frame */
  /* HLine */
  /* HLine */
}

.QFrame[frameShape="0"] {
  border-radius: 4px;
  border: 1px transparent #32414B;
}

.QFrame[frameShape="4"] {
  max-height: 2px;
  border: none;
  background-color: #32414B;
}

.QFrame[frameShape="5"] {
  max-width: 2px;
  border: none;
  background-color: #32414B;
}

/* QSplitter --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qsplitter

--------------------------------------------------------------------------- */
QSplitter {
  background-color: #32414B;
  spacing: 0px;
  padding: 0px;
  margin: 0px;
}

QSplitter::handle {
  background-color: #32414B;
  border: 0px solid #19232D;
  spacing: 0px;
  padding: 1px;
  margin: 0px;
}

QSplitter::handle:hover {
  background-color: #787878;
}

QSplitter::handle:horizontal {
  width: 5px;
  image: url(":/qss_icons/rc/line_vertical.png");
}

QSplitter::handle:vertical {
  height: 5px;
  image: url(":/qss_icons/rc/line_horizontal.png");
}

/* QDateEdit, QDateTimeEdit -----------------------------------------------

--------------------------------------------------------------------------- */
QDateEdit, QDateTimeEdit {
  selection-background-color: #1464A0;
  border-style: solid;
  border: 1px solid #32414B;
  border-radius: 4px;
  /* This fixes 103, 111 */
  padding-top: 2px;
  /* This fixes 103, 111 */
  padding-bottom: 2px;
  padding-left: 4px;
  padding-right: 4px;
  min-width: 10px;
}

QDateEdit:on, QDateTimeEdit:on {
  selection-background-color: #1464A0;
}

QDateEdit::drop-down, QDateTimeEdit::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 12px;
  border-left: 1px solid #32414B;
}

QDateEdit::down-arrow, QDateTimeEdit::down-arrow {
  image: url(":/qss_icons/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QDateEdit::down-arrow:on, QDateEdit::down-arrow:hover, QDateEdit::down-arrow:focus, QDateTimeEdit::down-arrow:on, QDateTimeEdit::down-arrow:hover, QDateTimeEdit::down-arrow:focus {
  image: url(":/qss_icons/rc/arrow_down.png");
}

QDateEdit QAbstractItemView, QDateTimeEdit QAbstractItemView {
  background-color: #19232D;
  border-radius: 4px;
  border: 1px solid #32414B;
  selection-background-color: #1464A0;
}

/* QAbstractView ----------------------------------------------------------

--------------------------------------------------------------------------- */
QAbstractView:hover {
  border: 1px solid #148CD2;
  color: #F0F0F0;
}

QAbstractView:selected {
  background: #1464A0;
  color: #32414B;
}

/* PlotWidget -------------------------------------------------------------

--------------------------------------------------------------------------- */
PlotWidget {
  /* Fix cut labels in plots #134 */
  padding: 0px;
}
"""
