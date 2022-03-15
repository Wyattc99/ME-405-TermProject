"""!
@file limit_switch.py
This file configures a limit switch to trigger high when our physical system presses the limit switch closed.
The file is set up as a class so a user can instantiate mulitple limit switches. We have physically configured the limit switch to be normallly open.
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   5-March-22
@copyright by Jacob Wong all rights reserved
"""

import pyb
import time

class Limit_Switch:
    """!
    Initializes the normally open pin on the Nucleo as an input pin. Contains a method to check if the normally open pin has been triggered high.
    """
    
    def __init__ (self, pin1):
        """!
        Configures limit switch input pin
        @param pin1 The nucleo pin wired to the normally open limit switch connection
        """
        ## Pin used to read incoming signal from limit switch
        self.pin1 = pyb.Pin(pin1, pyb.Pin.IN)
    
    def check_limit(self):
        """!
        Checks the value of the limit switch output. If read high, the method returns 1. If read low, the method returns 0.
        """
        
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