from PyQt5.QtCore import (
    pyqtSignal,
    QObject,
)
from rtqcm.detectors.detection_voter import DetectionVoter
import logging
import numpy as np
import pandas as pd

class DetectionController(QObject):
    def __init__(
            self,
            parent_run_controller
    ):
        super().__init__()
        self.parent_run_controller = parent_run_controller


    #TODO: Add slots in detector to perform detections
