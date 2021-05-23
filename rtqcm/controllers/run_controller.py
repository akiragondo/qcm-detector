from PyQt5.QtCore import (
    QTimer,
    pyqtSignal,
    QObject,
    QThread,
    QMutex
)
import logging
from typing import List
from rtqcm.models.connection_parameters import ConnectionParameters
from rtqcm.models.qcm_model import QCMModel
from rtqcm.models.detection import Detection
from rtqcm.workers.reader import Reader
from rtqcm.controllers.detection_controller import DetectionController
from rtqcm.workers.saver import Saver

class RunController(QObject):
    """
    Class responsible for controlling the back-end processing of the program. With functions such as:
        - Managing the read environment (threads, reads and timeouts)
        - Managing the Detections made (New detections, Sending new detections to the ViewController)
        - Managing sending an Email
    """
    finished = pyqtSignal()
    bad_connection = pyqtSignal()
    disconnect_timeout = pyqtSignal()
    detect = pyqtSignal()
    detection = pyqtSignal(object)
    read = pyqtSignal()
    plot_data = pyqtSignal(object)
    save = pyqtSignal(object, str)


    def __init__(self):
        super().__init__()
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.save_timer_handler)
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self.read_timer_handler)
        self.detect_timer = QTimer()
        self.detect_timer.timeout.connect(self.detection_timer_handler)
        self.threads = []
        self.mutex = QMutex()

        # Instantiate reader thread
        self.reader_thread = QThread()
        self.reader = Reader()
        self.reader.moveToThread(self.reader_thread)
        self.read.connect(self.reader.read)
        self.reader.sample.connect(self.receive_new_sample)
        self.reader_thread.start()
        self.threads.append(self.reader_thread)

        # Instantiate detector thread
        self.detector_thread = QThread()
        self.detector = DetectionController(parent_run_controller= self)
        self.detector.moveToThread(self.detector_thread)
        self.detect.connect(self.detector.detect)
        self.detector.detection.connect(self.receive_new_detection)
        self.detector_thread.start()
        self.threads.append(self.detector_thread)

        # Instantiate Saver thread
        self.saver_thread = QThread()
        self.saver = Saver(parent_mutex=self.mutex)
        self.saver.moveToThread(self.saver_thread)
        self.save.connect(self.saver.append_save)
        self.saver_thread.start()
        self.threads.append(self.saver_thread)

        self.is_simulated = False
        self.data_model = QCMModel()

        self.read_period = 1*1000
        self.detect_period = 30*1000
        self.save_period = 5*1000
        self.simulated_acceleration_factor = 10
        self.plot_update_period = 5
        self.timeout_limit = 10
        self.timeout_counter = 0

        self.connection_params: ConnectionParameters

    def start_timers(
            self,
            read_period,
            detect_period,
            save_period
    ):
        self.read_timer.setInterval(read_period)
        self.detect_timer.setInterval(detect_period)
        self.save_timer.setInterval(save_period)
        self.read_timer.start()
        self.detect_timer.start()
        self.save_timer.start()

    def start_run(self, connection_params: ConnectionParameters):
        if not self.data_model.is_empty_model():
            self.data_model.reset_model()
        self.is_simulated = False
        self.connection_params = connection_params
        self.start_timers(
            read_period= self.read_period,
            detect_period= self.detect_period,
            save_period= self.save_period
        )
        connection_successful = self.reader.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def start_simulated_run(self, connection_params: ConnectionParameters):
        if not self.data_model.is_empty_model():
            self.data_model.reset_model()
        self.is_simulated = True
        self.connection_params = connection_params
        self.start_timers(
            read_period= self.read_period/self.simulated_acceleration_factor,
            detect_period= self.detect_period/self.simulated_acceleration_factor,
            save_period= self.save_period
        )
        connection_successful = self.reader.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def save_timer_handler(self):
        self.save.emit(self.data_model, self.connection_params.output_data_file)

    def read_timer_handler(self):
        self.read.emit()

    def detection_timer_handler(self):
        self.detect.emit()

    def stop_run(self):
        self.read_timer.stop()
        self.detect_timer.stop()

    def receive_new_sample(self, new_sample):
        if new_sample is not None:
            self.timeout_counter = 0
            self.mutex.lock()
            self.data_model.append_sample(new_sample)
            self.mutex.unlock()
            if len(self.data_model.timestamps) % self.plot_update_period == 0:
                self.plot_data.emit(self.data_model.get_full_results())
        else:
            self.timeout_counter += 1
            logging.debug(f'Connection with RS232 timed out: {self.timeout_counter} times')
            if self.timeout_counter >= self.timeout_limit:
                self.stop_run()
                self.disconnect_timeout.emit()

    def receive_new_detection(self, detection: List[Detection]):
        self.detection.emit(detection)

