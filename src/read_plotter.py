# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 08:52:53 2022

@author: james
"""
class Hpgl:
    
    def __init__ (self, radial_hpgl, theta_hpgl):
        self.radial_hpgl = radial_hpgl
        self.theta_hpgl = theta_hpgl
        
    def read_data(self):    
        
        rows = []
        string = ''
        i = 0
        runs = 0
        pen_orientation = []                # Pen is down when '2'
        pen_flag = False
        num = False
        
        with open('Test1.hpgl', 'r') as plotter:
            
            for line in plotter:
                for character in line:
                    rows.append(character)
                    
                while runs <= 1:
    
                    if(i >= len(rows)):
                        runs = 2
                        
                    elif(rows[i] == 'D' or rows[i] == 'U'):
                        
                        pen_flag = True
                        if (rows[i] == 'D'):
                            pen_orientation.append(1)
                            string += rows[i]
                        elif (rows[i] == 'U'):
                            pen_orientation.append(2)
                            string += rows[i]
                        
                    elif (rows[i].isnumeric()):
                        string += str(rows[i])
                        num = True
                        
                    elif (rows[i] == '.'):
                        string += rows[i]
                   
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

              