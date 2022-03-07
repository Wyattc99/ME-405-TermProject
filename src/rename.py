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

import cotask
import task_share
from positioncontrol import PositionControlTask
from encoderdriver import EncoderDriver
from motordriver import MotorDriver
import pyb
import gc
import hpgl

<<<<<<< HEAD:src/main.py
def update_pwm_radial ():
=======

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
>>>>>>> c3a37880f1c91f43c1ef29af7eee5b82b400670a:src/rename.py
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

        yield (0)
        
def update_pwm_theta ():
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
            control_B.position_control()

        yield (0)
        
def get_setpoint_r (radial_hpgl):
    
    state = 0
        
    while True:
        
        if(state == 0):
            set_point_r.put(radial_hpgl.get())
            state = 1
            
        elif(state == 1):
        
            condition = control_A.check_error()
            
            if (condition == True):
                state = 0
                
        yield(0)
                
def get_setpoint_theta (theta_hpgl):
    
    state = 0
        
    while True:
        
        if(state == 0):
            set_point_theta.put(theta_hpgl.get())
            state = 1
            
        elif(state == 1):
        
            condition = control_B.check_error()
            
            if (condition == True):
                state = 0
                
        yield(0)

<<<<<<< HEAD:src/main.py
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')
    
    radial_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 1)
    
    theta_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 2)
    
    set_point_r = task_share.Share ('f', thread_protect = False, name = "Radial Set Point")
    
    set_point_theta = task_share.Share ('f', thread_protect = False, name = "Theta Set Point")
    
    error_r = task_share.Share ('f', thread_protect = False, name = "Radial Position Error")
    
    error_theta = task_share.Share ('f', thread_protect = False, name = "Theta Position Error")
    
    ## Creates the motor object for motor B
    motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)
    
    ## Creates the motor object for motor A
    motor_A = MotorDriver(pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Pin.board.PA10, 3)
    
    ## Creates the encoder object for encoder B
    enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    ## Creates the encoder object for encoder A
    enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    ## Create the position control object for system A
    control_A = PositionControlTask(motor_A, enc_A, error_r, set_point_r)
    
    ## Creates the position control object for system B
    control_B = PositionControlTask(motor_B, enc_B, error_theta, set_point_theta)
    
    hpgl.Hpgl(radial_hpgl, theta_hpgl)
    
    ## Task 1 used to operate motor 1 function task
    task1 = cotask.Task (update_pwm_radial, name = 'Radial Position Control', priority = 1, 
                             period = 50, profile = True, trace = False)
     
    ## Task 2 used to operate motor 2 function task
    task2 = cotask.Task (update_pwm_theta, name = 'Theta Position Control', priority = 1, 
                             period = 50, profile = True, trace = False)
      
    ## Task 2 used to operate motor 2 function task
    task3 = cotask.Task (get_setpoint_r, name = 'Radial Set Point Control', priority = 1, 
                             period = 50, profile = True, trace = False)
    
    ## Task 2 used to operate motor 2 function task
    task4 = cotask.Task (get_setpoint_theta, name = 'Theta Set Point Control', priority = 1, 
                             period = 50, profile = True, trace = False)
    
    gc.collect()
        
    # Add tasks to cotask schedular list
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)
    
    while True:
        cotask.task_list.pri_sched()
=======
        yield (0)
>>>>>>> 9db80527ac4d1566325147a95e3e78f7b43b587c
>>>>>>> c3a37880f1c91f43c1ef29af7eee5b82b400670a:src/rename.py
