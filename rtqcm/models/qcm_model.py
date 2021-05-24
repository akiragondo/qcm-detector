import numpy as np
import pandas as pd


class QCMModel:
    def __init__(self):
        self.resistances = np.array([])
        self.frequencies = np.array([])
        self.timestamps = np.array([])

    def append_sample(self, sample):
        self.resistances = np.append(self.resistances, sample[1])
        self.timestamps = np.append(self.timestamps, sample[0])
        self.frequencies = np.append(self.frequencies, sample[2])
        return True

    def get_frequency_results(self):
        results = np.vstack((self.timestamps, self.frequencies))
        return results

    def get_resistance_results(self):
        results = np.vstack((self.timestamps, self.frequencies))
        return results

    def get_full_results(self):
        results = np.vstack((self.timestamps, self.resistances, self.frequencies))
        return results

    def get_full_results_as_samples(self):
        results = np.vstack((self.timestamps, self.resistances, self.frequencies)).T
        return results

    def is_empty_model(self):
        return len(self.timestamps) <= 0

    def reset_model(self):
        self.resistances = np.array([])
        self.frequencies = np.array([])
        self.timestamps = np.array([])

