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
from solenoid import Solenoid
import pyb
import gc
import read_plotter
import time

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
    
    state = 1
    
    while True:
        
        # if (limit_A.check_limit()):
        #    210, 297 mm
        # set the duty to be constant until it hits the switch for motor A
        
        if (state == 0):
            limit_flag_A.put(limit_A.check_limit())
            
            if limit_flag_A.get() == 0 and zero_A == False:
                print ("LimA not pressed")
                #motor_A.set_duty_cycle(40)
            elif limit_flag_A.get() == 1:
                motor_A.set_duty_cycle(0)
                zero_A = True
                time.sleep(5)
                state = 1
                enc_A.set_position(-1000)
                enc_B.set_position(-1000)
                print ("LimA pressed!!")
        if (state == 1):
        # set the duty to be constant until it hits the switch for motor B
            print(limit_flag_B.get())
            limit_flag_B.put(limit_B.check_limit())
            if limit_flag_B.get() == 0 and zero_B == False:
                pass
                motor_B.set_duty_cycle(45)
            elif limit_flag_B.get() == 1:
                motor_B.set_duty_cycle(0)
                zero_B = True
                enc_B.set_position(-3000)
                #enc_B.set_position(-1000)
                
                state = 2
                
                
        
        if (state == 2):
            print(enc_A.get_position())
            print(enc_B.get_position())
            flag_zero.put(1)
            state=3
            
        if (state==3):
            pass
        
        print('1')
        yield(0)
    # Set the encoder position Values to Zero
    
