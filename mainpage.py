'''@file                mainpage.py
   @brief               Brief doc for mainpage.py
   @details             Detailed doc for mainpage.py

   @mainpage 

   @section sec_intro1         Software Design
                               
                               Our program will consist of tasks position_control1, position_control2, encoder1, encoder2, solenoid_pos, and limitswitch.
                               The position control tasks will control the duty cycle of each motor individually and measure how far off in
                               ticks each encoder is from its desired position. As each encoder gets closer to its desired position, the duty
                               cycles will be decreasing to reach a final position without overshooot through closed loop position control.
                               The encoder tasks will be responsible for updating, reading, and setting encoder position for each motor. A critical part
                               to this project is finding a way to reset the set position for each motor based on the image we want to draw. We imagine
                               that we will be using a task that gets the g-code for the desired image, which tells us the set position in the radial and
                               theta direction for each move of the pencil. Next, the solenoid task will control wether the solenoid is on or off to move 
                               the pencil on and off the paper. Finally, the limitswitch task will read when the pencil has reached the end of the leadscrew, 
                               notifying the controller the motor needs to stop or switch direction to avoid system failure. 
                               
                               ALl tasks will be facilitated by a main program that runs each task through a task schedular. Additionally, all
                               shared and queued variables will be created within the main file. We expect each task to share encoder position
                               and duty cycle to control the motor speed. Additionally, there will be queue values to store encoder position 
                               and time data that will be printed at the end of a program run. 
                               
                               With all tasks ran simultaneously at differnt frequencies through the task schedular, our microcontroller should
                               be able to successfully control each motors speed and direction individually to move our pencil in the radial
                               and theta direction. The most difficult aspect of the code we envision is changining the desired position of 
                               each encoder based on the image we want the system to draw. We will need encoder ticks to paper position conversions,
                               that will be found through testing.
                               
   @subsection subsec_intro1   Task Diagram and Finite State Machines
   
                               Below is the Task Diagram of all tasks used to control the pencil position.
                               
                               Below is the Finite State Machine for our file controlling the set position of the pencil.
                        
                        
   @author                     Jameson Spitz
   @author                     Jacob Wong
   @author                     Wyatt Conner

   @copyright                  CC BY

   @date                       February 24, 2021
'''