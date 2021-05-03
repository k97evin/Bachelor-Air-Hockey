import pygame
import pymunk
import math
from pymunk import Vec2d
import datetime

import puck_velocity
import time
import matplotlib.pyplot as plt

def velocity(puck_pos):
    
    vec = [Vec2d(pos[0],pos[1]) for pos,t in puck_pos]
    t = [t for pos,t in puck_pos]
    
    #vec1 = Vec2d(puck_pos[0][0],puck_pos[0][1])
    #vec2 = Vec2d(puck_pos[1][0],puck_pos[1][1])

    velocityVec = []
    
    if len(vec) > 4:  
        new_dir = vec[4][0]-vec[3][0]

        if new_dir.length > 2.0:
            td = t[4]-t[3]
            velocityVec = new_dir/(td.total_seconds())
            return velocityVec

        elif 1.0 < new_dir.length <= 2.0:
            new_dir = vec[4]-vec[2]
            td = t[4]-t[2]
            velocityVec = new_dir/(td.total_seconds())
            return velocityVec
        else:
            return Vec2d.zero()
    else:
        return Vec2d.zero()


#puck_pos = [[[1,2],5], [[10,20],50]]


#vec = [Vec2d(pos[0],pos[1]) for pos,t in puck_pos]
#vec1 = [pos[0]+pos[1] for pos,t in puck_pos]
#t = [t for pos,t in puck_pos]

#print(vec)
#print(vec1)
#print(t)

puck_pos = [[[100,300],1], [[10,20],50]]

pos = []

x = 0
for x in range(6):
    t = datetime.datetime.now()
    time.sleep(0.1)
    
    pos.append([[1000-x*50,400-x*50],t])
    print(pos[x-1])
    x+=1

pf = puck_velocity.puck_velocity2(pos)
print("Vvec: " + str(pf))