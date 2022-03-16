"""!
@file main.py
The main file of the term project that creates and runs the tasks needed to control
the 2 axis drawing robot we created. To do this we create each task as a method
that interacts with the firmware, and these tasks are then ran using cotask. 
@author Wyatt Conner
@author Jacob Wong
@author Jameson Spitz
@date 5-Mar-22
@copyright by Jameson Spitz all rights reserved

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
    When this task is called it will zero the 2 axis drawing robot back to its
    orgin which is located by 2 limit switches along its radial axis and angular
    axis. Once each limit switch has been touched the method will terminate and
    turn off each motor. 
    """
    
    ## Zero B is a flab to show that the motor B has finished its zeroing process
    zero_B = False
    print('Beginning Zeroing Proccess')
    
    ## State of the Zero Position Method to determine what state the finite state machine is in
    state = 0
    
    while True:
        
        # if (limit_A.check_limit()):
        # 210, 297 mm
        # set the duty to be constant until it hits the switch for motor A
        
        # Check the limit switch if it has been triggered
        if (state == 0):
        # set the duty to be constant until it hits the switch for motor B
            print(limit_flag_B.get())
            limit_flag_B.put(limit_B.check_limit())
            
            # Turn the motor on if the flag is off and has never been turned on
            if limit_flag_B.get() == 0 and zero_B == False:
                pass
                motor_B.set_duty_cycle(45)
            
            # Turn the motor off and set the encoder positions
            elif limit_flag_B.get() == 1:
                motor_B.set_duty_cycle(0)
                ## Zero_B is a flag to represent once the limit switch has been turned on once this flag will remain on to prevent oscillations of the switch
                zero_B = True
                enc_B.set_position(-3000)
                
                state = 1
                
                
        # Print the encoder positions to ensure they are zero'd
        if (state == 1):
            print(enc_A.get_position())
            print(enc_B.get_position())
            flag_zero.put(1)
            state=2
            
        if (state==2):
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
    
    ## State varible used to signal program whether to collect data, print or when to terminate the method
    state = 5
    
    while True:
        
        # We will remain in state 5 until the machine is zero'd to begin drawing.
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
        # State 0 is when we begin to control each motor for our set data points. 
        elif(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_radial.position_control()
            
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
    This is the method that controls the motor along the angular axis of the robot.
    This is done by updating the set point for the motor once each motor as reached
    their previous set points. Then conduct position control on the motor until it hits
    its new set point, then turn off the motor and wait for the radial axis to hit its set
    point. 
    """
    
    ## State varible used to signal program whether to collect data, print, data, or terminate program.
    state = 5
    
    while True:
        
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        
        elif(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_theta.position_control()
            
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
            state = 0
        print('3')
        yield (0)
        
def get_setpoint_r ():
    """!
    This method is used to control the motor along the radial axis of the robot.
    The way this is done is that the set point is given from our read plotter file.
    We then conduct a position control for this set point and once the motor is
    within a window of error that is acceptable the motor will turn off and set
    a flag that it has meet it's set point. Once both motors have meet their set
    points they will then update to a new setpoint and do the entire process again. 
    """
    ## State varible used to signal program whether to collect data, print, data, or terminate program.
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
        
            ## Condition 1 checks if the radial motor is within its acceptable error limit to say it has meet its set point.
            condition1 = control_radial.check_error()
            
            if(condition1 == True):
                state = 2
                
        elif(state == 2):
            flag_radial.put(0)
            ## Condition 2 checks if the theta motor is within its acceptable error limit to say it has meet its set point. 
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
    
        print('4')        
        yield(0)
                
def get_setpoint_theta ():
    """!
    This method is used to update the set point of the motor on the theta axis.
    If both motors have reached their setpoints this method will update the
    setpoint of the theta motor. The set point data is provided from the read 
    plotter file. 
    """
    
    ## State varible used to signal program whether to collect data, print, data, or terminate program.
    state = 5
        
    while True:
        
        if (state == 5):
            if (flag_zero.get() == 1):
                state = 0
                
        elif(state == 0):
            set_point_theta.put(theta_hpgl.get())
            state = 1
            
        elif(state == 1):
            ## Condition 2 checks if the theta motor is within its acceptable error limit to say it has meet its set point. 
            condition2 = control_theta.check_error()
            
            if (condition2 == True):
                state = 2
                
        elif(state == 2):
            flag_theta.put(0)
            ## Condition 1 checks if the radial motor is within its acceptable error limit to say it has meet its set point.
            condition1 = control_radial.check_error()
            print('Motor Theta')
             
            if (condition1 == True):
                state = 0
                flag_theta.put(1)
                print('!!!!!!!!!!!!!!!!! Checkpoint !!!!!!!!!!!!!!!!!')
        print('5')
        #print(state)        
        yield(0)
    

if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')
    
    ## This a Queue of encoder tick set points for the radial motor converted from hpgl file.
    radial_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 1)
    
    ## This a Queue of encoder tick set points for the angular motor converted from hpgl file.
    theta_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 2)
    
    ## This creates a queue for the solenoid to instruct when the solenoid should be on or off.
    solenoid_hpgl = task_share.Queue('f', size = 250, thread_protect = False,
                                      overwrite = False, name = 2)
    
    ## This create the share object is to set the radial set point within each task for any given moment.
    set_point_r = task_share.Share ('f', thread_protect = False, name = "Radial Set Point")
    
    ## This creates the share object is to set the theta set point within each task for any given moment.
    set_point_theta = task_share.Share ('f', thread_protect = False, name = "Theta Set Point")
    
    ## This share object is the error of the radial encoder from its set point to set duty and determine when it has reached the set point. 
    error_r = task_share.Share ('f', thread_protect = False, name = "Radial Position Error")
    
    ## This share object is the error of the theta encoder from its set point to set duty and determine when it has reached the set point. 
    error_theta = task_share.Share ('f', thread_protect = False, name = "Theta Position Error")
    
    ## This create the share object is used to signal when the limit flag on the angular axis is triggered
    limit_flag_A = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch A")
    
    ## This create the share object is used to signal when the limit flag on the radial axis is triggered
    limit_flag_B = task_share.Share ('i', thread_protect = False, name = "Flag for Limit Switch B")
    
    ## This creates the share object to signify once both limit flags are true to represent when the system is at the orgin.
    flag_zero = task_share.Share ('i', thread_protect = False, name = "System is zeroed")
    
    ## Creates the motor object for motor of the radial direction
    motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)
    
    ## Creates the motor object for motor of the angualr direction
    motor_A = MotorDriver(pyb.Pin.board.PB5, pyb.Pin.board.PB4, pyb.Pin.board.PA10, 3)
    
    ## Creates the encoder object for encoder of the radial radial direction
    enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    ## Creates the encoder object for encoder of the angualr direction
    enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    ## Create the position control the position of the motor along the angualr axis
    control_theta = PositionControlTask(motor_A, enc_A, error_theta, set_point_theta, .006)    # controller for theta direction
    
    ## Creates the position control the position of the motor along the radial axis
    control_radial = PositionControlTask(motor_B, enc_B, error_r, set_point_r, .025) # controller for radial direction
    
    ## Creaates the limit switch object to interact with the hardware of the switch on the angualr axis
    limit_A = Limit_Switch(pyb.Pin.board.PC2)
    
    ## Creates the limit switch object to interact with the hardware of the switch on the radial axis
    limit_B = Limit_Switch(pyb.Pin.board.PB0)
    
    ## Create the solenoid object to interact with the circuit connected to the solenoid to make it turn on and off
    my_sol = Solenoid(pyb.Pin.board.PC4)
    
    ## THis create the object of the read_plotter file to send it the raw data of the hpgl to be converted to our radial and angualr set points we need.
    my_hpgl = read_plotter.Hpgl(radial_hpgl, theta_hpgl, solenoid_hpgl, 85, 195)
    
    my_hpgl.read_data()
    
    my_hpgl.convert_data()
    
    ## This is the numerical value of our orgin of our system as it offset from the center of rotation, this value is measured in millimeters.
    origin = my_hpgl.convert_point(210,297)
    
    ## This creates a flag that is a share object of when the set point is reached along the angualr axis.
    flag_theta = task_share.Share ('i', thread_protect = False, name = "Flag Theta Set is reached")
    
    ## This creats a flag that is a share object of when the set point is reached along the radial axis.
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