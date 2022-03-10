# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 20:49:27 2022

@author: james
"""
import pyb
import time

class Limit_Switch:
    
    def __init__ (self, pin1):
        self.pin1 = pyb.Pin(pin1, pyb.Pin.IN)
    
    def check_limit(self):
        if(self.pin1.value() == 1):
            return 1
        else:
            return 0
        
if __name__ == "__main__":
    my_lim_A = Limit_Switch(pyb.Pin.board.PC0)
    my_lim_B = Limit_Switch(pyb.Pin.board.PB0)
    
    while True:
        print('A:::',my_lim_A.check_limit())
        print('B:::', my_lim_B.check_limit())
        time.sleep(.1)