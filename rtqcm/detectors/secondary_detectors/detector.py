import pandas as pd
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, f'{os.path.dirname(parentdir)}') 
from models.detection import Detection
from typing import List

class Detector:
    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> int:
        pass

    def describe(self) -> str:
        pass

    def make_detection_from_element(self, dataframe, index, detector) -> Detection:
        dataframe_element = dataframe.loc[index]
        detection = Detection(
            timestamp = dataframe_element['Timestamp'],
            frequency=dataframe_element['Frequency'],
            resistance=dataframe_element['Resistance'],
            severity= 'mild',
            period=[0,0],
            detector=detector,
            time = ''
        )
        return detection

    def make_detection_list_from_dataframe(self, dataframe, detection_indices, detector) -> List[Detection]:
        detections = [self.make_detection_from_element(dataframe, detection,detector) for detection in detection_indices]
        return detections

