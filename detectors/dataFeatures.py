import numpy as np
import pandas as pd

class DataFeatures():
    """
    Collects features from the input data, recalculates the features vector based on the new samples added
    """
    def __init__(self):
        self.plotData = np.array([])
        self.dataSamples = pd.DataFrame(columns=['Frequency', 'Resistance'])
        self.currentSample = []
        self.samplePeriod = 30 #Seconds from each sample picked
        self.lastTimestamp = None
        self.timePassed = 0

    def reset(self):
        self.plotData = np.array([])
        self.dataSamples = pd.DataFrame(columns=['Frequency', 'Resistance'])
        self.currentSample = []
        self.lastTimestamp = None
        self.timePassed = 0

    def increment_sample(self,results_array: np.ndarray):
        #Append plot time
        if len(self.plotData) <= 0:
            self.plotData = results_array
        else:
            self.plotData = np.vstack((self.plotData, results_array))

        if len(self.currentSample) <= 0:
            self.currentSample = results_array
        else:
            self.currentSample = np.vstack((self.currentSample, results_array))

        #If results array is of timestamp that shows an elapsed time over samplePeriod -> sample the data and zero the averages
        if self.lastTimestamp is None:
            self.lastTimestamp = results_array[0]
        else:
            self.timePassed = self.timePassed + (results_array[0] - self.lastTimestamp)
            self.lastTimestamp = results_array[0]

        if self.timePassed >= self.samplePeriod:
            self.timePassed = 0
            meanTimestamp = self.currentSample[:,0].mean()
            meanFrequency = self.currentSample[:,1].mean()
            meanResistance = self.currentSample[:,2].mean()
            data = {
                'Frequency' : meanFrequency,
                'Resistance' : meanResistance
            }
            df = pd.DataFrame(data,index=[pd.to_datetime(meanTimestamp, unit='s')])
            self.currentSample = []
            self.dataSamples = self.dataSamples.append(df)

        #Todo: Remove stored algorithm data after 48 hours


