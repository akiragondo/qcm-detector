from rtqcm.models.connection_parameters import ConnectionParameters
from time import sleep
import pandas as pd
import numpy as np
import datetime
import serial
import signal
import enum
import sys


class Status(enum.Enum):
    QueryF = 1
    WaitF = 2
    QueryR = 3
    WaitR = 4
    Finished = 5


class RS232:
    scaleFactors = {
        200: 0,
        500: 1,
        1000: 2,
        2000: 3,
        5000: 4,
        10000: 5,
        20000: 6
    }

    gateTimes = {
        100: 0,
        1000: 1,
        10000: 2
    }

    def __init__(self):
        self.is_simulated = False
        self.simulation_data = None
        self.simulationLength = 0
        self.current_index = 0

        self.ser = None
        self.gate_time = None
        self.scale_factor = None

        self.request_timedout = False
        self.tzinfo = datetime.datetime.now().astimezone().tzinfo

        self.dt = np.dtype([
            ('Time', np.unicode, 32),
            ('Frequency', np.float64),
            ('Resistance', np.float64)
        ])
        self.connection_params = None

    def establish_connection(self,
                             connection_params: ConnectionParameters,
                             is_simulated: bool):
        self.connection_params = connection_params
        if is_simulated:
            try:
                self.simulation_data = pd.read_csv(
                    self.connection_params.simulation_data_path,
                    parse_dates=["Time"],
                    index_col="Time"
                )
                self.simulationLength = len(self.simulation_data)
                self.is_simulated = is_simulated
                self.current_index = 0
                return True
            except Exception:
                return False
        else:
            self.is_simulated = is_simulated
            self.current_index = 0

            try:
                self.ser = serial.Serial(
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    bytesize=serial.EIGHTBITS,
                    stopbits=1,
                    port=self.connection_params.port_name
                )
                self.ser.isOpen()
                self.update_qcm_parameters()
                signal.signal(signal.SIGALRM, self.timeout_handler)
                print(
                    f"Connection established! port: {self.connection_params.port_name}"
                )
                return True
            except Exception:
                return False

    def update_qcm_parameters(self):
        assert(self.connection_params.correct_metadata())
        self.ser.write('P{}\r'.format(
            self.gateTimes[
                self.connection_params.gate_time
            ]
        ).encode())
        sleep(1)
        self.ser.write('D{}\r'.format(
            self.scaleFactors[
                self.connection_params.scale_factor
            ]
        ).encode())

    def timeout_handler(self, signum, frame):
        self.request_timedout = True
        print('timeout')

    def datetime_to_float(self, d):
        epoch = datetime.datetime.utcfromtimestamp(0)
        total_seconds = (
                d - epoch - self.tzinfo.utcoffset(None)).total_seconds()
        # total_seconds will be in decimals (millisecond precision)
        return total_seconds

    def read_data(self):
        # Input: none #Output: packet with [time, resistance, frequency]
        if not self.is_simulated:
            query_status = Status.QueryF
            frequency = None
            resistance = None
            self.request_timedout = False

            signal.alarm(5)
            while query_status != Status.Finished and not self.request_timedout:
                try:
                    if query_status == Status.QueryF:
                        self.ser.write('F\r'.encode())
                        query_status = Status.WaitF
                    elif query_status == Status.WaitF:
                        if self.ser.inWaiting() > 0:
                            frequency = float(self.ser.readline())
                            self.ser.write('R\r'.encode())
                            query_status = Status.WaitR
                    elif query_status == Status.WaitR:
                        if self.ser.inWaiting() > 0:
                            resistance = float(self.ser.readline())
                            query_status = Status.Finished
                except Exception:
                    return None

            if self.request_timedout:
                return None
            else:
                signal.alarm(0)
                d = datetime.datetime.now()
                time = f"{d.day}/{d.month}/{d.year} {d.hour}:{d.minute}:{d.second}.{d.microsecond}"
                d = self.datetime_to_float(d)
                return np.array([d, frequency, resistance])
        else:
            if self.current_index < self.simulationLength:
                d = self.simulation_data.index[self.current_index]
                time = f"{d.day}/{d.month}/{d.year} {d.hour}:{d.minute}:{d.second}.{d.microsecond}"
                current_row = self.simulation_data.values[self.current_index]
                frequency = current_row[0]
                resistance = current_row[1]
                d = self.datetime_to_float(d)
                self.current_index += 1
                return np.array([d, frequency, resistance])
            else:
                return None
