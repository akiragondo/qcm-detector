from .mainWindow import Ui_MainWindow
from comms.rs232 import list_serial_ports, RS232
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from detectors.stability import isStable
from datetime import datetime
from detectors.mainDetector import MainDetector
from comms.email import EmailComm
import pandas as pd
import numpy as np
import json

class MainApp(Ui_MainWindow):
    def __init__(self, window):
        # UI Setup
        self.setupUi(window)
        self.window = window
        self.state = 0
        self.print = False
        """
            Code: 
                red/orange -> Contaminations serious/mild
                blue -> system operations (connection, disconnection, detection begins)
                white -> system errors (timeouts)
        """
        self.colors = {
            "red" : "#B80000",
            "blue" : "#027CA1",
            "white" : "#F3F6F5",
            "orange" : "#FF8811"
        }

        # Time configurations
        self.stabilizationTime = 300
        self.visibleTime = 60 * 30
        self.drawPeriod = 5
        self.detectPeriod = 60
        self.savePeriod = 30

        # update viewbox
        self.updateViews()
        self.plotLine.getViewBox().sigResized.connect(self.updateViews)

        # Interactions - Connections
        self.is_simulated = False
        self.refresh_ports_combo()
        self.refreshButton.clicked.connect(self.refresh_ports_combo)
        self.is_connected = False
        self.connectButton.clicked.connect(self.connectButtonHandler)
        self.connectionTypeComboBox.currentTextChanged.connect(self.toggleSimulatorPort)
        self.searchButton.clicked.connect(self.searchOutputDirectory)
        self.emailTestButton.connect(self.verifyEmail)

        # QCM Setup
        self.rs = RS232()
        self.index = 0

        #Detector Setup
        self.detector = MainDetector()

        #Email Comm Setup
        self.comm = EmailComm()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePlot)



        # date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation = 'bottom')
        # self.graphWidget = PlotWidget(self.verticalLayoutWidget,
        #                               axisItems = {'bottom': date_axis}
        #                               )
        # self.graphWidget.setMouseEnabled(x=False, y=False)
        # self.graphWidget.setBackground(None)
        # self.graphWidget.setObjectName("graphWidget")
        #
        # #First axis setup
        # self.plotLine = self.graphWidget.plot(pen = pg.mkPen(color='#027CA1', width=3))
        # self.graphWidget.showAxis('left')
        # self.graphWidget.setLabel('left', 'Resistance', units="<font>&Omega;</font>",
        #                           color='#027CA1', **{'font-size':'14pt'})
        # self.graphWidget.getAxis('left').enableAutoSIPrefix(False)
        # #Second axis setup
        # self.graphWidget.showAxis('right')
        # self.graphWidget.setLabel('right', 'Frequency', units="<font>Hz</font>",
        #                           color='#FF8811', **{'font-size':'14pt'})
        # # self.graphWidget.getAxis('right').setPen(pg.mkPen(color='#F3F6F5', width=3))
        #
        # self.twinGraph = pg.ViewBox()
        # self.graphWidget.scene().addItem(self.twinGraph)
        # self.graphWidget.getAxis('right').linkToView(self.twinGraph)
        # self.twinGraph.setXLink(self.graphWidget)
        #
        # self.twinLine = pg.PlotCurveItem(pen = pg.mkPen(color='#FF8811',width=3))
        # self.twinGraph.addItem(self.twinLine)
        self.textBrowser.clear()

    def verifyEmail(self):
        self.comm.verifyEmail(self.emailField.text())

    def sendDetectionEmail(self, plot_data : np.ndarray, detectionDescription : str, severity : str, detectionTimestamp : int):
        """
        :param plot_data: np array of time, frequency and resistance in samples of 10 seconds
        :param detectionDescription: description of the detection made
        :return: result of sending email
        """
        timestamps  = plot_data[:,0]
        resistances  = plot_data[:,0]
        frequencies  = plot_data[:,0]
        body = {
            "to" : self.emailField.text(),
            "subject" : "{} Severity contamination detected",
            "data" : {
                "timestamps" : timestamps,
                "resistances" : resistances,
                "frequencies" : frequencies
            }
            "detection": {
                "timestamp": detectionTimestamp,
                "description" : detectionDescription,
                "severity" : severity
            }
        }
        jsonBody = json.dumps(body)
        self.comm.sendEmail(jsonBody)


    def addPastEvent(self, time, description, color):
        """
        :param time: time in timestamp from the results
        """
        timeText = datetime.fromtimestamp(time).strftime("%H:%M - %d/%m/%Y")
        content = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; " \
                  "-qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:{};\">•</span><span style=\"font-family:\'arial\',\'sans-serif\'; " \
                  "font-size:14px; color:#f3f6f5;\"> {} - {}</span></p></td></tr></table>\n".format(color,
                                                                                                    timeText,
                                                      description)
        content = content + self.textBrowser.toHtml()
        self.textBrowser.setText(content)

    def currentTime(self):
        return(self.rs.datetime_to_float(datetime.now()))

    def searchOutputDirectory(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Select Data Output Directory"))
        self.outputField.setText(file)

    def toggleSimulatorPort(self):
        if self.connectionTypeComboBox.currentText() == 'Simulation File':
            self.is_simulated = True
            self.timer.setInterval(1000 / 60)
            self.refreshButton.setText('Search')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.searchSimulatorFile)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.is_simulated = False
            self.timer.setInterval(1000)
            self.refreshButton.setText('Refresh')
            self.refreshButton.clicked.disconnect()
            self.refreshButton.clicked.connect(self.refresh_ports_combo)
            self.stackedWidget.setCurrentIndex(0)

    def add_vline(self, x):
        new_line = pg.InfiniteLine(pos=x)
        self.plotLine.getViewBox().addItem(new_line)

    def searchSimulatorFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.window, "Select Simulator File")
        self.dataFileField.setText(str(file[0]))

    def updateViews(self):
        self.twinGraph.setGeometry(self.plotLine.getViewBox().sceneBoundingRect())
        self.twinGraph.linkedViewChanged(self.plotLine.getViewBox(), self.twinGraph.XAxis)

    def updatePlot(self):
        data = self.rs.read_data()
        if data != None:
            if self.print:
                print('Time: {} - Res: {} - Freq - {}'.format(data['Time'], data['Resistance'], data['Frequency']))
            self.index += 1

        if self.index >= self.stabilizationTime and self.state == 1 and self.index % self.stabilizationTime / 2 == 0:
            sample = self.rs.results[:, 2][-self.stabilizationTime:]
            if isStable(sample, self.stabilizationTime):
                self.state = 2
                self.addPastEvent(self.rs.results[:,0][-1], 'System stabilized', self.colors['blue'])
                self.resultsLabel.setText('Ready')
                self.progressBar.setValue(100)
                self.add_vline(self.rs.results[:, 0][-1])

        if self.state > 1 and self.index % self.detectPeriod == 0:
            detection = self.detector.detectAnomaly(sample=self.rs.results[:][-self.detectPeriod:])
            if detection > 0:
                if detection == 1:
                    self.addPastEvent(self.rs.results[:, 0][-1], 'Mild Anomaly Detected', self.colors['orange'])

                if detection == 2:
                    self.addPastEvent(self.rs.results[:, 0][-1], 'Severe Anomaly Detected', self.colors['red'])


        if self.index % self.savePeriod == 0:
            self.rs.append_to_csv()


        if self.index % self.drawPeriod == 0:
            self.plotLine.setData(self.rs.results[:, 0], self.rs.results[:, 2])
            self.twinLine.setData(self.rs.results[:, 0], self.rs.results[:, 1])
            # Update X Range
            if (self.rs.results[:, 0][-1] - self.rs.results[:, 0][0] > self.visibleTime):
                self.plotLine.getViewBox().setXRange(self.rs.results[:, 0][-1] - self.visibleTime,
                                                     self.rs.results[:, 0][-1])



    def toggle_connect(self):
        self.is_connected = not self.is_connected

    def refresh_ports_combo(self):
        ports_list = list_serial_ports()
        self.portComboBox.clear()
        for port in ports_list:
            self.portComboBox.addItem(port)

    def connectButtonHandler(self):
        if self.is_connected:
            self.toggle_connect()
            self.connectButton.setText('Connect')
            self.timer.stop()

            self.rc = RS232()

            # Disconnect
            self.state = 0
            self.progressBar.setValue(0)
            self.resultsLabel.setText('')

            self.portComboBox.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.emailField.setEnabled(self.checkBox.isChecked())
            self.emailTestButton.setEnabled(True)
            self.refreshButton.setEnabled(True)
            self.fileName.setEnabled(True)
        else:
            # Connect
            port = self.portComboBox.currentText()
            gate_time = 1000
            scale_factor = 200
            output_folder = self.outputField.text()
            if output_folder[-1] != '/':
                output_folder += '/'
            self.rs.set_output_file(output_folder, self.fileName.text())
            result = self.rs.establish_connection(
                port_name=port,
                gate_time=gate_time,
                scale_factor=scale_factor,
                is_simulated=self.is_simulated,
                simulation_data_path=self.dataFileField.text()
            )
            if result == 0:
                self.toggle_connect()
                self.state = 1
                self.addPastEvent(self.currentTime(), 'Connection started', self.colors['blue'])
                # Connected - Waiting Stabilization
                # Stabilised - Training Model
                # Ready
                self.progressBar.setValue(20)
                self.resultsLabel.setText('Connected - Waiting Stabilization')

                self.connectButton.setText('Cancel')
                # Disable all buttons
                self.portComboBox.setEnabled(False)
                self.checkBox.setEnabled(False)
                self.emailField.setEnabled(False)
                self.emailTestButton.setEnabled(False)
                self.refreshButton.setEnabled(False)
                self.fileName.setEnabled(False)
                self.timer.start()
