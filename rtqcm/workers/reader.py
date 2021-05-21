from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)
import numpy as np
from rtqcm.api.rs232 import RS232
from rtqcm.models.connection_parameters import ConnectionParameters

class Reader(QObject):
    sample= pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.serial_api = RS232()
        self.connected = False

    def establish_connection(self, connection_params: ConnectionParameters, is_simulated):
        connection_successful = self.serial_api.establish_connection(
            connection_params=connection_params,
            is_simulated=is_simulated
        )
        return connection_successful

    def read(self):
        sample = self.serial_api.read_data()
        self.sample.emit(sample)


