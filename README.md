# Term Project
## Authors: Wyatt Conner, Jameson Spitz, Jacob Wong

## Introduction
The purpose of this project was to design a 2D plotter that can interpret an HPGL file and 
draw an image on paper. Our system controls the position of a pen by having our Nucleo 
microcontroller drive two motors, moving the pen along 2 axes. Additionally, the system 
must raise and lower the pen to control when the system is drawing.

## Hardware Design
To control the position of a pen, we designed a two degree of freedom system that operates 
in cylindrical coordinates R and Theta. We drive a lead screw actuator system using a motor 
to move the pen along the radial direction. The pen is secured to a 3D printed housing that 
is pushed by the lead screw along the main shaft of the assembly. The housing also holds a 
solenoid that performs the pen-up/pen-down action of the system.

To control movement of the housing in the theta direction, our system revolves about a pin joint 
connected to one end of a shaft, and a second motor drives a wheel on the other end of the shaft. 
See the images below for a CAD model and an image of the final prototype. All parts were either 
bought online, 3D printed, or found in our local Cal Poly machine shops.

### Assembly CAD Drawing
![Assembly Drawing and BOM](/Images/ASSEMBLY.JPG)

### Physical System Designed
![System Design](/Images/SystemDesign.jpg)

We needed 12V to power the solenoid. However,  the Nucleo is unable to provide such a voltage. 
Therefore, we use an external 12V-DC power supply, and we constructed circuitry using a MOSFET to 
control this voltage to the solenoid. This allows us to power and unpower the solenoid by setting 
a pin to high or low on the microcontroller. The schematic of the circuitry is shown below.

### Solenoid Wiring Diagram (Transistor and Diode)
![Solenoid Wiring1](/Images/Actual_Solenoid_Circuit.jpg){width = 50%}

### Theoretical Wiring Diagram
![Solenoid Wiring2](/Images/Solenoid.jpg)

Lastly, a limit switch is mounted on the main shaft to establish the zero point of the radial 
direction. Whenever the pen housing unit hits the limit switch, it sends a signal to the 
microcontroller to let the software know that housing is at this point.

## Software Design
The software for this project is a cooperative multitasking system that contains five tasks: a 
zeroing task, two tasks to set the desired position of the motors, and two tasks to set the duty
cycle of the motors. The zeroing task named 'Zero Position' sets the encoder position to zero
when the pen housing hits a limit switch, marking the zero position in the radial direction. The
desired position tasks called 'Radial Set Point Control' and 'Theta Set Point Control' reads the
HPGL file and converts X and Y coordinates to R and Theta coordinates. Then, the tasks store 
these coordinates in two queue objects. The two duty cycle tasks, called 'Radial Position Control'
and 'Theta Position Control' gather encoder data and desired position data from the previous two 
tasks. These tasks then implement closed-loop positional control to set the duty cycle going to 
each motor.

To convert X and Y data from the HPGL to R and Theta coordinates in the 'Set Point Control' 
tasks, we needed to derive two kinematic equations, one for R and one for Theta. Hand calculations
for these equations are pictured below.

### Inverse Kinematics Calculations
![Kinematics Sheet 1](/Images/hand_calcs_1.jpg)
![Kinematics Sheet 2](/Images/hand_calcs_2.jpg)

Each task is run using a finite state machine (FSM). The most important FSMs are in the 'Radial 
Position Control' and 'Theta Position Control' tasks. Both these task run using a similar FSM 
depicted by the State Transition Diagrm in the image below. In State 0, each task collects a new 
set point, or desired position for the motor. In State 1, each task calculates the error between
actual position (encoder data) and set point. If the error is above a specified threshold, it 
updates the duty cycle of the motor based on the error and returns to State 1. If the error is 
below the threshold, the tasks returns to State 0 to get a new set point. 

See a full description of our software and FSM and Task Diagram in the link to our repository:[Github Pages](https://wyattc99.github.io/ME-405-TermProject/)


## Results
To test our system, we began with testing each individual component separately. We first ran each 
motor to verify that we can control them separately. We next isolated the solenoid to ensure we 
can power and unpower it using the microcontroller. Lastly, we tested the limit switch by itself
and checked if the software can properly detect collision. 

Once we were ready to test the entire system together, our main focus was to verify that our 
kinematic relationships gave accurate results, adjust our threshold value for the error, and to 
tune the controller gains from our positional control loop. This test proved to be challenging,
and unfortunately, our system was unable to achieve satisfactory results. The desired image we
drew in Inkscape was a rectangle, but the image below is the drawing that our system produced.

### Resulting Rectangle
![Results](/Images/Results.jpg)

## Conclusion and Discussion
Although we were unable to create a successful 2D plotter before the deadline, we found several
issues that could be rectified in the future. One problem that we noticed was that the two
motors would reach their set points out of sync, meaning that one motor would have to wait for 
the other motor. To solve this, we could have interpolated between two setpoints to create 
several 'inbetween setpoints'. This would reduce the inaccuracies caused by the motors meeting
their setpoints at different times.

Another way we could have improved our software was to change the type of controller we used
in our positional control loop. Our current software uses a proportional (P) controller. Instead,
we could have implemented a PI controller to reduce the steady-state positional error. We could 
have even implemented a PID controller to decreased overshoot.


## Bill Of Materials


| Qty. | Part                    | Source                | Est. Cost |
|:----:|:----------------------  |:----------------------|:---------:|
|  1   | Wheel                   | 3D Printing           |     -     |
|  1   | Screw Eye               | Home Depot            |   $4.99   |
|  1   | Lead Screw              | Amazon                |   $12.99  |
|  1   | Solenoid                | Digi-Key              |   $4.95   |
|  3   | Limit Switches          | Amazon                |   $2.00   |
|  1   | Shaft Slider            | 3D Printing           |     -     |
|  1   | Pencil/Solenoid Housing | 3D Printing           |     -     |
|  1   | Duct Tape               | Home Depot            |   $6.87   |
|  2   | MOSFET                  | Friend in 405         |     -     |
|  1   | Diode                   | ME 405 Lab            |     -     |
|  3   | Zip Ties                | Friend in 405         |     -     |
|  5   | Wires/Solder            | ME 405 Lab            |     -     |
|  2   | Motors                  | ME 405 Lab            |     -     |
|  1   | Wood Block              | Home Depot            |   $8.25   |
|  1   | Shaft                   | Home Depot            |   $6.18   |
|  1   | Shaft Coupler           | Amazon                |   $3.98   |
|  1   | Wooden Peg              | Home Depot            |   $3.48   |