def update_pwm_radial ():
    """!
    Task which facilitates the motor position control method and records
    motor 1 data in a queue. The task then prints the data which is controlled
    by a generator.
    """
    
    ## State varible used to signal program whether to collect data, print
    #  data, or terminate program.
    state = 5
    
    while True:
        
        ## Updates Current Time
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        elif(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_radial.position_control()
            # print('Updating PWM')
            
            # if (limit_A.check_limit()):
            #     state = 1
            if(radial_hpgl.empty()):
                state = 1
                
            if(flag_radial.get() == 0):
                state = 2
        
        elif(state == 1):
            motor_B.set_duty_cycle(0)
            
        elif(state == 2):
            motor_B.set_duty_cycle(0)
            
            if(flag_radial.get() == 1):
                state = 0
                
        elif(state == 3):
            print('Limit Has been hit!')
            state = 0

        #print('State: ', state)
        print('2')
        yield (0)
        
def update_pwm_theta ():
    """!
    Task which facilitates the motor position control method and records
    motor 1 data in a queue. The task then prints the data which is controlled
    by a generator.
    """
    
    ## State varible used to signal program whether to collect data, print
    #  data, or terminate program.
    state = 5
    
    while True:
        
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        ## Updates Current Time
        elif(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_theta.position_control()
 #           print('Error: ', error_theta.get())
            
            # if (limit_B.check_limit()):
            #     state = 1
            if(theta_hpgl.empty()):
                    state = 1
                    
            if(flag_theta.get() == 0):
                state = 2
        
        elif(state == 1):
            motor_A.set_duty_cycle(0)
            
        elif(state == 2):
            motor_A.set_duty_cycle(0)
            
            if(flag_theta.get() == 1):
                state = 0
            
        elif(state == 3):
            #print('Limit Has been hit!')
            state = 0
        print('3')
        yield (0)
        
def get_setpoint_r ():
    
    state = 5
        
    while True:
        
        
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        elif(state == 0):
            
            set_point_r.put(radial_hpgl.get())
            set_point_theta.put(theta_hpgl.get())
           # print('Radial Set Point: ', set_point_r.get())
            state = 1
            
        elif(state == 1):
        
            #print('Checking for error!!!! ', error_r.get())
            condition1 = control_radial.check_error()
            
            if(condition1 == True):
                state = 2
                
        elif(state == 2):
            flag_radial.put(0)
            condition2 = control_theta.check_error()
            print('Motor Radial')
            
            if (condition2 == True):
                state = 0
                flag_radial.put(1)
                print('!!!!!!!!!!!!!!!!! Checkpoint !!!!!!!!!!!!!!!!!')
                sol_pos = solenoid_hpgl.get()
                print('Sol: ', sol_pos)
                if sol_pos == 0:
                    my_sol.pen_up()
                elif sol_pos==1:
                    my_sol.pen_down()
            
        #     if (condition1 == True):
        #         state = 2
                
        # elif(state == 2):
        #     motor_B.set_duty_cycle(0)
        #     condition2 = control_theta.check_error()
            
        #     if(condition2 == True):
        #         state = 0
        print('4')        
        yield(0)
                
def get_setpoint_theta ():
    
    state = 5
        
    while True:
        
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        elif(state == 0):
            set_point_theta.put(theta_hpgl.get())
            #print('Theta Set Point: ', set_point_theta.get())
            state = 1
            
        elif(state == 1):
        
            condition2 = control_theta.check_error()
            
            if (condition2 == True):
                state = 2
                
        elif(state == 2):
            flag_theta.put(0)
            condition1 = control_radial.check_error()
            print('Motor Theta')
             
            if (condition1 == True):
                state = 0
                flag_theta.put(1)
                print('!!!!!!!!!!!!!!!!! Checkpoint !!!!!!!!!!!!!!!!!')
        print('5')
        #print(state)        
        yield(0)
        
def solenoid_control():
    print('Sol')
    while True:
        if flag_radial.get(0) and flag_theta.get(0):
            sol_pos = solenoid_hpgl.get()
            print(sol_pos)
            if sol_pos == 0:
                my_sol.pen_up()
            elif sol_pos==1:
                my_sol.pen_down()
    
        yield (0)
    

if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')
    
    radial_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 1)
    
    theta_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 2)
    solenoid_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 2)
    
    set_point_r = task_share.Share ('f', thread_protect = False, name = "Radial Set Point")
    
    set_point_theta = task_share.Share ('f', thread_protect = False, name = "Theta Set Point")
    
    error_r = task_share.Share ('f', thread_protect = False, name = "Radial Position Error")
    
    error_theta = task_share.Share ('f', thread_protect = False, name = "Theta Position Error")
    
    limit_flag_A = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch A")
    
    limit_flag_B = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch B")
    
    flag_zero = task_share.Share ('i', thread_protect = False, name = "System is zeroed")
    
    ## Creates the motor object for motor B
    motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)
    
    ## Creates the motor object for motor A
    motor_A = MotorDriver(pyb.Pin.board.PB5, pyb.Pin.board.PB4, pyb.Pin.board.PA10, 3)
    
    ## Creates the encoder object for encoder B
    enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    ## Creates the encoder object for encoder A
    enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    ## Create the position control object for system A
    control_theta = PositionControlTask(motor_A, enc_A, error_theta, set_point_theta, .006)    # controller for theta direction
    
    ## Creates the position control object for system B
    control_radial = PositionControlTask(motor_B, enc_B, error_r, set_point_r, .025) # controller for radial direction
    
    limit_A = Limit_Switch(pyb.Pin.board.PC2)
    
    limit_B = Limit_Switch(pyb.Pin.board.PB0)
    
    my_sol = Solenoid(pyb.Pin.board.PC4)
    
    my_hpgl = read_plotter.Hpgl(radial_hpgl, theta_hpgl, solenoid_hpgl, 85, 195)
    
    my_hpgl.read_data()
    
    my_hpgl.convert_data()
    
    origin = my_hpgl.convert_point(210,297)
    
    flag_theta = task_share.Share ('i', thread_protect = False, name = "Flag Theta Set is reached")
    
    flag_radial = task_share.Share ('i', thread_protect = False, name = "Flag Radial Set is reached")
    
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
    
    ## Task 2 used to operate motor 2 function task
    task5 = cotask.Task (zero_position, name = 'Zero Position', priority = 1, 
                             period = 10, profile = True, trace = False)
    
    gc.collect()
        
    # Add tasks to cotask schedular list
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)
    cotask.task_list.append (task5)
    
    while True:
        cotask.task_list.pri_sched()