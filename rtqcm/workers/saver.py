from PyQt5.QtCore import (
    QObject,
    QMutex
)
import datetime
from rtqcm.models.qcm_model import QCMModel
import os
import numpy as np

class Saver(QObject):

    def __init__(self, parent_mutex: QMutex):
        super().__init__()
        self.saved_header = False
        self.lines_saved = 0
        self.output_path = None
        self.header_template = 'Timestamps, Frequency, Resistance\n'
        self.mutex = parent_mutex

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

    def save_header(self, output_path):
        with open(output_path, 'w+') as f:
            f.write(self.header_template)
            self.saved_header = True

    def format_line(self, results_sample):
        dt = datetime.datetime.fromtimestamp(results_sample[0])
        formatted_sample_time = f"{dt.day}/{dt.month}/{dt.year} {dt.hour}:{dt.minute}:{dt.second}.{dt.microsecond}"
        line = f"{formatted_sample_time}, {results_sample[1]:.3f}, {results_sample[2]:.3f}"
        return line

    def append_save(self, qcm_model: QCMModel, output_path):
        if not self.saved_header:
            if self.file_already_exists(output_path):
                self.output_path = self.make_non_overwrite_name(output_path)
            else:
                self.output_path = output_path
            self.save_header(self.output_path)
            self.saved_header = True
        # Append new lines
        self.mutex.lock()
        full_results = qcm_model.get_full_results_as_samples()
        self.mutex.unlock()
        if len(full_results) > 0:
            results = full_results[self.lines_saved:]
            self.save_lines(results, self.output_path)
            self.lines_saved = len(full_results)

    def save_lines(self, results, output_path):
        formatted_lines = "\n".join([self.format_line(result) for result in results])
        try:
            with open(output_path, 'a') as append_file:
                append_file.write(formatted_lines)
                append_file.write('\n')
        except IOError as e:
            raise e
