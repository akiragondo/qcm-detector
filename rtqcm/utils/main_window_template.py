# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui-quegay.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from qtwidgets import AnimatedToggle
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import ui_rc


class MainWindowTemplate(QtCore.QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1280, 747)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QWidget{background:color: #F3F6F5}")
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("QWidget{background-color: #F3F6F5;}")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, -1, 1281, 793))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QtWidgets.QWidget(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(320, 791))
        self.widget.setStyleSheet("QWidget{\n"
                                  "    background-color: #052034;\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 175, 321, 661))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(20, 0, 20, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayoutToggle = QtWidgets.QHBoxLayout()
        self.horizontalLayoutToggle.setObjectName("horizontalLayoutToggle")
        self.labelToggle = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelToggle.sizePolicy().hasHeightForWidth())
        self.labelToggle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelToggle.setFont(font)
        self.labelToggle.setStyleSheet("color: #f3f6f5;")
        self.labelToggle.setLineWidth(0)
        self.labelToggle.setObjectName("labelToggle")
        self.horizontalLayoutToggle.addWidget(self.labelToggle)
        self.horizontalLayoutToggle.addStretch()
        self.horizontalLayoutToggle.setSpacing(0)


        self.simulationToggle = AnimatedToggle(
            parent=self.verticalLayoutWidget_2,
            checked_color= '#025D79',
            pulse_checked_color='#44027CA1',
        )
        self.simulationToggle.setStyleSheet(
            "background-color: white; margin=0;padding=0;"
        )
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationToggle.sizePolicy().hasHeightForWidth())
        self.simulationToggle.setSizePolicy(sizePolicy)

        # self.simulationToggle.setMinimumSize(QtCore.QSize(100, 30))
        # self.simulationToggle.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayoutToggle.addWidget(self.simulationToggle)
        self.horizontalLayoutToggle.setSpacing(0)

        self.verticalLayout.addLayout(self.horizontalLayoutToggle)


        self.horizontalLayoutToggle.addWidget(self.simulationToggle)
        self.connectionTypeLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.connectionTypeLabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectionTypeLabel.sizePolicy().hasHeightForWidth())
        self.connectionTypeLabel.setSizePolicy(sizePolicy)
        self.connectionTypeLabel.setMinimumSize(QtCore.QSize(160, 49))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.connectionTypeLabel.setFont(font)
        self.connectionTypeLabel.setStyleSheet("QComboBox{color: #f3f6f5; "
                                                  "padding-left: 0px;}\n "
                                                  "\n"
                                                  "QComboBox:disabled,\n"
                                                  "QComboBox[disabled]{\n"
                                                  "  color: light gray;\n"
                                                  "}")
        self.connectionTypeLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.connectionTypeLabel.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.connectionTypeLabel.setObjectName("connectionTypeLabel")
        self.connectionTypeLabel.setStyleSheet("color: #f3f6f5;")
        self.connectionTypeLabel.setLineWidth(0)
        self.horizontalLayout.addWidget(self.connectionTypeLabel, 0, QtCore.Qt.AlignLeft)
        self.refreshButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.refreshButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setMinimumSize(QtCore.QSize(100, 30))
        self.refreshButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.refreshButton.setFont(font)
        self.refreshButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refreshButton.setStyleSheet("QPushButton{\n"
                                         "    background-color: #025D79;\n"
                                         "     border-radius: 15px;\n"
                                         "  color: #f3f6f5;}\n"
                                         "\n"
                                         "QPushButton::hover{\n"
                                         "    background-color: #027CA1;\n"
                                         " }\n"
                                         "\n"
                                         "QPushButton:disabled,\n"
                                         "QPushButton[disabled]{\n"
                                         "  color: light gray;\n"
                                         "}")
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.verticalLayoutWidget_2)
        self.stackedWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(0, 35))
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.portComboBox = QtWidgets.QComboBox(self.page)
        self.portComboBox.setEnabled(True)
        self.portComboBox.setGeometry(QtCore.QRect(0, 0, 280, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portComboBox.sizePolicy().hasHeightForWidth())
        self.portComboBox.setSizePolicy(sizePolicy)
        self.portComboBox.setMinimumSize(QtCore.QSize(21, 35))
        self.portComboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.portComboBox.setFont(font)
        self.portComboBox.setStyleSheet("QComboBox{border-radius:15px; background-color: #022B3B;  color: #f3f6f5;}\n"
                                        "\n"
                                        "QComboBox:disabled,\n"
                                        "QComboBox[disabled]{\n"
                                        "  color: light gray;\n"
                                        "}")
        self.portComboBox.setIconSize(QtCore.QSize(39, 26))
        self.portComboBox.setFrame(False)
        self.portComboBox.setObjectName("portComboBox")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.dataFileField = QtWidgets.QLineEdit(self.page_2)
        self.dataFileField.setEnabled(True)
        self.dataFileField.setGeometry(QtCore.QRect(0, 0, 281, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataFileField.sizePolicy().hasHeightForWidth())
        self.dataFileField.setSizePolicy(sizePolicy)
        self.dataFileField.setMinimumSize(QtCore.QSize(0, 30))
        self.dataFileField.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.dataFileField.setStyleSheet(
            "QLineEdit{background-color: #022B3B; border-radius:15px; padding: 0px 6px;color:#F3F6F5;  border: 0; "
            "outline: none;}\n "
            "\n"
            "QLineEdit:disabled[text=\"\"],\n"
            "QLineEdit[disabled][text=\"\"]{\n"
            "  color: #555555;\n"
            "}")
        self.dataFileField.setText("")
        self.dataFileField.setObjectName("dataFileField")
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: #f3f6f5;")
        self.label_8.setLineWidth(0)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8, 0, QtCore.Qt.AlignVCenter)
        self.searchButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.searchButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(100, 30))
        self.searchButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.searchButton.setFont(font)
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchButton.setStyleSheet("QPushButton{\n"
                                        "    background-color: #025D79;\n"
                                        "     border-radius: 15px;\n"
                                        "  color: #f3f6f5;}\n"
                                        "\n"
                                        "QPushButton::hover{\n"
                                        "    background-color: #027CA1;\n"
                                        " }\n"
                                        "\n"
                                        "QPushButton:disabled,\n"
                                        "QPushButton[disabled]{\n"
                                        "  color: light gray;\n"
                                        "}")
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_10.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.outputField = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.outputField.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputField.sizePolicy().hasHeightForWidth())
        self.outputField.setSizePolicy(sizePolicy)
        self.outputField.setMinimumSize(QtCore.QSize(0, 30))
        self.outputField.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.outputField.setStyleSheet("QLineEdit{background-color: #022B3B; border-radius:15px; padding: 0px 6px;}\n"
                                       "\n"
                                       "QLineEdit{ color:#F3F6F5; }\n"
                                       "\n"
                                       "QLineEdit:disabled[text=\"\"],\n"
                                       "QLineEdit[disabled][text=\"\"]{\n"
                                       "  color: #555555;\n"
                                       "}")
        self.outputField.setText("")
        self.outputField.setFrame(True)
        self.outputField.setObjectName("outputField")
        self.verticalLayout.addWidget(self.outputField)
        self.fileName = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.fileName.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setMinimumSize(QtCore.QSize(0, 30))
        self.fileName.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.fileName.setStyleSheet("QLineEdit{background-color: #022B3B; border-radius:15px; padding: 0px 6px;}\n"
                                    "\n"
                                    "QLineEdit{ color:#F3F6F5; }\n"
                                    "\n"
                                    "QLineEdit:disabled[text=\"\"],\n"
                                    "QLineEdit[disabled][text=\"\"]{\n"
                                    "  color: #555555;\n"
                                    "}")
        self.fileName.setText("")
        self.fileName.setFrame(True)
        self.fileName.setObjectName("fileName")
        self.verticalLayout.addWidget(self.fileName)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #f3f6f5;")
        self.label_2.setLineWidth(0)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.emailTestButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.emailTestButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emailTestButton.sizePolicy().hasHeightForWidth())
        self.emailTestButton.setSizePolicy(sizePolicy)
        self.emailTestButton.setMinimumSize(QtCore.QSize(100, 30))
        self.emailTestButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.emailTestButton.setFont(font)
        self.emailTestButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.emailTestButton.setStyleSheet("QPushButton{\n"
                                           "    background-color: #025D79;\n"
                                           "     border-radius: 15px;\n"
                                           "  color: #f3f6f5;}\n"
                                           "\n"
                                           "QPushButton::hover{\n"
                                           "    background-color: #027CA1;\n"
                                           " }\n"
                                           "\n"
                                           "QPushButton:disabled,\n"
                                           "QPushButton[disabled]{\n"
                                           "  color: light gray;\n"
                                           "}")
        self.emailTestButton.setObjectName("emailTestButton")
        self.horizontalLayout_2.addWidget(self.emailTestButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setEnabled(True)
        self.checkBox.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox.setStyleSheet("QCheckBox{ color: #f3f6f5;}\n"
                                    "QCheckBox:disabled,\n"
                                    "QCheckBox[disabled]{\n"
                                    "  color: light gray;\n"
                                    "}")
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.emailField = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.emailField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emailField.sizePolicy().hasHeightForWidth())
        self.emailField.setSizePolicy(sizePolicy)
        self.emailField.setMinimumSize(QtCore.QSize(0, 30))
        self.emailField.setStyleSheet("QLineEdit{background-color: #022B3B; border-radius:15px; padding: 0px 6px;}\n"
                                      "\n"
                                      "QLineEdit{ color:#F3F6F5; }\n"
                                      "QLineEdit[text=\"\"]{ color:#888888; }\n"
                                      "\n"
                                      "QLineEdit:disabled[text=\"\"],\n"
                                      "QLineEdit[disabled][text=\"\"]{\n"
                                      "  color: #555555;\n"
                                      "}")
        self.emailField.setText("")
        self.emailField.setObjectName("emailField")
        self.horizontalLayout_3.addWidget(self.emailField)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.connectButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.connectButton.setFont(font)
        self.connectButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connectButton.setStyleSheet("QPushButton{\n"
                                         "    background-color: #025D79;\n"
                                         "     border-radius: 15px;\n"
                                         "  color: #f3f6f5;}\n"
                                         "\n"
                                         "QPushButton::hover{\n"
                                         "    background-color: #027CA1;\n"
                                         " }")
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(76, 20))
        self.progressBar.setStyleSheet("QProgressBar {\n"
                                       "     border-radius: 10px;\n"
                                       "     background-color: #022B3B;\n"
                                       "    color: #f3f6f5;\n"
                                       " }\n"
                                       "\n"
                                       " QProgressBar::chunk {\n"
                                       "     background-color: #025D79;\n"
                                       "    border-radius: 10px\n"
                                       "}")
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.resultsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultsLabel.sizePolicy().hasHeightForWidth())
        self.resultsLabel.setSizePolicy(sizePolicy)
        self.resultsLabel.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.resultsLabel.setFont(font)
        self.resultsLabel.setStyleSheet("color: #F3F6F5;")
        self.resultsLabel.setLineWidth(0)
        self.resultsLabel.setText("")
        self.resultsLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.resultsLabel.setObjectName("resultsLabel")
        self.verticalLayout.addWidget(self.resultsLabel)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.logo = QtWidgets.QLabel(self.widget)
        self.logo.setGeometry(QtCore.QRect(30, 40, 181, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(0, 0))
        self.logo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/newPrefix/unnamed.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout_4.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setStyleSheet("QWidget{background-color:#022B3B; font-size:16px}")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widget_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 941, 731))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphWidget = PlotWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setObjectName("graphWidget")
        date_axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        self.graphWidget = PlotWidget(self.verticalLayoutWidget,
                                      axisItems={'bottom': date_axis}
                                      )
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget.setBackground(None)
        self.graphWidget.setObjectName("graphWidget")

        # First axis setup
        self.plotLine = self.graphWidget.plot(pen=pg.mkPen(color='#027CA1', width=3))
        self.graphWidget.showAxis('left')
        self.graphWidget.setLabel('left', 'Resistance', units="<font>&Omega;</font>",
                                  color='#027CA1', **{'font-size': '14pt'})
        self.graphWidget.getAxis('left').enableAutoSIPrefix(False)
        # Second axis setup
        self.graphWidget .showAxis('right')
        self.graphWidget.setLabel('right', 'Frequency', units="<font>Hz</font>",
                                  color='#FF8811', **{'font-size': '14pt'})
        # self.graphWidget.getAxis('right').setPen(pg.mkPen(color='#F3F6F5', width=3))

        self.twinGraph = pg.ViewBox()
        self.graphWidget.scene().addItem(self.twinGraph)
        self.graphWidget.getAxis('right').linkToView(self.twinGraph)
        self.twinGraph.setXLink(self.graphWidget)

        self.twinLine = pg.PlotCurveItem(pen=pg.mkPen(color='#FF8811', width=3))
        self.twinGraph.addItem(self.twinLine)
        self.verticalLayout_3.addWidget(self.graphWidget)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 0, 20, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #F3F6F5;")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setMinimumSize(QtCore.QSize(0, 10))
        self.line.setStyleSheet("color: #F3F6F5;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 10))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 70))
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_5.addWidget(self.textBrowser)
        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout_4.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.checkBox.toggled['bool'].connect(self.emailField.setEnabled)
        self.connectButton.clicked.connect(self.connectButton.toggle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QCM Contamination Detector"))
        self.connectionTypeLabel.setText(_translate("MainWindow", "Connection Port"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.dataFileField.setPlaceholderText(_translate("MainWindow", "Simulation Data File"))
        self.labelToggle.setText(_translate("MainWindow", "Real/Simulation"))
        self.label_8.setText(_translate("MainWindow", "Output Directory"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.outputField.setPlaceholderText(_translate("MainWindow", "Output Directory"))
        self.fileName.setPlaceholderText(_translate("MainWindow", "File Name"))
        self.label_2.setText(_translate("MainWindow", "Email Notification"))
        self.emailTestButton.setText(_translate("MainWindow", "Register Email"))
        self.checkBox.setText(_translate("MainWindow", "Enabled"))
        self.emailField.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Past Events"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:16px; font-weight:400; font-style:normal;\">\n"
                                            "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; border-collapse:collapse;\" cellspacing=\"2\" cellpadding=\"0\" bgcolor=\"#ffffff\">\n"
                                            "<tr>\n"
                                            "<td style=\" vertical-align:top; padding-left:10; padding-right:10; padding-top:8; padding-bottom:8;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\',\'sans-serif\'; font-size:14px; color:#3dadfa;\">• </span><span style=\" font-family:\'arial\',\'sans-serif\'; font-size:14px; color:#ebf4fa;\">12:23 07/01/2021 - Training Finished</span><span style=\" font-family:\'arial\',\'sans-serif\'; font-size:14px; color:#ceff09;\"> </span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\',\'sans-serif\'; font-size:14px; color:#fc0006;\">•</span><span style=\" font-family:\'arial\',\'sans-serif\'; font-size:14px; color:#f3f6f5;\"> 16:39 07/01/2021 - High Risk Contamination</span></p></td></tr></table>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.actionquit.setText(_translate("MainWindow", "Save Data"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

