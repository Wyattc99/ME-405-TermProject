# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 08:31:32 2022

@author: wyatt
"""

from positioncontrol import PositionControlTask
from motordriver import MotorDriver
from encoderdriver import EncoderDriver
import pyb


#>>>>> Initlizing Class Objects <<<<<<

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
control_B = PositionControlTask(motor_B, enc_B)