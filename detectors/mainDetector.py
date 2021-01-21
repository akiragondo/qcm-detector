import numpy as np
import pandas as pd
from .detectorInterface import DetectorInterface
from .dataFeatures import DataFeatures

class MainDetector(DetectorInterface):
    def __init__(self, detectionPeriod : int):
        self.averageSize = 20 #minutes
        self.lagSize = 20 #minutes

        self.varThreshold = 1.6 #threshold percentage for detection
        self.severeThreshold = 4 #threshold percentage for detection
        self.detectionPeriod = int(detectionPeriod)
        """
            code:
                -1 - needs more data
                0 - Undetected
                1 - initial detected
                2 - anomaly detected
        """

    def detectAnomaly(self, data : DataFeatures) -> int:
        currentSampleSize = len(data.dataSamples)
        neededDataSamples = (self.lagSize + self.averageSize)*60/data.samplePeriod + 1
        if currentSampleSize > neededDataSamples :
            #Detect normally

            avgSampleSize = int(self.averageSize*60/data.samplePeriod)
            lagSampleSize = int(self.lagSize*60/data.samplePeriod)
            rollingShiftData = data.dataSamples.rolling(window=avgSampleSize).mean().shift(periods = lagSampleSize)
            rollingShiftData = (data.dataSamples - rollingShiftData)*100/rollingShiftData
            if np.any(rollingShiftData['Resistance'].values[- self.detectionPeriod:] > self.severeThreshold):
                return 2
            elif np.any(rollingShiftData['Resistance'].values[-self.detectionPeriod:] > self.varThreshold):
                return 1
            else:
                return 0
        else:
            return -1


