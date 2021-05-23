from time import sleep
from rtqcm.detectors.secondary_detectors.mean_detector import MeanDetector
from rtqcm.detectors.secondary_detectors.prediction_detector import PredictionDetector
from rtqcm.models.detection import Detection
from rtqcm.models.qcm_model import QCMModel
from typing import List
import numpy as np
import pandas as pd

from time import time

class DetectionVoter:
    """
    Class responsible for:
        - Making detections with all detectors available
        - Voting whether or not the detections are valid
        - Making the detection
        - Comparing the detection to previous ones to see if it hasn't already been detected
    """
    def __init__(
            self,
            run_controller
        ):
        self.mean_detector = MeanDetector(
            lag_time=15,
            moving_average_time=10,
            detection_threshold=1.5,
            parent_controller=run_controller
        )
        self.prediction_detector = PredictionDetector()
        self.run_controller = run_controller
        self.dataframe_model = None
        self.past_detections = []

        # Merge conditions
        self.timestamp_diff_thresh = 60
        self.large_timestamp_diff_thresh = 600
        self.resistance_diff_thresh = 1
        self.frequency_diff_thresh = 1

        self.recency_cutoff_hours = 48
        self.recency_cutoff_delta = pd.Timedelta(f"{self.recency_cutoff_hours:02d}:00:00")

    def make_dataframe_from_model(self, qcm_model: QCMModel):
        self.run_controller.mutex.lock()
        index = pd.to_datetime(qcm_model.timestamps, unit='s') - pd.Timedelta('03:00:00')
        dataframe = pd.DataFrame(
            data=zip(qcm_model.resistances, qcm_model.frequencies, qcm_model.timestamps),
            index=index,
            columns= ['Frequency', 'Resistance', 'Timestamp']
        ).resample('10S').mean()
        self.run_controller.mutex.unlock()
        if len(dataframe) > 1:
            cutoff_time = dataframe.index.values[-1] - self.recency_cutoff_delta
            dataframe = dataframe[cutoff_time:]
        return dataframe

    def aggregate_past_detections(self, detections_list: List[Detection]):
        new_detections = []
        for detection in detections_list:
            already_detected = False
            for past_detection in self.past_detections:
                if self.is_same_detection(past_detection, detection):
                    already_detected = True
                    self.convert_to_severe(past_detection)
            if not already_detected:
                new_detections.append(detection)
        self.past_detections = self.past_detections + new_detections

    def convert_to_severe(self, detection):
        detection.severity = 'severe'

    def is_same_detection(self, detection_1 : Detection, detection_2: Detection):
        if np.abs(detection_1.timestamp - detection_2.timestamp) < self.timestamp_diff_thresh:
            return True
        if np.abs(detection_1.timestamp - detection_2.timestamp) < self.large_timestamp_diff_thresh:
            if np.abs(detection_1.resistance - detection_2.resistance)*100/detection_1.resistance < self.resistance_diff_thresh:
                if np.abs(detection_1.frequency - detection_2.frequency)*100/detection_1.frequency < self.frequency_diff_thresh:
                    return True
                return False
            return False
        return False

    def detect(self) -> List[Detection]:
        dataframe_model = self.make_dataframe_from_model(self.run_controller.data_model)
        mean_detections = self.mean_detector.detect_anomalies(dataframe_model)
        # merged_mean_detection = self.merge_similar_detections(mean_detections)
        self.aggregate_past_detections(mean_detections)
        return self.past_detections
