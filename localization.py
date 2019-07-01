#!/usr/bin/env python
# coding: utf-8

# given camera angle of the task and the change of angle, create a weight distribution in shape of a cone and shift the weight distribution as camera/sub angle changes

# In[1]:


import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
import copy


# In[2]:


#NOTE: The whole class can be sped up, if necessary, with vectorizing in numpy
#TODO: Multiple objects


class particleFilter():
    particleMat = []
    def __init__(self, angleAmount):
        ''' 
        angleAmount is the number of angle we want in particleMat. 
        coordinate: say we use polar with 0 in Cartesian positve x direction. It goes [0,len(angleAmount)), 
        which we will output by mapping this to [0,360), or whatever the sub takes
        '''
        self.particles = angleAmount
        self.particleMat = [ 0 for i in range(self.particles) ]
        self.i_to_angle = 360/angleAmount
    
    def resetWeights(self):
        self.particleMat = [ 0 for i in range(self.particles) ]
        
    def addTask(self):
        pass
    
    def updateAngle(self,newAngle,stdev):
        '''
        data will be the input data in angles, most likely one single input and error in angle. 
        angle might need adjustment to fit our coordinates.
        error might need treatment to become standard deviation
        '''
        '''
        increase prob for "angle", bc we see angle.
        '''
        #Might want to change to adust number of measurements to change weights
        fWeight = 0.3
        
        for i in range(len(self.particleMat)):
            angle = int(round(i*self.i_to_angle))
            angleDiff = min([math.fabs(angle - newAngle),math.fabs(newAngle-angle+360)])
            gaussDelta =  math.e**( -angleDiff*angleDiff / (2* stdev**2) )
            self.particleMat[i] = fWeight*gaussDelta+ (1-fWeight)*self.particleMat[i]
        
        #normalize
        if sum(self.particleMat)>360:
            total = 360/sum(self.particleMat)
            self.particleMat = [i*total for i in self.particleMat]
        
    def updateCameraAngle(self,cameraChange):
        newAng = [0 for i in range(len(self.particleMat))]
        for i in range(len(self.particleMat)):
            angIdx = int(round(cameraChange/self.i_to_angle))
            if i-angIdx>=0:
                newAng[i-angIdx]=self.particleMat[i]
            else:
                newAng[i+int(round((360-cameraChange)/self.i_to_angle))]=self.particleMat[i]
        self.particleMat = newAng
        
    def getPredictedState(self):
        angles = [x*self.i_to_angle for x in range(0, self.particles)]
        max_x = angles[array(self.particleMat).argmax()] 
        stDev = np.std(np.array(self.particleMat), axis = 0)
        return max_x, self.particleMat[(int)(max_x/self.i_to_angle)]
    


# Proposed Move Condition
# particle.getPredictedState will return a vector of 3 values:
#     1) Predicted angle
#     2) Weight at angle
#     3) Sum of weights
#    
# We use quantity 3 to evaluate "accumulation," or whether we had enough measurements to start predicting angle data.
# 
# Once the weight at angle is higher than, say, 120, we next use quantity 2 to calculate "certainty." I suggest, based of very crude estimate, a weight of .97 as a threshold of certainty.
# 
# Our idea is to turn toward that weight, then go forward. Once the angle gets too far from origin, we reset the angle matrix.

# In[6]:

#SAMPLE:
'''
particle = particleFilter(360)
a=particle.updateAngle(90,50)
for i in range(10):
    a=particle.updateAngle(90,50)
for i in range(100):
    a=particle.updateAngle(45,50)
    a=particle.updateAngle(0,50)
    
    
for i in range(359):
    plt.polar(i/180*math.pi, particle.particleMat[i],"bo")
print(particle.getPredictedState())
'''




