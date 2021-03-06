# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:32:58 2020

@author: vernier
"""

from PyQt5.QtCore import QSettings
from serial import Serial
import pyTMCL



class abstractMotor(object):
    def __init__(self, port, module_address, motor_id, confSettings):
        
        self.port=port
        self.module_address=module_address
        self.motor_id=motor_id
        self.confSettings=confSettings
        self.mottype='generic'
        
        # Connect, and get motor : returns Bus and Motor instances from pyTMCL module
        try:
            self.serial_port = Serial(self.port, timeout=1, write_timeout=1)
  
        except Exception as e:
            raise e
        
        try:
            self.bus = pyTMCL.connect(self.serial_port)
        except Exception as e:
            raise e
            
        try:
            self.motor = self.bus.get_motor(self.module_address, self.motor_id)
        except Exception as e:
            raise e
            
            
        try :
            self.confMot=QSettings(confSettings, QSettings.IniFormat) # motor configuration  files  
            self.vMax=int(self.confMot.value(self.mottype+'/vMax'))#1142
            self.iMax=int(self.confMot.value(self.mottype+'/iMax'))
            self.iStby=int(self.confMot.value(self.mottype+'/iStby'))
            self.accMax=int(self.confMot.value(self.mottype+'/accMax'))
            self.ustepRes=int(self.confMot.value(self.mottype+'/ustepRes')) # step resolution (0-8)
            
        except Exception as e :
            self.serial_port.close()
            raise e
        
        try : 

            self.set_param(4, self.iMax)   # max current frac
            self.set_param(5, self.accMax) # max acc
            self.set_param(140, self.ustepRes)  # µstep res
            self.set_param(4, self.vMax) # max vel
            self.set_param(7, self.iStby) # max standby current 
            currPos = self.get_pos()
            self.set_param(0, currPos) # max standby current 
            self.STOP()
            
        except Exception as e :
            raise e
            try :
                self.serial_port.close()
            except :
                pass
        
    def close(self):
        self.motor.stop()
        self.serial_port.close()
    
    def STOP(self):
        self.motor.stop()
        
    
    def set_param(self, n, val):
        try:
            self.motor.set_axis_parameter(n, val)      
        except Exception as e : 
            raise e
    
    def move_absolute(self, steps, callbackFunction):
        self.motor.move_absolute(steps, callbackFunction)
        
    def move_relative(self, steps, callbackFunction):
        self.motor.move_relative(steps, callbackFunction)
    
    def get_pos(self):
        return self.motor.get_axis_parameter(1)
    
    def get_vel(self):
        return self.motor.get_axis_parameter(4)
    
    def set_vel(self, vel):
        self.motor.set_axis_parameter(4, vel)
    
    def get_acc(self):
        return self.motor.get_axis_parameter(5)
    
    def set_acc(self, acc):
        self.motor.set_axis_parameter(5, acc)
    
    def get_left_switch_stat(self):
        stat = self.motor.get_axis_parameter(11)
        if stat == 0:
            stat = False
        else:
            stat = True
        return stat
    
    def get_right_switch_stat(self):
        stat = self.motor.get_axis_parameter(10)
        if stat == 0:
            stat = False
        else:
            stat = True
        return stat


        
        

            
            