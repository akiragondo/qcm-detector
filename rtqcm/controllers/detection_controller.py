from PyQt5.QtCore import (
    pyqtSignal,
    QObject,
)
from rtqcm.detectors.detection_voter import DetectionVoter
from rtqcm.models.detection import Detection
import logging
import numpy as np
import pandas as pd


class DetectionController(QObject):
    detection= pyqtSignal(object)

    def __init__(
            self,
            parent_run_controller
    ):
        super().__init__()
        self.parent_run_controller = parent_run_controller
        self.detection_voter = DetectionVoter(parent_run_controller)


    def detect(self):
        detection_result = self.detection_voter.detect()
        self.detection.emit(detection_result)

