import numpy as np
import pandas as pd

def isStable(sample : np.ndarray,stabilizationTime : int):
    stabilizationThreshold = stabilizationTime*0.8/(900*100)
    max = sample.max()
    min = sample.min()
    mean = sample.mean()
    maxDev = (max - mean)/mean
    minDev = (mean - min)/mean
    dev = np.max([maxDev,minDev])
    # print("Stability Checked for {} samples:".format(stabilizationTime))
    # print(" Deviation of {}% found".format(dev*100))
    if dev < stabilizationThreshold:
        return True
    else:
        return False