import numpy as np
import pandas as pd
from .detectorInterface import DetectorInterface

class MainDetector(DetectorInterface):
    def __init__(self):
        """
        Idea behind detector: if it detects a deviation between max - min bigger than a percentage of the moving
        average, it gets into state 1 and puts boundaries a percentage amount <100% of the threshold around the
        moving average. If the resistance keeps itself outside of these boundaries for a number of minutes,
        it will be  detected as a contamination
        """
        self.previousResistances = np.array([])
        self.previousFrequencies = np.array([])

        self.initialOnsetTime = 10 #minutes
        self.hysteresisWaitTime = 5 #minutes

        self.hysteresisPercentage = 30 #min to top hysteresis for detection stability
        self.initialThreshold = 2 #threshold for initial detection
        """
            code:
                0 - Undetected
                1 - initial detected
                2 - anomaly detected
        """
        self.state = 0
        self.hysteresisResTop = None
        self.hysteresisResBottom = None

    def detectAnomaly(self, sample: np.ndarray) -> int:
        if len(self.previousResistances < 15):
            self.previousResistances = np.append(self.previousResistances, np.mean(sample[:,2]))
            self.previousFrequencies = np.append(self.previousFrequencies, np.mean(sample[:,1]))
            return -1
        else:
            self.previousResistances = np.roll(self.previousResistances,-1)
            self.previousResistances[-1] = np.mean(sample[:,2])
            self.previousFrequencies = np.roll(self.previousFrequencies,-1)
            self.previousFrequencies[-1] = np.mean(sample[:,1])

            averageResistance = np.mean(self.previousResistances)

            if self.state == 0:
                deviation = np.max(self.previousResistances) - np.mean(self.previousResistances)
                deviation = (deviation/averageResistance)*100
                if deviation > self.initialThreshold:
                    self.state = 1
                    self.hysteresisResTop = self.averageResistance


