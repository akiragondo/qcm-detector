from time import sleep

from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    QObject,
    QThread,
)
import numpy as np


class RunController(QObject):
    finished = pyqtSignal()
    plot_data = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_handler)

    def start_run(self):
        self.timer.setInterval(1000)
        self.timer.start()
        if self.timer.isActive and self.timer.isSignalConnected:
            return True
        else:
            return False

    def start_simulated_run(self):
        self.timer.setInterval(1000/10)
        self.timer.start()
        if self.timer.isActive and self.timer.isSignalConnected:
            return True
        else:
            return False

    def stop_run(self):
        # Handle ressetting everything
        self.timer.stop()

    def timer_handler(self):
        y_data = np.random.rand(1000, 1000)
        y_data = y_data.mean(axis=1)
        x_data = np.linspace(1, len(y_data), len(y_data))
        xy_data = np.vstack((x_data, y_data))
        self.plot_data.emit(xy_data)
