import numpy as np
import pandas as pd
from .detectorInterface import DetectorInterface

class MainDetector(DetectorInterface):
    def __init__(self):
        self.initialResistance = None
        self.lastResistance = None
        self.detectionTime = None
        self.currentResistance = None

        #Variable thresholds for detections
        #initial derivative for starting detection
        self.initialDiffDetectionThresh = 0.05

        #percentage of difference in resistance to detect a contamination
        self.resistanceDiffDetectionThresh = 2

    def detectAnomaly(self, sample: np.ndarray) -> int:
        if self.lastResistance is None:
            self.lastResistance = sample[0][2]
            self.currentResistance = sample[0][2]

