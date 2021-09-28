from time import sleep
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from detectors.secondary_detectors.ocsvm_detector import SVMDetector
from detectors.secondary_detectors.mean_detector import MeanDetector
from detectors.secondary_detectors.prediction_detector import PredictionDetector
from detectors.secondary_detectors.isolation_detector import IsolationDetector
from models.detection import Detection
from models.qcm_model import QCMModel
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
        self.isolation_detector = IsolationDetector()
        self.ocsvm_detector = SVMDetector()
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

    def reset(self):
        self.past_detections = []
        self.prediction_detector.reset()
        self.mean_detector.reset()
        self.isolation_detector.reset()
        self.ocsvm_detector.reset()

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
        if detection_1.detector != detection_2.detector:
            return False
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
        if not dataframe_model.empty:
            mean_detections = self.mean_detector.detect_anomalies(dataframe_model)
            prediction_detections = self.prediction_detector.detect_anomalies(dataframe_model)
            isolation_detections = self.isolation_detector.detect_anomalies(dataframe_model)
            ocsvm_detections = self.ocsvm_detector.detect_anomalies(dataframe_model)
            detections = mean_detections + prediction_detections + isolation_detections + ocsvm_detections
            
            self.aggregate_past_detections(detections)
            return self.past_detections
        else:
            return []
