# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:50:00 2020

@author: vernier
"""

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QPushButton,QSpinBox,QLineEdit
from PyQt5.QtWidgets import QComboBox,QSlider,QLabel,QInputDialog
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon

import sys, time, string
from serial.tools.list_ports import comports
import trinamicMotor


import qdarkstyle # pip install qdarkstyle https://github.com/ColinDuquesnoy/QDarkStyleSheet  sur conda
import pathlib,os


class TrinamGUI(QWidget) :

    def __init__(self,name=None):
        super(TrinamGUI, self).__init__()

        
        
        self.setWindowTitle('Trinamic motors')
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))



        self.setup()
        self.actionButton()
        self.listComPorts()
        



        
    def setup(self):    
        
        vbox=QVBoxLayout()
        
        
        intro = QHBoxLayout()
        self.comPorts = QComboBox()
        self.comPorts.setMaximumWidth(80)
        
        self.refresh=QPushButton('Refresh')
        self.refresh.setMaximumWidth(120)
                
        intro.addWidget(self.comPorts)
        intro.addWidget(self.refresh)
        intro.addStretch(500)
        vbox.addLayout(intro)
        
        mot1=QHBoxLayout()
        self.connectBtn = QPushButton('Connect Motor')
        self.disconnectBtn = QPushButton('Disconnect Motor')
        
        self.moveMinusBtn = QPushButton('Move rel -')
        self.movePlusBtn = QPushButton('Move rel +')
        
        self.movmentBox = QSpinBox()
        self.movmentBox.setMinimum(0)
        self.movmentBox.setMaximum(10000000)
        self.movmentBox.setMaximumWidth(80)
        
        
        self.STOP_Btn = QPushButton('STOP !')
        
        self.velBtn = QPushButton('Set Vel')
        
        self.velBox = QSpinBox()
        self.velBox.setMinimum(0)
        self.velBox.setMaximum(12000)
        self.velBox.setMaximumWidth(80)
        
        self.accBtn = QPushButton('Set Acc')
        
        self.accBox = QSpinBox()
        self.accBox.setMinimum(0)
        self.accBox.setMaximum(9000)
        self.accBox.setMaximumWidth(80)
        
        self.posBox = QLineEdit()
        self.posBox.setMaximumWidth(80)
        self.posBox.setReadOnly(True)
        self.posLabel = QLabel("Curr Pos")
        
        
        self.messageBox = QLineEdit()
        self.messageBox.setMaximumWidth(120)
        self.messageBox.setReadOnly(True)
        self.messageLabel = QLabel("Message")
        

        mot1.addWidget(self.connectBtn)
        mot1.addWidget(self.moveMinusBtn)
        mot1.addWidget(self.movmentBox);
        mot1.addWidget(self.movePlusBtn)
        mot1.addWidget(self.posLabel)
        mot1.addWidget(self.posBox)
        mot1.addWidget(self.velBox)
        mot1.addWidget(self.velBtn)
        mot1.addWidget(self.accBox)
        mot1.addWidget(self.accBtn)
        mot1.addWidget(self.messageLabel)
        mot1.addWidget(self.messageBox)
        mot1.addWidget(self.STOP_Btn)
        mot1.addWidget(self.disconnectBtn)

        vbox.addLayout(mot1)
        self.setLayout(vbox)

        
    def actionButton(self):
        self.refresh.clicked.connect(self.listComPorts)
        self.connectBtn.clicked.connect(self.createMotor)
        self.disconnectBtn.clicked.connect(self.removeMotor)
        self.moveMinusBtn.clicked.connect(lambda : self.moveMotor(-1))
        self.movePlusBtn.clicked.connect(lambda : self.moveMotor(1))
        self.velBtn.clicked.connect(self.changeVel)
        self.accBtn.clicked.connect(self.changeAcc)
        self.STOP_Btn.clicked.connect(self.stopMotor)
        
          
    def listComPorts(self):
        try:
            self.comPorts.clear()
            ports = comports()
            for port in ports :
                self.comPorts.addItem(port.device)
        except: 
            self.messageBox.setText('No COM port')
            

    def createMotor(self):   
        try:
            port = self.comPorts.currentText()
            self.motor=trinamicMotor.abstractMotor(port, 1, 0, 'configMoteur.ini')
            self.messageBox.setText('Success')
            
        except :
            self.messageBox.setText('Mot open fail')
            self.connectBtn.setEnabled(True)
        else:    
            try:
                self.velBox.setValue(self.motor.get_vel())
                self.accBox.setValue(self.motor.get_acc())
                self.posBox.setText(str(self.motor.get_pos()))
            except Exception as e:
                print(str(e))
            else :
                self.connectBtn.setEnabled(False)


    
    def removeMotor(self):

        try:
            self.motor.close()
            
        except :
            self.messageBox.setText('Mot close fail')
            pass
        self.connectBtn.setEnabled(True)
    
    def changePosVal(self):
        try: 
            self.posBox.setText(str(self.motor.get_pos()))
        except:
            pass
    
    def moveMotor(self, direction):
        mv = direction*self.movmentBox.value()
        try:
        
            self.motor.move_relative(mv, lambda : self.changePosVal())
        except :
            self.messageBox.setText('Mov fail')
            pass
    
    def changeVel(self):
        vel = self.velBox.value()
        try:
        
            self.motor.set_vel(vel)
        except :
            self.messageBox.setText('Vel fail')
            pass
        
    def changeAcc(self):
        acc = self.accBox.value()
        try:
        
            self.motor.set_vel(acc)
        except :
            self.messageBox.setText('Acc fail')
            pass
    
         
    def stopMotor(self):
        try:
        
            self.motor.STOP()
        except :
            self.messageBox.setText('Stop fail')
            pass
        
  

if __name__ == "__main__":
    appli = QApplication(sys.argv)  
    e = TrinamGUI(name='TrinamGUI')  
    e.show()
    appli.exec_()         