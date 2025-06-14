# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '.\\platforms'

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 500)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.txtName = QtWidgets.QLineEdit(self.centralwidget)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout_2.addWidget(self.txtName)
        self.btnConnect = QtWidgets.QPushButton(self.centralwidget)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout_2.addWidget(self.btnConnect)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.txtChatHistory = QtWidgets.QTextEdit(self.centralwidget)
        self.txtChatHistory.setReadOnly(True)
        self.txtChatHistory.setObjectName("txtChatHistory")
        self.verticalLayout.addWidget(self.txtChatHistory)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.txtMessage = QtWidgets.QLineEdit(self.centralwidget)
        self.txtMessage.setObjectName("txtMessage")
        self.horizontalLayout.addWidget(self.txtMessage)
        self.btnSend = QtWidgets.QPushButton(self.centralwidget)
        self.btnSend.setEnabled(False)
        self.btnSend.setObjectName("btnSend")
        self.horizontalLayout.addWidget(self.btnSend)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat Client An Toàn"))
        self.label.setText(_translate("MainWindow", "Tên của bạn:"))
        self.txtName.setPlaceholderText(_translate("MainWindow", "Nhập tên của bạn"))
        self.btnConnect.setText(_translate("MainWindow", "Kết nối"))
        self.label_2.setText(_translate("MainWindow", "Tin nhắn:"))
        self.txtMessage.setPlaceholderText(_translate("MainWindow", "Nhập tin nhắn và nhấn Enter để gửi"))
        self.btnSend.setText(_translate("MainWindow", "Gửi"))
