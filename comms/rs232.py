import sys
import glob

import serial
import enum
import datetime
import numpy as np
import pandas as pd
from time import sleep
from os.path import exists

import signal

scaleFactors = {
    200 : 0,
    500 : 1,
    1000 : 2,
    2000 : 3,
    5000 : 4,
    10000 : 5,
    20000 : 6
}

gateTimes = {
    100 : 0,
    1000 : 1,
    10000 : 2
}


class Status(enum.Enum):
    QueryF = 1
    WaitF = 2
    QueryR = 3
    WaitR = 4
    Finished = 5

class RS232:

    def __init__(self):
        self.ser = None
        self.gate_time = None
        self.scale_factor = None
        self.readings = pd.Series([])
        self.results = np.array([])

        self.output_file = None
        self.wrote_header = False

        self.request_timedout = False

    def establish_connection(self, port_name, gate_time, scale_factor):
        self.ser = serial.Serial(
            baudrate=9600,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=1,
            port = port_name
        )
        self.gate_time = gate_time
        self.scale_factor = scale_factor
        try:
            self.ser.isOpen()
            self.set_metadata(gate_time=self.gate_time, scale_factor=self.scale_factor)
            signal.signal(signal.SIGALRM, self.timeout_handler)
            print('Connection established! port: {}'.format(port_name))
            return 0
        except Exception:
            raise(Exception)
            return 1

    def set_metadata(self, gate_time, scale_factor):
        assert(gate_time in gateTimes and scale_factor in scaleFactors)
        self.ser.write('P{}\r'.format(gateTimes[gate_time]).encode())
        sleep(1)
        self.ser.write('D{}\r'.format(scaleFactors[scale_factor]).encode())

    def set_output_file(self, output_folder):
        output_base_name = output_folder + datetime.datetime.now().strftime("%y-%m-%d_data")
        if exists(output_base_name + '.csv'):
            output_base_name = output_folder + datetime.datetime.now().strftime("%y-%m-%d")
            i = 1
            while exists("{}_{}-data.csv".format(output_base_name, i)):
                i += 1
            self.output_file = "{}_{}-data.csv".format(output_base_name, i)
        else:
            self.output_file = "{}.csv".format(output_base_name)
        self.wrote_header = False

    def timeout_handler(self,signum, frame):
        self.request_timedout = True
        print('timeout')

    def read_data(self):
        #Input: none #Output: packet with [time, resistance, frequency]
        query_status = Status.QueryF
        dt = np.dtype([('Time', np.unicode, 32), ('Frequency', np.float64), ('Resistance', np.float64)])
        frequency = None
        resistance = None
        self.request_timedout = False

        signal.alarm(5)
        while(query_status != Status.Finished and not self.request_timedout):
            try:
                if(query_status == Status.QueryF):
                    self.ser.write('F\r'.encode())
                    query_status = Status.WaitF
                elif(query_status==Status.WaitF):
                    if(self.ser.inWaiting()>0):
                        frequency = float(self.ser.readline())
                        self.ser.write('R\r'.encode())
                        query_status = Status.WaitR
                elif(query_status==Status.WaitR):
                    if(self.ser.inWaiting()>0):
                        resistance = float(self.ser.readline())
                        query_status = Status.Finished
            except:
                return None

        if self.request_timedout:
            return None
        else:
            signal.alarm(0)
            d = datetime.datetime.now()
            time = "{d.day}/{d.month}/{d.year} {d.hour}:{d.minute}:{d.second}.{d.microsecond}".format(d=d)
            data_packet = np.array((time, frequency, resistance), dtype= dt)
            new_pd = pd.Series(data_packet)
            d = datetime_to_float(d)
            if len(self.results) == 0:
                self.results = np.array([d, frequency, resistance])
            else:
                self.results = np.vstack((self.results, [d, frequency, resistance]))
            self.readings = self.readings.append(new_pd)
            return(data_packet)


    def append_to_csv(self):
        if self.output_file!= None:
            if not self.wrote_header:
                content = 'Time, Frequency, Resistance \n'
                for reading in self.readings:
                    content = content + ('{}, {}, {}\n'.format(reading['Time'],reading['Frequency'],reading['Resistance']))
                self.wrote_header = True

                file = open(self.output_file, 'w')
                file.write(content)
                file.close()
                self.readings = pd.Series([])
                return 0
            else:
                content = ''
                for reading in self.readings:
                    content = content + ('{}, {}, {}\n'.format(reading['Time'],reading['Frequency'],reading['Resistance']))

                file = open(self.output_file, 'a')
                file.write(content)
                file.close()
                self.readings = pd.Series([])
                return 0
        return 1

def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def list_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/cu[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/cu.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

