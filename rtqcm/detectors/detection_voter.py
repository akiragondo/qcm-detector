from time import sleep
from rtqcm.detectors.secondary_detectors.mean_detector import MeanDetector
from rtqcm.detectors.secondary_detectors.prediction_detector import PredictionDetector
from rtqcm.models.detection import Detection
from rtqcm.models.qcm_model import QCMModel
from typing import List
import numpy as np
import pandas as pd

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
            lag_time=1,
            moving_average_time=1,
            detection_threshold=1.5,
            parent_controller=run_controller
        )
        self.prediction_detector = PredictionDetector()
        self.run_controller = run_controller
        self.dataframe_model = None

    def make_dataframe_from_model(self, qcm_model: QCMModel):
        index = pd.to_datetime(qcm_model.timestamps, unit='s') - pd.Timedelta('03:00:00')
        dataframe = pd.DataFrame(
            data=zip(qcm_model.resistances, qcm_model.frequencies, qcm_model.timestamps),
            index=index,
            columns= ['Frequency', 'Resistance', 'Timestamp']
        ).resample('5S').mean()
        return dataframe

    def merge_similar_detections(self, detections_list: List[Detection]):
        if len(detections_list) > 0:
            first_timestamp_time = detections_list[0].timestamp
            severity = 'mild' if len(detections_list) < 6 else 'severe'
            mean_frequency = np.mean([detection.frequency for detection in detections_list])
            mean_resistance = np.mean([detection.resistance for detection in detections_list])
            total_period = [detections_list[0].timestamp, detections_list[-1].timestamp]
            merged_detection = Detection(
                timestamp=first_timestamp_time,
                severity=severity,
                frequency=mean_frequency,
                resistance=mean_resistance,
                period=total_period
            )
            return merged_detection
        else:
            return None

    def detect(self) -> Detection:
        self.run_controller.mutex.lock()
        dataframe_model = self.make_dataframe_from_model(self.run_controller.data_model)
        self.run_controller.mutex.unlock()
        mean_detections = self.mean_detector.detect_anomalies(dataframe_model)
        merged_mean_detection = self.merge_similar_detections(mean_detections)
        if merged_mean_detection is not None:
            print("Detected something")
        else:
            print("Skipped detection")
        return merged_mean_detection
