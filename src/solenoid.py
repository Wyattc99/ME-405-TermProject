# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 19:26:26 2022

@author: james
"""

import pyb

class Solenoid:
    
    def __init__ (self, pin1):
        self.pin1 = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        
    def pen_down(self):
        self.pin1.high()
        
    def pen_up(self):
        self.pin1.low()
