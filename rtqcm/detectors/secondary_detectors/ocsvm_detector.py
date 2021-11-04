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


class SVMDetector(Detector):
    def __init__(self):
        self.clf = OneClassSVM(kernel = 'rbf', gamma='scale', nu=0.1)
        self.sliding_window_time = 150 #seconds
        self.training_time = 180 #seconds
        self.sampled = False
        self.start_time = None
        
    def describe(self) -> str:
        return 'OneClassSVM'

    def reset(self):
        self.clf = OneClassSVM(kernel = 'rbf', gamma='scale', nu=0.1)
        self.start_time = None
        self.sampled = False

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        detection_diff = (detection_dataframe - detection_dataframe.rolling(f'{self.sliding_window_time}s').mean()).dropna()
        if self.start_time == None:
            self.start_time = detection_dataframe.index.values[0]
        else:
            if (detection_dataframe.index.values[-1] - self.start_time) > np.timedelta64(self.training_time, 's') and not self.sampled:
                self.sampled = True
                self.clf = self.clf.fit(detection_diff)
            elif self.sampled:
                y_pred = self.clf.fit_predict(detection_diff)
                detection_indices = np.where(y_pred < 0)[0]
                detection_times = detection_diff.iloc[detection_indices].index

                detections = [self.make_detection_from_element(
                    dataframe=detection_dataframe,
                    index=detection_time,
                    detector=self.describe()
                ) for detection_time in detection_times]
                return detections
        return []