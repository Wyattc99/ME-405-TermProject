"""!
@file read_plotter.py
This file reads our HPGL setpoints from a csv file. The data is organized into two lists, the x and y coordinates. 
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   26-Jan-22
@copyright by Jacob Wong all rights reserved
"""

import math as m

class Hpgl:
    
    def __init__ (self, radial_hpgl, theta_hpgl, solenoid_hpgl, offset_x, offset_y):
        self.radial_hpgl = radial_hpgl
        self.theta_hpgl = theta_hpgl
        self.solenoid_hpgl = solenoid_hpgl
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pitch = 8
        self.rotation = 16_384
        self.R_wheel = 80
        self.R_main = 560
        
    def read_data(self):    
        
        rows = []
        string = ''
        i = 0
        runs = 0
        num = False
        sol_pos = 0
        
        with open('test4.hpgl', 'r') as plotter:
            
            for line in plotter:
                for character in line:
                    rows.append(character)
                    
                while runs <= 1:

                    if(i >= len(rows)):
                        runs = 2
                        
                    #     if (rows[i] == 'D'):
                    #         pen_orientation.append(1)
                    #         string += rows[i]
                    #     elif (rows[i] == 'U'):
                    #         pen_orientation.append(2)
                    #         string += rows[i]
                    
                    elif (rows[i] == '.'):
                        string += rows[i]
                        
                    try:
                        int(rows[i])
                        string += str(rows[i])
                        num = True
                        
                    except: 
                        pass
                        
                        
                    # elif (unicode(rows[i]).isnumeric()):
                    #     string += str(rows[i])
                    #     num = True
                   
                    if (i < len(rows)):
                        
                        if(rows[i] == 'D' or rows[i] == 'U'):
                            if rows[i] == 'D':
                                sol_pos = 1
                            elif rows[i] =='U':
                                sol_pos = 0
                        
                        if(rows[i] == ',' or rows[i] == ';'):
                            
                            if(num):
                                x = round(float(string)/1016*25.4,2)
                                y = round(float(string)/1016*25.4,2)
                                
                                if runs == 0:
                                    self.radial_hpgl.put(x)
                                    self.solenoid_hpgl.put(sol_pos)
                                    runs = 1
                                elif runs == 1:
                                    self.theta_hpgl.put(y)
                                    runs = 0
                                    
                            # elif(pen_flag):
                                
                            #     if runs == 0:
                            #         self.radial_hpgl.put(string)
                            #     elif runs == 1:
                            #         self.theta_hpgl.put(string)
                                
                            string = ''
                            num = False
                        
                        print(sol_pos)
                            
                    
                    i += 1
                               
                       
                i = 0
                rows = []            
                runs = 0
                
    def convert_data(self):
        
        x_data = []
        y_data = []
        theta = 0
        theta = 0
        
        while self.radial_hpgl.any():
            y_data.append(self.radial_hpgl.get())
         
        while self.theta_hpgl.any():
            x_data.append(self.theta_hpgl.get())
            
        print('Length X: ', len(x_data))
        print('Length Y: ', len(y_data))
        
        for i in range (0, len(x_data)):
           
            # Convert Cartesian Cordiantes
            R_T = ((x_data[i] + self.offset_x - self.offset_x*m.sin(m.pi/2 - theta))**2 + (y_data[i] + self.offset_y + self.offset_x*m.cos(m.pi/2-theta))**2)**(.5)
            R_desired = R_T - self.offset_y
            self.rad_enc1 = self.rotation*(R_desired)/self.pitch
            
            theta = m.atan((x_data[i]+self.offset_x)/(y_data[i] + self.offset_y)) - m.atan(self.offset_x/R_T)
                
           
                    
            self.rad_enc2 = (self.R_main/self.R_wheel)*theta*self.rotation/(2*m.pi)
            
            self.radial_hpgl.put(self.rad_enc1)
            self.theta_hpgl.put(self.rad_enc2)
            print ('x:', x_data[i], 'y:', y_data[i])
            print ('r:', R_desired, 'theta:',theta)
            
    def convert_point(self, X, Y):
            
            # Convert Cartesian Cordiantes
            self.R = ((X + self.offset_x)**2 + (Y+self.offset_y)**2)**(.5)
            self.rad_enc1 = self.rotation*(self.R - self.offset_y)/self.pitch
            
            try:
                self.theta = m.atan(Y/X)
                
            except:
                self.theta = m.pi/2

                    
            self.rad_enc2 = (self.R_main/self.R_wheel)*self.theta*self.rotation/(2*m.pi)
            
            return (self.rad_enc1, self.rad_enc2)
            

            

              