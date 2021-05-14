from time import sleep

from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    QObject,
    QThread,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from rtqcm.controllers.MainWindowTemplate import MainWindowTemplate
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    current_n = 0
    def run(self):
        """Long-running task."""
        for i in range(10):
            sleep(0.1)
            Worker.current_n += 1
            self.progress.emit(Worker.current_n)
        self.finished.emit()
    def reset(self):
        """Reverse-long running task"""
        while Worker.current_n > 0:
            sleep(0.05)
            Worker.current_n -= 1
            self.progress.emit(Worker.current_n)
        self.finished.emit()

class ViewController(MainWindowTemplate):
    def __init__(self, window):
        self.setupUi(window)
        self.window = window