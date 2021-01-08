from .detectorInterface import DetectorInterface
import numpy as np

class Aggregator(DetectorInterface):
    """
    Class: Aggregator
    Description: Aggregates the detections from each detector to return the class of contaminations (if there are any) in the sample collected.
    score has to be kept for 10 minutes, if no other detections are found, a score 1 anomaly is raised
    if another anomaly has been found after 10 minutes, its score is added and a contamination is raised
    if the main detector detects an anomaly, a contamination is immediately raised
    Detectors:
        - Main detector
            If derivative > thresh and after 15 minutes, curRes > 1.02*initialRes -> Contamination
            Derivative > thresh -> avoids temperature drifts being detected as contaminations
        - Auxiliary detectors
            Volatility -> Average moving standard deviation change
            Arima -> Unexpected changes in readings
    """
    def __init__(self):
        self.currentScore = 0

    def detectAnomaly(self, sample: np.ndarray) -> int:
