# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:49:27 2022

@author: james
"""
import pyb

class Limit_Switch:
    
    def __init__ (self, pin1):
        self.pin1 = pyb.Pin(pin1, pyb.Pin.IN)
    
    def check_limit(self):
        if(self.pin1.value() == 1):
            return True
        else:
            return False