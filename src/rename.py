# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Thu Mar  3 08:31:32 2022

@author: wyatt
"""

from positioncontrol import PositionControlTask
from motordriver import MotorDriver
from encoderdriver import EncoderDriver
import pyb


#>>>>> Initlizing Class Objects <<<<<<

=======
Created on Sat Mar  5 21:13:25 2022

@author: james
"""
from positioncontrol import PositionControlTask
from encoderdriver import EncoderDriver
from motordriver import MotorDriver
import pyb


>>>>>>> 9db80527ac4d1566325147a95e3e78f7b43b587c
## Creates the motor object for motor B
motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)

## Creates the motor object for motor A
motor_A = MotorDriver(pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Pin.board.PA10, 3)

## Creates the encoder object for encoder B
enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)

## Creates the encoder object for encoder A
enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)

## Create the position control object for system A
control_A = PositionControlTask(motor_A, enc_A)

## Creates the position control object for system B
<<<<<<< HEAD
control_B = PositionControlTask(motor_B, enc_B)
=======
control_B = PositionControlTask(motor_B, enc_B)

def system_1 ():
    """!
    Task which facilitates the motor position control method and records
    motor 1 data in a queue. The task then prints the data which is controlled
    by a generator.
    """
    
    ## State varible used to signal program whether to collect data, print
    #  data, or terminate program.
    state = 0
    
    while True:
        
        ## Updates Current Time
        if(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_A.position_control()
        
            ## Current time at which the position data is collected
            current_time_A = time.ticks_diff(time.ticks_ms(), start_time)
            
            if current_time_A > 5000:
                state = 1
            
            # Collect time list data if the queue is not full
            if time_list_A.full() == False:
                # Creates a list of Time data
                time_list_A.put(current_time_A)

            # Collect position data if the queue is not full                
            if Position_A.full() == False:
                # Creates a list of Time data
                Position_A.put(enc_A.get_position())
            else:
                pass


        yield (0)
>>>>>>> 9db80527ac4d1566325147a95e3e78f7b43b587c
