from rtqcm.detectors.secondary_detectors.detector import Detector
from rtqcm.models.detection import Detection
from typing import List
import pandas as pd


class MeanDetector(Detector):
    def __init__(
            self,
            lag_time: float,
            moving_average_time: float,
            detection_threshold: float,
            parent_controller
    ):
        self.lag_time = lag_time
        self.moving_average_time = moving_average_time

        self.lag_time_format = f"00:{lag_time:02d}:00"
        self.moving_average_time_string = f"{moving_average_time}min"

        self.last_detection = None
        self.detection_threshold = detection_threshold
        self.parent_controller = parent_controller

    def reset(self):
        self.last_detection = None

    def describe(self) -> str:
        return 'Mean-shift'

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        rolling_average = detection_dataframe['Resistance'].rolling(self.moving_average_time_string).mean()
        shifted = rolling_average.shift(periods = self.lag_time, freq= 'min')
        diff = abs((rolling_average - shifted)*100/shifted)
        detection_indices = diff.index[diff > self.detection_threshold]
        if self.last_detection is not None:
            detection_indices = [detection_index for detection_index in detection_indices if detection_index > self.last_detection]
        self.last_detection = diff.index[-1] - pd.Timedelta(self.lag_time_format)
        detections = self.make_detection_list_from_dataframe(detection_dataframe, detection_indices, self.describe())
        return detections




