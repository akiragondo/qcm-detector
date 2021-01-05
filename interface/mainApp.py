from .mainWindow import Ui_MainWindow
from comms.rs232 import list_serial_ports,RS232
import pyqtgraph as pg
from PyQt5 import QtCore,QtWidgets
from utils.utils import DateAxisItem
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class MainApp(Ui_MainWindow):
    def __init__(self,window):
        #UI Setup
        self.setupUi(window)

        # Insert in window
        # date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation = 'bottom')
        # self.graphWidget = PlotWidget(self.gridLayoutWidget,
        #                               title="Resistance Measurement",
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

        #Plotting setup

        #update viewbox
        self.updateViews()
        self.plotLine.getViewBox().sigResized.connect(self.updateViews)

        #Interactions - Connections
        self.refresh_ports_combo()
        self.refreshButton.clicked.connect(self.refresh_ports_combo)
        self.is_connected = False
        self.connectButton.clicked.connect(self.connectButtonHandler)


        #QCM Setup
        self.output_folder = '/Users/akira/soft/Qt Projects/rtqcm/data/'
        self.rs = RS232()
        self.index = 0

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePlot)


    def updateViews(self):
        self.twinGraph.setGeometry(self.plotLine.getViewBox().sceneBoundingRect())
        self.twinGraph.linkedViewChanged(self.plotLine.getViewBox(), self.twinGraph.XAxis)

    def updatePlot(self):
        data = self.rs.read_data()
        if data != None:
            print ('Time: {} - Res: {} - Freq - {}'.format(data['Time'], data['Resistance'], data['Frequency']))
            self.index += 1

        if self.index % 2 == 0:
            self.plotLine.setData(self.rs.results[:,0], self.rs.results[:,2])
            self.twinLine.setData(self.rs.results[:,0], self.rs.results[:,1])

        if self.index %10 == 0:
            self.rs.append_to_csv()

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

            #Disconnect
            self.progressBar.setValue(0)
            self.resultsLabel.setText('')

            self.portComboBox.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.emailField.setEnabled(self.checkBox.isChecked())
            self.emailTestButton.setEnabled(True)
            self.refreshButton.setEnabled(True)
        else:
            #Connect
            port = self.portComboBox.currentText()
            gate_time = 1000
            scale_factor = 200
            self.rs.set_output_file(self.output_folder)
            result = self.rs.establish_connection(port_name=port, gate_time=gate_time, scale_factor=scale_factor)
            if result == 0:
                self.toggle_connect()
                #Connected - Waiting Stabilization
                #Stabilised - Training Model
                #Ready
                self.progressBar.setValue(20)
                self.resultsLabel.setText('Connected - Waiting Stabilization')

                self.connectButton.setText('Cancel')
                #Disable all buttons
                self.portComboBox.setEnabled(False)
                self.checkBox.setEnabled(False)
                self.emailField.setEnabled(False)
                self.emailTestButton.setEnabled(False)
                self.refreshButton.setEnabled(False)
                self.timer.start()



