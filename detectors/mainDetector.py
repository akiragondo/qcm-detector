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
        self.lastDetection = None
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
            rollingAvg = data.dataSamples.rolling(window=avgSampleSize).mean()
            rollingShiftData = (data.dataSamples - rollingAvg.shift(periods = lagSampleSize))*100/rollingAvg.shift(periods = lagSampleSize)
            if np.any(rollingShiftData['Resistance'].values[- self.detectionPeriod:] > self.severeThreshold):
                if self.lastDetection is None:
                    self.lastDetection = data.dataSamples[-1]['Resistance']
                else:
                    if (rollingAvg[-1]['Resistance'] - self.lastDetection)*100/self.lastDetection:
                        return 0
                return 2
            elif np.any(rollingShiftData['Resistance'].values[-self.detectionPeriod:] > self.varThreshold):
                if self.lastDetection is None:
                    self.lastDetection = data.dataSamples[-1]['Resistance']
                else:
                    if (rollingAvg[-1]['Resistance'] - self.lastDetection)*100/self.lastDetection:
                        return 0
                return 1
            else:
                self.lastDetection = None
                return 0
        else:
            return -1


