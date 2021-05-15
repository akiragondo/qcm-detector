from time import sleep

from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    QObject,
    QThread,
)
import numpy as np
from rtqcm.api.rs232 import RS232
from rtqcm.models.ConnectionParameters import ConnectionParameters
from rtqcm.models.QCMModel import QCMModel


class RunController(QObject):
    """
    Class responsible for controlling the back-end processing of the program. With functions such as:
        - Managing the read environment (threads, reads and timeouts)
        - Managing the Detections made (New detections, Sending new detections to the ViewController)
        - Managing sending an Email
    """
    finished = pyqtSignal()
    plot_data = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_handler)
        self.is_simulated = False
        self.rsApi = RS232()
        self.data_model = QCMModel()
        self.plot_update_period = 5

    def connect(self):
        pass

    def start_run(self, connectionParams : ConnectionParameters):
        self.is_simulated = False
        self.timer.setInterval(1000)
        self.timer.start()
        connection_successful = self.rsApi.establish_connection(
            connectionParams=connectionParams,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def start_simulated_run(self, connectionParams: ConnectionParameters):
        self.is_simulated = True
        self.timer.setInterval(1000/10)
        self.timer.start()
        connection_successful = self.rsApi.establish_connection(
            connectionParams=connectionParams,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False


    def stop_run(self):
        # Handle ressetting everything
        self.timer.stop()

    def timer_handler(self):
        new_sample = self.rsApi.read_data()
        self.data_model.append_sample(new_sample)
        if len(self.data_model.timestamps) % self.plot_update_period == 0:
            self.plot_data.emit(self.data_model.get_full_results())

