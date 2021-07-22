import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

if __name__ == '__main__':
    input_file_path = '/home/kimino/soft/qcm-detector/data/tests/test_descriptions.json'
    with open(input_file_path, 'r') as test_json_file:
        input_file = json.loads(test_json_file.read())
    tests = input_file['Tests']
    for test in tests:
        test_object = test[list(test.keys())[0]]
        test_df = pd.read_csv(
            test_object['Path'],
            sep=',',
            delim_whitespace=False
        ).rename(columns=lambda x: x.strip())
        fig, ax = plt.subplots()
        test_df['Resistance'].plot(ax = ax)
        for anomaly in test_object['Anomalies']:
            start = anomaly['Start']
            end = anomaly['End']
            ax.axvspan(start, end, alpha= 0.2, color = 'red')
        plt.title(f"{test_object['Path'].split('/')[-1]}")
        plt.show()