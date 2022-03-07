# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 08:52:53 2022

@author: james
"""

import math as m

class Hpgl:
    
    def __init__ (self, radial_hpgl, theta_hpgl, offset):
        self.radial_hpgl = radial_hpgl
        self.theta_hpgl = theta_hpgl
        self.offset = offset
        
    def read_data(self):    
        
        rows = []
        string = ''
        i = 0
        runs = 0
        pen_orientation = []                # Pen is down when '2'
        pen_flag = False
        num = False
        
        with open('test2.hpgl', 'r') as plotter:
            
            for line in plotter:
                for character in line:
                    rows.append(character)
                    
                print(rows)
                    
                while runs <= 1:

                    if(i >= len(rows)):
                        runs = 2
                        
                    # elif(rows[i] == 'D' or rows[i] == 'U'):
                        
                    #     pen_flag = True
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
                        print(string)
                        num = True
                        
                    except: 
                        pass
                        
                        
                    # elif (unicode(rows[i]).isnumeric()):
                    #     string += str(rows[i])
                    #     num = True
                   
                    if (i < len(rows)):
                        
                        if(rows[i] == ',' or rows[i] == ';' or pen_flag):
                            
                            if(num):
                                x = round(float(string)/1016*25.4,2)
                                y = round(float(string)/1016*25.4,2)
                                
                                if runs == 0:
                                    self.radial_hpgl.put(x)
                                    runs = 1
                                elif runs == 1:
                                    self.theta_hpgl.put(y)
                                    runs = 0
                                    
                            elif(pen_flag):
                                
                                if runs == 0:
                                    self.radial_hpgl.put(string)
                                elif runs == 1:
                                    self.theta_hpgl.put(string)
                                
                            string = ''
                            num = False
                            pen_flag = False
                            
                    i += 1
                               
                       
                i = 0
                rows = []            
                runs = 0
                
    def convert_data(self):
        
        radial_data = []
        theta_data = []
        
        while self.radial_hpgl.any():
            radial_data.append(self.radial_hpgl.get())
         
        while self.theta_hpgl.any():
            theta_data.append(self.theta_hpgl.get())
            
        print(radial_data)
        print('\n', theta_data)
            
        for i in range (0, len(radial_data)):
            
            # if (radial_data[i].isnumeric() and theta_data[i].isnumeric()):
            self.pitch = 8
            self.rotation = 16_384
            self.R_wheel = 1
            self.R_main = 2
            
            # Convert Cartesian Cordiantes
            self.R = ((radial_data[i])**2 + (theta_data[i])**2)**(.5) + self.offset
            self.rad_enc1 = (self.R - self.offset)/self.pitch
            
            try:
                self.theta = m.tan(theta_data[i]/radial_data[i])
                
            except:
                if (theta_data[i] > 0):
                    self.theta = m.pi/2
                elif(theta_data[i] < 0):
                    self.theta = -m.pi/2
                else:
                    self.theta = 0
                    
            self.rad_enc2 = (self.R_main/self.R_wheel)*self.theta
            
            self.radial_hpgl.put((2*self.rotation/m.pi)*self.rad_enc1)
            self.theta_hpgl.put((2*self.rotation/m.pi)*self.rad_enc2)
            

              