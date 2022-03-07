import math as m
                
def convert(self, offset, X, Y):
    self.pitch = 8
    self.offset = offset
    self.X = X
    self.Y = Y
    self.rotation = 16_384
    self.R_wheel = 1
    self.R_main = 2
    
    # Convert Cartesian Cordiantes
    self.R = m.isqrt((self.X)^2 + (self.Y)^2) + self.offset
    self.rad_enc1 = (self.R - self.offset)/self.pitch
    
    self.theta = m.tan(self.Y/self.X)
    self.rad_enc2 = (self.R_main/self.R_wheel)*self.theta
    
    self.enc1_tick = (2*self.rotation/m.pi)*self.rad_enc1
    self.enc2_tick = (2*self.rotation/m.pi)*self.rad_enc2
    
    return(self.enc1_tick, self.enc2_tick)
    
    