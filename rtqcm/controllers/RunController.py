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
import logging


class RunController(QObject):
    """
    Class responsible for controlling the back-end processing of the program. With functions such as:
        - Managing the read environment (threads, reads and timeouts)
        - Managing the Detections made (New detections, Sending new detections to the ViewController)
        - Managing sending an Email
    """
    finished = pyqtSignal()
    disconnect_timeout = pyqtSignal()
    plot_data = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_handler)
        self.is_simulated = False
        self.rs_api = RS232()
        self.data_model = QCMModel()
        self.plot_update_period = 5
        self.timeout_limit = 10
        self.timeout_counter = 0

    def connect(self):
        pass

    def start_run(self, connection_params: ConnectionParameters):
        self.is_simulated = False
        self.timer.setInterval(1000)
        self.timer.start()
        connection_successful = self.rs_api.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def start_simulated_run(self, connection_params: ConnectionParameters):
        self.is_simulated = True
        self.timer.setInterval(1000 / 10)
        self.timer.start()
        connection_successful = self.rs_api.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def stop_run(self):
        # Handle resetting everything
        self.timer.stop()

    def timer_handler(self):
        new_sample = self.rs_api.read_data()
        if new_sample is not None:
            self.timeout_counter = 0
            self.data_model.append_sample(new_sample)
            if len(self.data_model.timestamps) % self.plot_update_period == 0:
                self.plot_data.emit(self.data_model.get_full_results())
        else:
            self.timeout_counter += 1
            logging.debug(f'Connection with RS232 timed out: {self.timeout_counter} times')
            if self.timeout_counter >= self.timeout_limit:
                self.disconnect_timeout.emit()



