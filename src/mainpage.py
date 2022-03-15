"""!
   @file                       mainpage.py

   @mainpage                   Thsi page serves as a summary of our softeware operations. Talsk about how tasks interacted with eachother, and contains our overall task diagram and Finite State Machine for our position control task.

   @section sec_intro1         Software Design
                               
                               Our program will consist of the task functions zero_position(), update_pwm_radial(), update_pwm_theta(), get_setpoint_r(), and get_setpoint_theta(). The zero_position() task sets the duty cycle of the motor controlling the radial direction to 45 so the pen moves towards home base (our y-offset) until it hits the limit switch. Once the limit switch triggers, the zero_position() task enters an empty state and triggers the position control phases to begin. The update_pwm tasks facilitate position control by setting the duty cycle of each respective motor based on the error between our encoder position and setpoint adjusted by our proportional gain value. As each encoder gets closer to its desired position, the duty cycles will be decreasing to reach a final position without overshooting via closed loop position control. The update_pwm tasks also check if a desired setpoint has been reached by an individual motor. In this case, that motor’s duty cycle is set to zero until the other motor reaches its setpoint. Once all setpoints have been reached, the duty cycle of each motor is set to zero to terminate the program. The get_setpoint() tasks are responsible for iterating to the next desired HPGL setpoint for each motor once the previous setpoint has been set. These tasks also flag once a setpoint has been reached, signaling to the updat_pwm tasks to stop the respective motor until the other motor's setpoint flag is triggered. 

                               All in all, our system works by performing closed loop position control on each motor individually, each having its own gain value and setpoints. The setpoints are acquired from HPGL and converted from raw dpi into encoder ticks that we specify for each motor. The setpoints for our radial and theta coordinates are iterated through once each motor has reached its desired setpoint within reasonable error. All tasks are facilitated by a main file, storing data in shares and queues so tasks and other files can share data. While each motor is being controlled, we integrated a solenoid to control the orientation of the pen acquired from HPGL setpoint data. Additionally, we use a limit_switch to ensure our pen position is set at the right zero point and does not move too far in the radial direction to damage our system. The main file runs all tasks through the task scheduler from the file co_task().
                               
   @section subsec_intro2      Task Diagram and Finite State Machines
   
                               Below is the Task Diagram of all tasks used to control the pencil position.
                               \image html TaskDiagram_FinalProj.jpg
                               
                               Below is the Finite State Machine for our the position control file of one motor.
                               \image html Fsm_TermProj.jpg
                        
   @author                     Jameson Spitz
   @author                     Jacob Wong
   @author                     Wyatt Conner

   @copyright                  CC BY

   @date                       March 10, 2022
"""