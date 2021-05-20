from rtqcm.detectors.secondary_detectors.detector_interface import DetectorInterface
from rtqcm.models.detection import Detection
from typing import List
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

        self.lag_time_string = f"{lag_time}min"
        self.moving_average_time_string = f"{moving_average_time}min"

        self.detection_threshold = detection_threshold
        self.parent_controller = parent_controller

    def describe(self) -> str:
        raise NotImplementedError

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        rolling_average = detection_dataframe['Resistance'].rolling(self.moving_average_time_string).mean()
        shifted = rolling_average.shift(periods = self.lag_time, freq= 'min')
        diff = (rolling_average - shifted)*100/shifted
        detection_indices = diff.index[diff > self.detection_threshold]
        detections = self.make_detection_list_from_dataframe(detection_dataframe, detection_indices)
        return detections




