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
from sklearn.svm import OneClassSVM


class IsolationDetector(Detector):
    def __init__(self):
        clf = OneClassSVM(kernel = 'rbf', gamma='scale', nu=0.1)
        self.sliding_window_time = 150 #seconds

        
    def describe(self) -> str:
        return 'OneClassSVM'

    def reset(self):
        clf = OneClassSVM(kernel = 'rbf', gamma='scale', nu=0.1)

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        detection_diff = (detection_dataframe - detection_dataframe.rolling(f'{self.sliding_window_time}s').mean()).dropna()
        
        y_pred = self.clf.fit_predict(detection_diff)
        detection_indices = np.where(y_pred < 0)[0]
        detection_times = detection_diff.iloc[detection_indices].index

        detections = [self.make_detection_from_element(
            dataframe=detection_dataframe,
            index=detection_time,
            detector=self.describe()
        ) for detection_time in detection_times]
        return detections
