"""!
@file solenoid.py
This file configures the solenoid output pin on the Nucleo. Methods can control whether
the output pin of the solenoid is high or low to control the orientation of the setpoint.
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   5-March-22
@copyright by Jacob Wong all rights reserved
"""

import pyb
import time

class Solenoid:
    """!
    Initializes solenoid pin as output, while the other solenoid wire is connected to power through a transistor
    and a diode.
    """
    
    def __init__ (self, pin1):
        """!
        Configures solenoid pin as output.
        @param pin1 Pin connected to the output lead of the solenoid.
        """
        ## Pin object for what pin is hook up to the solenoid circuit
        self.pin1 = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        
    def pen_down(self):
        """!
        Sets the orinentation of the pen down by setting the output pin high.
        """
        self.pin1.high()
        
    def pen_up(self):
        """!
        Sets the orientation of the pen up by setting the output pin to low.
        """
        self.pin1.low()
        
if __name__ == "__main__":
    ## Solenoid object for testing purposes
    my_sol = Solenoid(pyb.Pin.board.PC4)
    
    my_sol.pen_down()
    time.sleep(3)
    my_sol.pen_up()
