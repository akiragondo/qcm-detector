import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, f'{os.path.dirname(parentdir)}') 
from detectors.secondary_detectors.detector import Detector
import pandas as pd
from models.detection import Detection
from typing import List
import numpy as np
from sklearn.ensemble import IsolationForest


class IsolationDetector(Detector):
    def __init__(self):
        self.initial_sample_time = 15  # Minimum sample time in minutes
        self.sampled = False
        self.prediction_model = IsolationForest(contamination = 0.01)
        self.initial_sample = pd.DataFrame()

        
    def describe(self) -> str:
        return 'IsolationForest'

    def reset(self):
        self.prediction_model = None
        self.initial_sample = pd.DataFrame()
        self.prediction_model = IsolationForest(contamination=0.01)
        self.sampled = False

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        if len(self.initial_sample) == 0:
            self.initial_time = detection_dataframe.index[0]
        
        if not self.sampled:
            self.initial_sample = pd.concat([self.initial_sample, detection_dataframe], axis='rows')
            if detection_dataframe.index[-1] - self.initial_time > pd.Timedelta(f"{self.initial_sample_time}m"):
                self.sampled = True
                self.prediction_model.fit(self.initial_sample)
            return[]
        else:
            detection_indices = np.where(self.prediction_model.fit_predict(detection_dataframe) < 0)[0]
            detection_times = detection_dataframe.iloc[detection_indices].index

            detections = [self.make_detection_from_element(
                dataframe=detection_dataframe,
                index=detection_time,
                detector=self.describe()
            ) for detection_time in detection_times]
            return detections
