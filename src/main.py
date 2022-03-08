# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 21:13:25 2022

@author: james
"""

import cotask
import task_share
from positioncontrol import PositionControlTask
from encoderdriver import EncoderDriver
from motordriver import MotorDriver
from limit_switch import Limit_Switch
import pyb
import gc
import read_plotter

def zero_position():
    """!
    Task which will zero the machine to its orgin using the limit switches within
    the assembly or our design. 
    """
    ## Zero A is a flag to show that the motor A has finished its zeroing process
    zero_A = False
        ## Zero B is a flab to show that the motor B has finished its zeroing process
    zero_B = False
    print('Beginning Zeroing Proccess')
    
    while True:
        
        # if (limit_A.check_limit()):
        #    210, 297 mm
        # set the duty to be constant until it hits the switch for motor A
        if limit_flag_A == False and zero_A == False:
            motor_A.set_duty_cycle(50)
        elif limit_flag_A == True:
            motor_A.set_duty_cycle(0)
            zero_A = True
            print('Zero of Motor A complete')
        else:
            pass
        
        # set the duty to be constant until it hits the switch for motor B
        if limit_flag_B ==False and zero_B == False:
            motor_B.set_duty_cycle(50)
        elif limit_flag_B == True:
            motor_B.set_duty_cycle(0)
            zero_B = True
            print('Zero of Motor B complete')
        else:
            pass
        
        if zero_A == True and zero_B == True:
            break
        
    # Set the encoder position Values to Zero
    enc_A.set_position(0)
    enc_B.set_position(0)
    print('The Machine is has been calibrated')
    
def update_pwm_radial ():
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
            control_radial.position_control()
            # print('Updating PWM')
            
            # if (limit_A.check_limit()):
            #     state = 1
                
        if(state == 1):
            print('Limit Has been hit!')
            state = 0

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
            control_theta.position_control()
            print('Updating PWM')
            print('Error: ', error_theta.get())
            
            # if (limit_B.check_limit()):
            #     state = 1
                
        if(state == 1):
            print('Limit Has been hit!')
            state = 0

        yield (0)
        
def get_setpoint_r ():
    
    state = 0
        
    while True:
        
        if(state == 0):
            
            set_point_r.put(-1*radial_hpgl.get()-16000)
            print('Radial Set Point: ', set_point_r.get())
            state = 1
            
        elif(state == 1):
        
            print('Checking for error!!!! ', error_r.get())
            condition = control_radial.check_error()
            
            if (condition == True):
                state = 0
                
        yield(0)
                
def get_setpoint_theta ():
    
    state = 0
        
    while True:
        
        if(state == 0):
            set_point_theta.put(-1*theta_hpgl.get()-16000)
            print('Theta Set Point: ', set_point_theta.get())
            state = 1
            
        elif(state == 1):
        
            condition = control_theta.check_error()
            
            if (condition == True):
                state = 0
                
        yield(0)

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
    
    limit_flag_A = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch A")
    
    limit_flag_B = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch B")
    
    offset = 190.5 # offset in mm
    
    ## Creates the motor object for motor B
    motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)
    
    ## Creates the motor object for motor A
    motor_A = MotorDriver(pyb.Pin.board.PB5, pyb.Pin.board.PB4, pyb.Pin.board.PA10, 3)
    
    ## Creates the encoder object for encoder B
    enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    ## Creates the encoder object for encoder A
    enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    ## Create the position control object for system A
    control_theta = PositionControlTask(motor_A, enc_A, error_theta, set_point_theta, 40)    # controller for theta direction
    
    ## Creates the position control object for system B
    control_radial = PositionControlTask(motor_B, enc_B, error_r, set_point_r, 60) # controller for radial direction
    
    limit_A = Limit_Switch(pyb.Pin.board.PC2)
    
    limit_B = Limit_Switch(pyb.Pin.board.PB0)
    
    my_hpgl = read_plotter.Hpgl(radial_hpgl, theta_hpgl, offset)
    
    my_hpgl.read_data()
    
    my_hpgl.convert_data()
    
    origin = my_hpgl.convert_point(210,297)
    
    print(origin)
    
    ## Task 1 used to operate motor 1 function task
    task1 = cotask.Task (update_pwm_radial, name = 'Radial Position Control', priority = 1, 
                             period = 10, profile = True, trace = False)
     
    ## Task 2 used to operate motor 2 function task
    task2 = cotask.Task (update_pwm_theta, name = 'Theta Position Control', priority = 1, 
                             period = 10, profile = True, trace = False)
      
    ## Task 2 used to operate motor 2 function task
    task3 = cotask.Task (get_setpoint_r, name = 'Radial Set Point Control', priority = 1, 
                             period = 10, profile = True, trace = False)
    
    ## Task 2 used to operate motor 2 function task
    task4 = cotask.Task (get_setpoint_theta, name = 'Theta Set Point Control', priority = 1, 
                             period = 10, profile = True, trace = False)
    
    gc.collect()
        
    # Add tasks to cotask schedular list
    #cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    #cotask.task_list.append (task3)
    cotask.task_list.append (task4)
    
    while True:
        cotask.task_list.pri_sched()