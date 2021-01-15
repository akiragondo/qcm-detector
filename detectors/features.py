import numpy as np
import pandas as pd

class DataFeatures():
    """
    Collects features from the input data, recalculates the features vector based on the new samples added
    """
    def __init__(self):
        self.movingAverageResistance = None
        self.recentVariationResistance = None
        self.recentVolatilityFrequency = None

