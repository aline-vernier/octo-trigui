# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:50:00 2020

@author: vernier
"""

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget
from PyQt5.QtWidgets import QComboBox,QLabel,QPushButton,QSpinBox,QLineEdit

from PyQt5.QtGui import QIcon

import sys
from serial.tools.list_ports import comports

import trinamicMotor

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

###############################################################################
#               SETTING UP UI LAYOUT                                          #
###############################################################################  
        
    def setup(self):    
        
        vbox=QVBoxLayout()

########  Intro : connect & disconnect
        intro = QHBoxLayout()
        self.comPorts = QComboBox()
        self.comPorts.setMaximumWidth(80)
        
        self.refresh=QPushButton('Refresh')
        self.refresh.setMaximumWidth(120)
        
        self.connectBtn = QPushButton('Connect Motor')
        self.disconnectBtn = QPushButton('Disconnect Motor')
                
        intro.addWidget(self.comPorts)
        intro.addWidget(self.refresh)
        intro.addWidget(self.connectBtn)
        intro.addWidget(self.disconnectBtn)
        intro.addStretch(0)
        vbox.addLayout(intro)
        
########  Message  
        
        message = QHBoxLayout()
        self.messageBox = QLineEdit()
        self.messageBox.setMaximumWidth(600)
        self.messageBox.setReadOnly(True)
        self.messageLabel = QLabel("Message")
        message.addWidget(self.messageLabel)
        message.addWidget(self.messageBox)
        vbox.addLayout(message)
        
########  Relative movement      
        
        relHBox=QHBoxLayout()
        self.moveMinusBtn = QPushButton('Move rel -')
        self.movePlusBtn = QPushButton('Move rel +')
        
        self.movmentBox = QSpinBox()
        self.movmentBox.setMinimum(0)
        self.movmentBox.setMaximum(10000000)
        self.movmentBox.setMaximumWidth(120)
    
        relHBox.addWidget(self.moveMinusBtn)
        relHBox.addWidget(self.movmentBox);
        relHBox.addWidget(self.movePlusBtn)
        vbox.addLayout(relHBox)
        
########  Absolute movement   
        
        absHBox=QHBoxLayout()
        self.moveAbsBtn = QPushButton('Move abs.')
        
        self.movmentAbsBox = QSpinBox()
        self.movmentAbsBox.setMinimum(-10000000)
        self.movmentAbsBox.setMaximum(10000000)
        self.movmentAbsBox.setMaximumWidth(120)
    
        absHBox.addWidget(self.movmentAbsBox)
        absHBox.addWidget(self.moveAbsBtn)
        

        vbox.addLayout(absHBox)
        
########  Set Velocity          
 
        velHBox=QHBoxLayout()
        self.velBtn = QPushButton('Set Vel')
        
        self.velBox = QSpinBox()
        self.velBox.setMinimum(0)
        self.velBox.setMaximum(12000)
        self.velBox.setMaximumWidth(120)   
        
        velHBox.addWidget(self.velBox)
        velHBox.addWidget(self.velBtn)
        
        vbox.addLayout(velHBox)
        
########  Set Acceleration          
 
        accHBox=QHBoxLayout()
        self.accBtn = QPushButton('Set Acc')
        
        self.accBox = QSpinBox()
        self.accBox.setMinimum(0)
        self.accBox.setMaximum(12000)
        self.accBox.setMaximumWidth(120)   
        
        accHBox.addWidget(self.accBox)
        accHBox.addWidget(self.accBtn)
        
        vbox.addLayout(accHBox)
        
########  Position and stop
        
        posNStopHBox=QHBoxLayout()
        self.posBox = QLineEdit()
        self.posBox.setMaximumWidth(80)
        self.posBox.setReadOnly(True)
        self.posLabel = QLabel("Curr Pos")
        
        self.STOP_Btn = QPushButton('STOP !')
        
        posNStopHBox.addWidget(self.posLabel)
        posNStopHBox.addWidget(self.posBox)
        posNStopHBox.addWidget(self.STOP_Btn)
        
        vbox.addLayout(posNStopHBox)
        
########  Set full layout

        self.setLayout(vbox)

########  Make sure everything is clean on closing

        appli.aboutToQuit.connect(self.cleanOnClosing)
        
   
###############################################################################
#               DEFINING BUTTON BEHAVIOUR                                     #
###############################################################################        
    
     
    def actionButton(self):
        
        
        self.refresh.clicked.connect(self.listComPorts)
        self.connectBtn.clicked.connect(self.createMotor)
        self.disconnectBtn.clicked.connect(self.removeMotor)
        self.moveMinusBtn.clicked.connect(lambda : self.moveMotor(-1))
        self.movePlusBtn.clicked.connect(lambda : self.moveMotor(1))
        self.moveAbsBtn.clicked.connect(self.moveAbsMotor)
        self.velBtn.clicked.connect(self.changeVel)
        self.accBtn.clicked.connect(self.changeAcc)
        self.STOP_Btn.clicked.connect(self.stopMotor)

###############################################################################
#               INITIALIZATION AND CLOSURE                                    #
###############################################################################      
          
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
            self.motor=trinamicMotor.abstractMotor(port, 1, 0, 
                                                   'configMoteur.ini')
            self.messageBox.setText('Success')
            
        except Exception as e :
            self.messageBox.setText('Mot open fail:' + str(e))
            self.connectBtn.setEnabled(True)
        else:    
            try:
                self.velBox.setValue(self.motor.get_vel())
                self.accBox.setValue(self.motor.get_acc())
                self.posBox.setText(str(self.motor.get_pos()))
            except Exception as e:
                self.messageBox.setText(str(e))
            else :
                self.connectBtn.setEnabled(False)

    
    def removeMotor(self):

        try:
            self.motor.close()
            
        except :
            self.messageBox.setText('Mot close fail')
            pass
        self.connectBtn.setEnabled(True)

###############################################################################
#               MOTOR BEHAVIOUR                                               #
###############################################################################
    
    def changePosVal(self):
        try: 
            self.posBox.setText(str(self.motor.get_pos()))
        except:
            pass
    
    def moveMotor(self, direction):
        mv = direction*self.movmentBox.value()
        try:
        
            self.motor.move_relative(mv, lambda : self.changePosVal())
        except Exception as e :
            self.messageBox.setText('Rel Mov fail:' + str(e))
            pass
        
    def moveAbsMotor(self, direction):
        mv = self.movmentAbsBox.value()
        try:
            self.motor.move_absolute(mv, lambda : self.changePosVal())
        except Exception as e :
            self.messageBox.setText('Abs Mov fail:' + str(e))
            pass
    
    def changeVel(self):
        vel = self.velBox.value()
        try:
        
            self.motor.set_vel(vel)
        except Exception as e:
            self.messageBox.setText('Vel fail:'+ str(e))
            pass
        
    def changeAcc(self):
        acc = self.accBox.value()
        try:
        
            self.motor.set_vel(acc)
        except Exception as e:
            self.messageBox.setText('Acc fail:'+ str(e))
            pass
    
         
    def stopMotor(self):
        try:
        
            self.motor.STOP()
        except Exception as e:
            self.messageBox.setText('Stop fail:'+ str(e))
            pass
    
###############################################################################
#               APPLICATION EXIT                                              #
###############################################################################
    
    def cleanOnClosing(self):
        try:
            self.motor.STOP()
        except:
            pass
        try:
            self.motor.close()
        except:
            pass
        finally: 
            try:
                sys.exit(0)
            except Exception as e:
                print(str(e))
        
        
###############################################################################
#              MAIN                                                           #          
###############################################################################        
  

if __name__ == "__main__":
    appli = QApplication(sys.argv)  
    e = TrinamGUI(name='TrinamGUI')  
    e.show()
    appli.exec_()         