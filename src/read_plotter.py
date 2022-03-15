"""!
@file read_plotter.py
This file reads our HPGL setpoints from a csv file. The data is organized into two lists, the x and y coordinates. The file also 
has a method to convert our adjusted HPGL data from cartesion coordinated in mm into polar coordinates in mm and radians. The inverse
kinematics to calculate our polar coordinates was a tedious and key calculation in order to output the correct setpoints.
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   3-March-22
@copyright by Jacob Wong all rights reserved
"""

import math as m

class Hpgl:
    """!
    Converts raw HPGL data in dpi into cartesian coordinates and then polar coordinates.
    """
    
    def __init__ (self, radial_hpgl, theta_hpgl, solenoid_hpgl, offset_x, offset_y):
        
        """!
        Initializes queue variables to store radial, theta, and pen up/down setpoint data. System characteristics such as the encoder ticks per rotation, 
        lead screw pitch, wheel and square beam radii, and pen offset data are defined.
        @param radial_hpgl Queue variable to store radial setpoint data
        @param theta_hpgl Queue variable to store theta setpoint data
        @param solenoid_hpgl Queue variable to store solenoid up/down set point data
        @param offset_x Accounts for pen offset from center of rotation in x direction
        @param offset_y Accounts for pen offset from center of rotation in y direction
        """
        ## Queue variable storing radial setpoint data
        self.radial_hpgl = radial_hpgl
        
        ## Queue variable storing theta setpoint data
        self.theta_hpgl = theta_hpgl
        
        ## Queue variable storing pen up/down setpoint data
        self.solenoid_hpgl = solenoid_hpgl
        
        ## Offest from center of rotation in x direction
        self.offset_x = offset_x
        
        ## Offest from center of rotation in y direction
        self.offset_y = offset_y
        
        ## Offest from center of rotation in x direction
        self.pitch = 8
        
        ## Encoder ticks per rotation
        self.rotation = 16_384
        
        ## radius of wheel in mm
        self.R_wheel = 80
        
        ## Radius of peg to wheel in mm
        self.R_main = 560
        
    def read_data(self):  
        """!
        This method parses through the csv file containing HPGL setpoint data, and converts the data into two lists of
        x and y data, converting the raw HPGl from dpi to mm. The file also stores the pen up and pen down commands from
        the HPGL.
        """
        
        ## stores hpgl data as list of characters
        rows = []
        
        ## Placeholder to contain each hpgl coordinate output as a string
        string = ''
        
        ## Iterates from 0 to one less than the length of characters.
        i = 0
        
        ## Indicates wether HPGL coordinate chould be added to the x list or y list
        runs = 0
        
        ## Checks if a character from HPGL is numeric
        num = False
        
        ## Indicated the desired orientation of solenoid
        sol_pos = 0
        
        with open('test4.hpgl', 'r') as plotter:            # Open the HPGL file
            
            for line in plotter:                            # Parse through every character of each line of the HPGL
                for character in line:
                    rows.append(character)                  # Append each character to the rows list
                    
                while runs <= 1:

                    if(i >= len(rows)):                     # Run while i is less than the total count of character
                        runs = 2
                    
                    elif (rows[i] == '.'):                  # Add  decimal point to HPGL coordinate in case it is a float
                        string += rows[i]
                         
                    try:                                    # Try to convert HPGL character into an integer. If int, add the character to string
                        int(rows[i])                 
                        string += str(rows[i])
                        num = True
                        
                    except: 
                        pass                                # If not int, pass
                        
                    if (i < len(rows)):
                        
                        if(rows[i] == 'D' or rows[i] == 'U'):         # Check desired position of solenoid based on 'U' or 'D' indicator
                            if rows[i] == 'D':
                                sol_pos = 1
                            elif rows[i] =='U':
                                sol_pos = 0
                        
                        if(rows[i] == ',' or rows[i] == ';'):         # Add string to respective setpoint list based once a comma or semi-colon has indicated
                            
                            if(num):                                  # Convert the raw HPGL data drom dpi to mm
                                x = round(float(string)/1016*25.4,2)  
                                y = round(float(string)/1016*25.4,2)
                                
                                if runs == 0:             
                                    self.radial_hpgl.put(x)                    # Add x corrdinate data to radial queue
                                    self.solenoid_hpgl.put(sol_pos)            # Add pen position to solenoid queue
                                    runs = 1
                                elif runs == 1:
                                    self.theta_hpgl.put(y)                     # Add y coordinate data to theta queue
                                    runs = 0
                                
                            string = ''
                            num = False
                        
                        print(sol_pos)
                            
                    
                    i += 1                                           # Increment the index of rows
                               
                       
                i = 0                                                # Reset parameters for next run
                rows = []            
                runs = 0
                
    def convert_data(self):
        """!
        Re-writes the cartesian setpoint data as polar setpoints in the same radial and theta queue variables. 
        """
        
        ## Placeholder for the x-coordinate data
        x_data = []
        
        ## Placeholder for the y-coordinate data
        y_data = []
        
        ## Initial value of theta to calculate first Radial coordinate
        theta = 0
        
        while self.radial_hpgl.any():
            y_data.append(self.radial_hpgl.get())          # Empty radial queue into placeholder list
         
        while self.theta_hpgl.any():
            x_data.append(self.theta_hpgl.get())           # Empty theta queue into placeholder list
            
        print('Length X: ', len(x_data))                   # Printing for troubleshooting
        print('Length Y: ', len(y_data))
        
        for i in range (0, len(x_data)):                   # Iterate through placeholder lists, converting each respective list to polar
           
            # Convert Cartesian Cordiantes
            R_T = ((x_data[i] + self.offset_x - self.offset_x*m.sin(m.pi/2 - theta))**2 + (y_data[i] + self.offset_y + self.offset_x*m.cos(m.pi/2-theta))**2)**(.5)    # Inverse kinematics to find setpoints, see README for analysis
            R_desired = R_T - self.offset_y                                                                                                                            # Account for radial offset
            self.rad_enc1 = self.rotation*(R_desired)/self.pitch                                                                                                       # Convert to ticks
            
            theta = m.atan((x_data[i]+self.offset_x)/(y_data[i] + self.offset_y)) - m.atan(self.offset_x/R_T)                                                          # Finds theta setpoint in radians, see README
                 
           
                    
            self.rad_enc2 = (self.R_main/self.R_wheel)*theta*self.rotation/(2*m.pi)                                                                                    # Converts radians to ticks, and converts the rotation of the shaft to the rotation of the wheel.
            
            self.radial_hpgl.put(self.rad_enc1)            # Re-write setpoints into queue variables
            self.theta_hpgl.put(self.rad_enc2)
            print ('x:', x_data[i], 'y:', y_data[i])
            print ('r:', R_desired, 'theta:',theta)
            

            

              