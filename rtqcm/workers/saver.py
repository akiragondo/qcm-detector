from PyQt5.QtCore import (
    QObject,
    QMutex
)
import datetime
from rtqcm.models.qcm_model import QCMModel
import os
from typing import List
from rtqcm.models.detection import Detection

class Saver(QObject):

    def __init__(self, parent_qcm_model_mutex: QMutex, parent_detection_list_mutex: QMutex):
        super().__init__()
        self.saved_header_samples = False
        self.saved_header_detection = False
        self.lines_saved_samples = 0
        self.lines_saved_detections = 0
        self.samples_output_path = None
        self.detections_output_path = None
        self.samples_header_template = 'Timestamp, Frequency, Resistance\n'
        self.detections_header_template = 'Timestamp, Detector, Severity, Frequency, Resistance\n'
        self.qcm_model_mutex = parent_qcm_model_mutex
        self.detection_list_mutex = parent_detection_list_mutex

    def file_already_exists(self, path):
        return os.path.exists(path)

    def make_non_overwrite_name(self, output_path:str):
        if not self.file_already_exists(output_path):
            return output_path
        else:
            #Make files with incremental numbers
            split_extension = output_path.split('.')
            base_name = split_extension[0]
            extensions = '.'.join(split_extension[1:])
            incremental_number = 1
            test_file_name = f"{base_name}_{incremental_number}.{extensions}"
            while self.file_already_exists(test_file_name):
                incremental_number +=1
                test_file_name = f"{base_name}_{incremental_number}.{extensions}"
            return test_file_name

    def save_header_samples(self, output_path):
        with open(output_path, 'w+') as f:
            f.write(self.samples_header_template)
            self.saved_header_samples = True

    def save_header_detections(self, output_path):
        with open(output_path, 'w+') as f:
            f.write(self.detections_header_template)
            self.saved_header_detection = True

    def format_sample_line(self, results_sample):
        dt = datetime.datetime.fromtimestamp(results_sample[0])
        formatted_sample_time = f"{dt.day}/{dt.month}/{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}.{dt.microsecond}"
        line = f"{formatted_sample_time}, {results_sample[1]:.3f}, {results_sample[2]:.3f}"
        return line

    def append_save_samples(self, qcm_model: QCMModel, output_path):
        if not self.saved_header_samples:
            if self.file_already_exists(output_path):
                self.samples_output_path = self.make_non_overwrite_name(output_path)
            else:
                self.samples_output_path = output_path
            self.save_header_samples(self.samples_output_path)
            self.saved_header_samples = True
        # Append new lines
        self.qcm_model_mutex.lock()
        full_results = qcm_model.get_full_results_as_samples()
        self.qcm_model_mutex.unlock()
        if len(full_results) > 0:
            results = full_results[self.lines_saved_samples:]
            self.save_lines_samples(results, self.samples_output_path)
            self.lines_saved_samples = len(full_results)

    def save_lines_samples(self, results, output_path):
        formatted_lines = "\n".join([self.format_sample_line(result) for result in results])
        try:
            with open(output_path, 'a') as append_file:
                append_file.write(formatted_lines)
                append_file.write('\n')
        except IOError as e:
            raise e

    def format_detection_line(self, detection: Detection):
        dt = datetime.datetime.fromtimestamp(detection.timestamp)
        formatted_sample_time = f"{dt.day}/{dt.month}/{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}.{dt.microsecond}"
        line = f"{formatted_sample_time}, {detection.detector}, {detection.severity}, {detection.frequency:.3f}, {detection.resistance:.3f}"
        return line

    def save_lines_detections(self, detections, output_path):
        if len(detections) > 0:
            formatted_lines = "\n".join([self.format_detection_line(detection) for detection in detections])
            try:
                with open(output_path, 'a') as append_file:
                    append_file.write(formatted_lines)
                    append_file.write('\n')
            except IOError as e:
                raise e

    def append_save_detections(self, detections: List[Detection], output_path):
        print(f'Saved detections: {detections}')
        detection_output = output_path.split('.')[0] + '_detections.' + output_path.split('.')[-1]
        if not self.saved_header_detection:
            if self.file_already_exists(detection_output):
                self.detections_output_path = self.make_non_overwrite_name(detection_output)
            else:
                self.detections_output_path = detection_output
            self.save_header_detections(self.detections_output_path)
            self.saved_header_detection = True
        # Append new lines
        self.detection_list_mutex.lock()
        full_results = detections
        self.detection_list_mutex.unlock()
        if len(full_results) > 0:
            results = full_results[self.lines_saved_detections:]
            self.save_lines_detections(results, self.detections_output_path)
            self.lines_saved_detections = len(full_results)