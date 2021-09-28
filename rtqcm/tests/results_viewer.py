import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
from typing import List
import sys, os
import json


if __name__ == '__main__':
    input_file = "/home/kimino/soft/qcm-detector/results.json"
    with open(input_file, 'r') as input_results:
        s = input_results.read()

        results = json.loads(s)
    for result_key in list(results.keys()):
        result = results[result_key]
        data_df = pd.read_csv(
            result['Path'],
            sep=',',
            delim_whitespace=False,
            parse_dates=['Time'],
            dayfirst=True,
            index_col='Time'
        ).rename(columns=lambda x: x.strip())
        fig, ax = plt.subplots()
        time = (data_df.index.values + pd.to_timedelta('03:00:00')).astype('float64')/1e+9
        ax.plot(time, data_df['Resistance'], alpha = 0.8)
        ax.set_title(f"Experiment: {result_key}\nRecall: {result['Recall']} TP: {result['Number of True Positives']} FP: {result['Number of False Positives']} FN: {result['Number of False Negatives']}")

        for detection in result['True Positives']:
            ax.axvline(detection['timestamp'], color='g', alpha=0.45)
        for detection in result['Detections']:
            if detection not in result['True Positives']:
                ax.axvline(detection['timestamp'], color='r', alpha=0.45)
        plt.show()
