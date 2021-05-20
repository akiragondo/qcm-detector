from PyQt5.QtCore import (
    QTimer,
    pyqtSignal,
    QObject,
    QThread,
    QMutex
)
import logging
from rtqcm.models.connection_parameters import ConnectionParameters
from rtqcm.models.qcm_model import QCMModel
from rtqcm.models.detection import Detection
from rtqcm.controllers.read_controller import ReadController
from rtqcm.controllers.detection_controller import DetectionController


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
    detection = pyqtSignal(Detection)
    read = pyqtSignal()
    plot_data = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self.read_timer_handler)
        self.detect_timer = QTimer()
        self.detect_timer.timeout.connect(self.detection_timer_handler)
        self.threads = []

        # Instantiate reader thread
        self.reader_thread = QThread()
        self.reader = ReadController()
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

        self.is_simulated = False
        self.data_model = QCMModel()
        self.simulated_acceleration_factor = 10
        self.plot_update_period = 5
        self.timeout_limit = 10
        self.timeout_counter = 0

        self.mutex = QMutex()

    def start_run(self, connection_params: ConnectionParameters):
        if not self.data_model.is_empty_model():
            self.data_model.reset_model()
        self.is_simulated = False
        self.start_timers(
            read_period= 1000,
            detect_period= 10000
        )
        connection_successful = self.reader.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

    def start_timers(
            self,
            read_period,
            detect_period
    ):
        self.read_timer.setInterval(read_period)
        self.detect_timer.setInterval(detect_period)
        self.read_timer.start()
        self.detect_timer.start()

    def start_simulated_run(self, connection_params: ConnectionParameters):
        if not self.data_model.is_empty_model():
            self.data_model.reset_model()
        self.is_simulated = True
        self.start_timers(
            read_period= 1000/self.simulated_acceleration_factor,
            detect_period= 10000/self.simulated_acceleration_factor
        )
        connection_successful = self.reader.establish_connection(
            connection_params=connection_params,
            is_simulated=self.is_simulated
        )
        if connection_successful:
            return True
        else:
            return False

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

    def receive_new_detection(self, detection: Detection):
        if detection.severity is not None:
            self.detection.emit(detection)

