from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget


class CriticalErrorMessageBox(QMessageBox):
    def __init__(self, text: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error")
        self.setText(text)


class FileDialog(QFileDialog):
    def __init__(self, name, path=""):
        super().__init__(directory=path)
        self.setWindowTitle(name)
        # self.setOption(QFileDialog.DontUseNativeDialog, True)


class CSVSaveFileDialog(FileDialog):
    def __init__(self):
        super().__init__(name="CSV File")
        self.setFileMode(QFileDialog.AnyFile)
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setNameFilter("CSV UTF-8(*.csv)")
