from rtqcm.detectors.secondary_detectors.detector_interface import DetectorInterface
import numpy as np
import pandas as pd


class MeanDetector(DetectorInterface):
    def __init__(
            self,
            lag_time: float,
            moving_average_time: float,
            detection_threshold: float,
            parent_controller
    ):
        self.lag_time = lag_time
        self.moving_average_time = moving_average_time
        self.detection_threshold = detection_threshold
        self.parent_controller = parent_controller

    def describe(self) -> str:
        raise NotImplementedError

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> int:
        #TODO: find way to shift based in time

        #TODO: make moving average shifted difference
        raise NotImplementedError

