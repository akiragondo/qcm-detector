import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
from typing import List
import sys, os
import json

def make_detection_from_period_tuple(period):
    detection = {
        "Start": period[0],
        "End": period[1]
    }
    return detection

if __name__ == '__main__':
    folder = "/home/kimino/soft/qcm-detector/data/tests/"
    folder_query = folder+'*.csv'
    files_in_folder = glob(folder_query)
    files_in_folder = [file for file in files_in_folder if 'chosen' not in file]
    output_file = '/data/tests/test_descriptions.json'

    for file in files_in_folder:
        print(f"Reading file: {file.split('/')[-1]}")
        df = pd.read_csv(
            file,
            sep=',',
            delim_whitespace=False
        ).rename(columns=lambda x: x.strip())
        fig, ax = plt.subplots()
        ax.plot(df['Resistance'])
        ax.set_title(file.split('/')[-1])
        plt.show()
        use = input('use current file? (y/'')')
        if use != '':
            detection_number = 0
            detection_periods = []
            while True:
                start_time = input(f'Input the start of detection {detection_number}')
                if start_time == '!':
                    break
                end_time = input(f'Input the end of detection {detection_number}')
                if end_time == '!':
                    break
                elif end_time == '-1':
                    end_time = len(df)
                detection_number+=1
                detection_period = (int(start_time), int(end_time))
                detection_periods.append(detection_period)

            file_name = input('Input name descriptor for current file')
            if file_name=='':
                file_name = file.split('/')[-1].split('.')[0]
            detections_list = [make_detection_from_period_tuple(period) for period in detection_periods]
            output_dict = {
                file_name: {
                    "Anomalies": detections_list,
                    "Path" : file
                }
            }
            with open(output_file, 'r') as output_json_file:
                current_json = json.loads(output_json_file.read())

            with open(output_file, 'w') as output_json_file:
                current_json['Tests'].append(output_dict)
                output_json_file.write(json.dumps(current_json, indent = 4))
            new_file_name = file
            new_file_name_split = new_file_name.split('/')
            new_file_name_split[-1] = '.'.join([new_file_name_split[-1].split('.')[0]+'_chosen', new_file_name_split[-1].split('.')[-1]])
            new_file_name = '/'.join(new_file_name_split)
            os.rename(file, new_file_name)
        else:
            new_file_name = file
            new_file_name_split = new_file_name.split('/')
            new_file_name_split[-1] = '.'.join([new_file_name_split[-1].split('.')[0]+'_discarded', new_file_name_split[-1].split('.')[-1]])
            new_file_name = '/'.join(new_file_name_split)
            os.rename(file, new_file_name)