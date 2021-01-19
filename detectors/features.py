import numpy as np
import pandas as pd

class DataFeatures():
    """
    Collects features from the input data, recalculates the features vector based on the new samples added
    """
    def __init__(self):
        self.movingAverageResistance = np.array([])
        self.recentVariationResistance = np.array([])
        self.recentVolatilityFrequency = np.array([])
        self.movingAverageTime = 20*60
        self.lagTime = 15*60
        self.lastIndex = 0

    def increment_sample(results_array: np.ndarray):
        #Todo: Make incremental sample add to the existing moving average resistance -> lastIndex - time + dropna

        #Todo: make moving average resistance filter the previous 48 hours for lack of unnecessary data + resample
        pass





