from PyQt5.QtCore import QMutex
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from models.connection_parameters import ConnectionParameters
from detectors.detection_voter import DetectionVoter
from models.qcm_model import QCMModel
from api.rs232 import RS232
from typing import List
from models.detection import Detection
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")
import tqdm
import json
import time


class TestController:
    def __init__(self):
        self.rs_api = RS232()
        self.data_model = QCMModel()
        self.detector = DetectionVoter(run_controller=self)
        self.mutex = QMutex()

        self.read_time = 1
        self.detection_period = 60

        self.detection_time_period = 5

    def get_anomaly_timestamp_dicts(self, anomalies_object : dict, rs_api : RS232):
        assert(len(rs_api.simulation_data > 0))
        anomaly_list = []
        for anomaly in anomalies_object:
            start = rs_api.datetime_to_float(rs_api.simulation_data.index[int(anomaly['Start'])])
            end = rs_api.datetime_to_float(rs_api.simulation_data.index[int(anomaly['End'])-1])
            anomaly_dict ={'Start': start, 'End': end}
            anomaly_list.append(anomaly_dict)
        return anomaly_list

    def get_single_file_predictions(self, file_name):
        connections_params = ConnectionParameters(
            port_name='',
            scale_factor=200,
            gate_time=1000,
            simulation_data_path = file_name,
            output_data_file= ''
        )
        self.rs_api.establish_connection(connections_params,is_simulated=True)
        for i in tqdm.tqdm(range(self.rs_api.simulationLength)):
            current_reading = self.rs_api.read_data()
            self.data_model.append_sample(current_reading)
            if i % self.detection_time_period == 0 and i > self.detection_time_period:
                self.detector.detect()
        detections = self.detector.past_detections
        return detections

    def get_results_from_test(self, test, detections, detection_time):
        test_object = test[list(test.keys())[0]]
        test_anomalies = self.get_anomaly_timestamp_dicts(test_object['Anomalies'], self.rs_api)
        true_positives = [detection.__dict__ for detection in self.get_true_positives(detections, test_anomalies)]
        false_negatives = self.get_false_negatives(detections, test_anomalies)
        recall = float(len(true_positives)/(len(true_positives) + len(false_negatives))) if len(true_positives) + len(false_negatives) > 0 else 0
        result = {
            list(test.keys())[0]: {
                "Detections": [detection.__dict__ for detection in detections],
                "Anomalies": test_anomalies,
                "Number of detections": len(detections),
                "True Positives": true_positives,
                "False Negatives": false_negatives,
                "Number of True Positives": len(true_positives),
                "Number of False Positives": len(detections) - len(true_positives),
                "Number of False Negatives": len(false_negatives),
                "Number of True Negatives": len(test_anomalies) - len(false_negatives),
                "Total Detection Time": detection_time,
                "Recall": recall,
                "Path": test_object['Path']
            }
        }
        return result

    def get_false_negatives(self, detections, test_anomalies):
        false_negatives = [anomaly for anomaly in test_anomalies if not self.detected_anomaly(detections, anomaly)]
        return false_negatives

    def get_true_positives(self, detections, test_anomalies):
        true_positives = [detection for detection in detections if self.is_detection_within_anomalies(
            detection,
            test_anomalies
        )]
        return true_positives


    def test(self, json_test_descriptors):
        with open(json_test_descriptors, 'r') as test_json_file:
            input_file = json.loads(test_json_file.read())
        tests = input_file['Tests']
        results = {}
        for test in tests:
            self.detector.reset()
            self.data_model.reset_model()
            test_path = test[list(test.keys())[0]]['Path']
            print(f"Testing: {test_path.split('/')[-1]}")
            start_time = time.time()
            detections = self.get_single_file_predictions(test_path)
            total_detection_time = time.time() - start_time
            result = self.get_results_from_test(test, detections, total_detection_time)
            results.update(result)
            with open('results.json', 'w+') as output_file:
                output_file.write(json.dumps(results, indent=4))


    def test_correct_detection(self, detection):
        return self.rs_api.simulation_data.loc[detection.time][' Label'] == 1

    def is_detection_within_anomalies(self, detection, anomalies):
        for anomaly in anomalies:
            if anomaly['Start'] < detection.timestamp < anomaly['End']:
                return True
        return False

    def detected_anomaly(self, detections, anomaly):
        for detection in detections:
            if anomaly['Start'] < detection.timestamp < anomaly['End']:
                return True
        return False


if __name__ == '__main__':
    ts = TestController()
    print(ts.test('/home/kimino/soft/qcm-detector/data/tests/test_descriptions_short.json'))

