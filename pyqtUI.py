# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.v6.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint
from Settings import readSettings, writeSettings
from passlogic import *
import os


class MainWindow(QtWidgets.QMainWindow):
    username = os.getlogin()
    Dir = readSettings()
    data = ""
    lastApp = ""
    lastID = ""
    key = setKey(Dir)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.loadTable()
        self.setWindowTitle('You\'r Password Saver')
        self.oldPos = self.pos()

    # mouse events -> draggable Frameless Window
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def loadTable(self):
        # refresh table
        self.tableWidget.clearSelection()
        self.data = ReadData(self.key)
        self.tableWidget.setRowCount(0)
        for rowNum, rowData in enumerate(self.data):
            self.tableWidget.insertRow(rowNum)
            for columNum, Data in enumerate(rowData):
                self.tableWidget.setItem(rowNum, columNum, QtWidgets.QTableWidgetItem(str(Data)))

    def SendData(self):
        self.refresh()
        # get text
        programName = self.NameEdit.text().strip()
        ID = self.IDedit.text().strip()
        password = self.PassEdit.text().strip()
        # check empty strings
        if programName == "" or ID == "" or password == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Empty field noticed")
            msg.setInformativeText('Must fill all fields')
            msg.setWindowTitle("Error")
            msg.exec_()
        # call for checkDuplicates at passlogic
        elif checkDuplicate(programName, ID, self.data):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You've used this App with the Same email address")
            msg.setInformativeText("Do you mean 'update'?")
            msg.setWindowTitle("Duplicate")
            msg.exec_()
        else:
            # clear lines and send values to passlogic - WriteData function
            self.NameEdit.clear()
            self.IDedit.clear()
            self.PassEdit.clear()
            WriteData(programName, ID, password, self.key, self.encryptBox.isChecked())
        self.refresh()

    def updateData(self):
        # get text
        self.refresh()
        programName = self.NameEdit.text().strip()
        ID = self.IDedit.text().strip()
        password = self.PassEdit.text().strip()
        # check empty strings
        if programName == "" or ID == "" or password == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Empty field noticed")
            msg.setInformativeText('Must fill all fields')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            # clear lines and send values to passlogic - updateData function
            self.NameEdit.clear()
            self.IDedit.clear()
            self.PassEdit.clear()
            updateData(programName, ID, password, self.key, self.encryptBox.isChecked(), str(self.lastApp),
                       str(self.lastID))
        self.refresh()

    # select key button function
    def getKeyDir(self):
        # calls for Q file dialog
        File = QFileDialog.getOpenFileName(None, 'select directory for your key', r"D:\\", "Text files(*.txt)")
        # no selection
        if File[0] == '':
            print("nothing selected")
        else:
            # validate key
            self.key = setKey(File[0])
            # catch errors from passlogic - encrypt function
            if encrypt('123', self.key) == 'binascii.Error' or encrypt('123', self.key) == 'ValueError':
                self.key = setKey(readSettings())
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("the file selected has an invalid key.\n ")
                msg.setInformativeText("for a new key please select an empty file")
                msg.setWindowTitle("Bad file")
                msg.exec_()
            else:
                # enter new key to settings and UI
                writeSettings(File[0])
                self.key = setKey(readSettings())
                self.keyLable.setText("the key is -  " + self.key)
                self.refresh()

    # delete row action(function at passlogic)
    def sendIDtoDelete(self):
        row = self.tableWidget.currentRow()
        try:
            DeleteRow(self.tableWidget.item(row, 0).text(), self.tableWidget.item(row, 1).text())
        except AttributeError:
            print("No row selected")
        self.refresh()

    # handels table row selection
    def clickSelectChange(self):
        # row select
        row = self.tableWidget.currentRow()
        # fill lines with selected row
        self.NameEdit.setText(self.tableWidget.item(row, 0).text())
        self.IDedit.setText(self.tableWidget.item(row, 1).text())
        # update last selected item
        self.lastApp = self.tableWidget.item(row, 0).text()
        self.lastID = self.tableWidget.item(row, 1).text()

    # close app
    def closeEvent(self):
        reply = QMessageBox.question(
            self.centralwidget, "Message",
            "Are you sure you want to quit? ",
            QMessageBox.Close | QMessageBox.Cancel,
        )

        if reply == QMessageBox.Close:
            sys.exit()
        else:
            pass

    # key listener
    def keyPressEvent(self, event):
        # Close application from escape key.
        if event.key() == Qt.Key_Escape:
            self.closeEvent()
        # refresh at f5
        if event.key() == Qt.Key_F5:
            self.refresh()
        # calls for show info
        if event.key() == Qt.Key_F1:
            self.showInfo()
        # delete row
        if event.key() == Qt.Key_Delete:
            self.sendIDtoDelete()

    def refresh(self):
        self.key = setKey(readSettings())
        self.keyLable.setText("the key is -  " + self.key)
        self.loadTable()

    # user use information box
    def showInfo(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Hello user,\nThis application will save you'r passwords in an encrypted\nand safe way.\nAt first "
                    "use of this app a text file will be created at you'r desktop.\nThis text file will hold you'r "
                    "encryption key, without a key you'r \npasswords cant be encrypted.\nIt is recommended to move "
                    "the key to an outer source(like a USB flashdrive).\n*Note you must select the new file location "
                    "using the 'select key button'\n\nTo create a new key simply select an empty txt file.\n You may "
                    "use diffrent keys for diffrent passwords.\n")
        msg.setInformativeText('If you do not want to encrypt the password\n leave the "encrypt password" check box '
                               'unchecked.\n*Note that unencrypted passwords will always show')
        msg.setWindowTitle("How to use")
        msg.exec_()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(785, 471)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color:rgba(85, 85, 85, 150);\n"
                           "")
        self.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 250, 701, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NameEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NameEdit.sizePolicy().hasHeightForWidth())
        self.NameEdit.setSizePolicy(sizePolicy)
        self.NameEdit.setMaximumSize(QtCore.QSize(229, 50))
        self.NameEdit.setBaseSize(QtCore.QSize(40, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.NameEdit.setFont(font)
        self.NameEdit.setObjectName("NameEdit")
        self.horizontalLayout.addWidget(self.NameEdit)
        self.IDedit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.IDedit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IDedit.sizePolicy().hasHeightForWidth())
        self.IDedit.setSizePolicy(sizePolicy)
        self.IDedit.setMaximumSize(QtCore.QSize(229, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.IDedit.setFont(font)
        self.IDedit.setObjectName("IDedit")
        self.horizontalLayout.addWidget(self.IDedit)
        self.PassEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PassEdit.sizePolicy().hasHeightForWidth())
        self.PassEdit.setSizePolicy(sizePolicy)
        self.PassEdit.setMaximumSize(QtCore.QSize(229, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.PassEdit.setFont(font)
        self.PassEdit.setObjectName("PassEdit")
        self.horizontalLayout.addWidget(self.PassEdit)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(650, 340, 91, 16))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        # <----------------submit button------------------>
        self.Subtn = QtWidgets.QPushButton(self.centralwidget)
        self.Subtn.setGeometry(QtCore.QRect(580, 320, 151, 41))
        self.Subtn.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                 "border: 2px solid black;\n"
                                 "border-radius:10px;")
        self.Subtn.setObjectName("Subtn")
        self.Subtn.setToolTip('This will create a new row\n all fields must be filled\n'
                              'There\'s no validation for your info, please check spelling')
        self.Subtn.clicked.connect(self.SendData)
        # <----------table-------------------->
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(35, 30, 691, 192))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setStyleSheet("::section{Background-color:rgba(230, 230, 230, 200);\n"
                                       "border-radius:14px;padding-right: 10px;}")
        self.tableWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setMidLineWidth(2)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.verticalHeader().setVisible(False)
        # <--end of table ------>
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 220, 701, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(11)
        font.setItalic(False)
        font.setUnderline(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:rgba(175, 175, 175, 200)")
        self.label_6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(11)
        font.setItalic(False)
        font.setUnderline(True)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color:rgba(175, 175, 175, 200)")
        self.label_5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(11)
        font.setItalic(False)
        font.setUnderline(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color:rgba(175, 175, 175, 200)")
        self.label_3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        # <----------------select key button------------------>
        self.SelectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.SelectBtn.setGeometry(QtCore.QRect(660, 380, 75, 23))
        self.SelectBtn.setStyleSheet("background-color:rgb(117, 117, 117);\n"
                                     "border-style: outset;\n"
                                     "border-width: 2px;\n"
                                     "border-color:rgb(0, 0, 0);\n"
                                     "")
        self.SelectBtn.setObjectName("SelectBtn")
        self.SelectBtn.setToolTip('Select a text file with your key.\nIf you want a new key simply select an empty '
                                  'text file.')
        self.SelectBtn.clicked.connect(self.getKeyDir)
        # <----------------update password button------------------>
        self.updateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.updateBtn.setGeometry(QtCore.QRect(500, 340, 75, 23))
        self.updateBtn.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                     "border-style: outset;\n"
                                     "border-width: 2px;\n"
                                     "border-color:rgb(0, 0, 0);\n"
                                     "")
        self.updateBtn.setObjectName("updateBtn")
        self.updateBtn.setToolTip('This will update the selected row')
        self.updateBtn.clicked.connect(self.updateData)
        # <----------------delete row button------------------>
        self.deleteBtn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteBtn.setGeometry(QtCore.QRect(420, 340, 75, 23))
        self.deleteBtn.setStyleSheet("QPushButton{\n"
                                     "background-color:rgba(255, 0, 0, 190);\n"
                                     "border-style: outset;\n"
                                     "border-width: 2px;\n"
                                     "border-color:rgb(0, 0, 0);};\n"
                                     "QPushButton::hover\n"
                                     "{\n"
                                     "    background-color:rgba(255, 80, 80, 220);\n"
                                     "};\n"
                                     "")
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setToolTip('This will delete the selected row')
        self.deleteBtn.clicked.connect(self.sendIDtoDelete)
        # <------------quit btn---------------->
        self.quitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.quitBtn.setGeometry(QtCore.QRect(20, 400, 75, 23))
        self.quitBtn.setStyleSheet("QPushButton::hover{background-color:red}\n"
                                   "QPushButton{border-style: outset;\n"
                                   "border-color:gray;\n"
                                   "border-width: 2px;};")
        self.quitBtn.clicked.connect(self.closeEvent)
        self.quitBtn.setObjectName("quitBtn")
        # <------------info btn---------------->
        self.infoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.infoBtn.setGeometry(QtCore.QRect(110, 400, 75, 23))
        self.infoBtn.setStyleSheet("QPushButton::hover{background-color:yellow}\n"
                                   "QPushButton{border-style: outset;\n"
                                   "border-color:gray;\n"
                                   "border-width: 2px;};")
        self.infoBtn.clicked.connect(self.showInfo)
        self.infoBtn.setObjectName("infoBtn")
        # <----------------show password check button------------------>
        self.encryptBox = QtWidgets.QCheckBox(self.centralwidget)
        self.encryptBox.setGeometry(QtCore.QRect(630, 10, 111, 17))
        self.encryptBox.setObjectName("encryptBox")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 785, 21))
        self.menubar.setObjectName("menubar")
        self.menumain = QtWidgets.QMenu(self.menubar)
        self.menumain.setObjectName("menumain")
        self.menusettings = QtWidgets.QMenu(self.menubar)
        self.menusettings.setObjectName("menusettings")
        self.setMenuBar(self.menubar)
        # <-----Sign in ----->
        self.actionSign_in = QtWidgets.QAction(self)
        self.actionSign_in.setObjectName("actionSign_in")
        # <-----Sign out ----->
        self.actionsign_Out = QtWidgets.QAction(self)
        self.actionsign_Out.setObjectName("actionsign_Out")
        # <----Offline ----->
        self.actionOffline_mode = QtWidgets.QAction(self)
        self.actionOffline_mode.setCheckable(True)
        self.actionOffline_mode.setObjectName("actionOffline_mode")
        self.menumain.addAction(self.actionSign_in)
        self.menusettings.addAction(self.actionsign_Out)
        self.menusettings.addAction(self.actionOffline_mode)
        self.menubar.addAction(self.menumain.menuAction())
        self.menubar.addAction(self.menusettings.menuAction())
        self.keyLable = QtWidgets.QLabel("the key is -  " + self.key, self)
        self.keyLable.setGeometry(270, 400, 370, 20)
        # <------row selection lisner --->
        self.tableWidget.itemSelectionChanged.connect(self.clickSelectChange)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Subtn.setText(_translate("MainWindow", "Submit"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "App name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID/Email"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "password"))
        self.label_6.setText(_translate("MainWindow", "Program name"))
        self.label_5.setText(_translate("MainWindow", "ID/Email"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.SelectBtn.setAccessibleDescription(_translate("MainWindow", "background-color:rgb(190, 190, 190);\n"
                                                                         "border-style: outset;\n"
                                                                         "border-width: 2px;\n"
                                                                         "border-color:rgb(0, 0, 0);\n"
                                                                         ""))
        self.SelectBtn.setText(_translate("MainWindow", "Select key"))
        self.updateBtn.setText(_translate("MainWindow", "update"))
        self.deleteBtn.setText(_translate("MainWindow", "delete"))
        self.quitBtn.setText(_translate("MainWindow", "Close"))
        self.infoBtn.setText(_translate("MainWindow", "how to use"))
        self.encryptBox.setText(_translate("MainWindow", "encrypt password"))
        self.menumain.setTitle(_translate("MainWindow", "main"))
        self.menusettings.setTitle(_translate("MainWindow", "settings"))
        self.actionSign_in.setText(_translate("MainWindow", "Sign in"))
        self.actionsign_Out.setText(_translate("MainWindow", "sign Out"))
        self.actionOffline_mode.setText(_translate("MainWindow", "Offline mode"))
