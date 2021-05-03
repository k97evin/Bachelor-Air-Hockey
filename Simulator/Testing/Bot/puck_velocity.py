import pygame
import pymunk
import math
from pymunk import Vec2d
import datetime


# Screen size
width, height = 1200,600

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,127,80)
BLACK = (0,0,0)
CYAN = (0,255,255)

# Table dimensions
scaling = 7
table_width = int(160*scaling)
table_height = int(70*scaling)
puck_radius = int(7/2*scaling)
pusher_radius = int(9.6/2*scaling)
goal_size = 30*scaling

# wall varaibles
wall_thickness = 10

left = (width-table_width-2*wall_thickness)/2
right = width-left
top = (height-table_height-2*wall_thickness)/2
bottom = height-top

vertical_wall_size = [wall_thickness, table_height+2*wall_thickness]
horisontal_wall_size = [table_width+2*wall_thickness, wall_thickness]



def velocity(puck_pos, last_puck_pos, last_dir):
    
    vec1 = Vec2d(puck_pos[0],puck_pos[1])
    vec2 = Vec2d(last_puck_pos[0],last_puck_pos[1])
    new_dir = vec1-vec2

    
    if new_dir.length > 0.1:
        return new_dir
    

    else:
        return Vec2d.zero()




def velocity2(puck_pos):
    
    vec = [Vec2d(pos[0],pos[1]) for pos,t in puck_pos]
    t = [t for pos,t in puck_pos]
    
    #vec1 = Vec2d(puck_pos[0][0],puck_pos[0][1])
    #vec2 = Vec2d(puck_pos[1][0],puck_pos[1][1])

    velocityVec = []
    
    if len(vec) > 4:  
        new_dir = vec[4]-vec[3]

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







# test 
# import time
# import matplotlib.pyplot as plt

# puck_pos = [[[100,300],1], [[10,20],50]]

# pos = []
# t = []
# x = []
# y = []

# i = 0
# for i in range(5):
#     time.sleep(0.5)
#     t.append(datetime.datetime.now())
    
#     pos.append([[1000-i*50,400-i*0],t[i]])
#     print(pos[i])

#     x.append(pos[i][0][0])
#     y.append(pos[i][0][1])
#     i+=1

# deltaT = t[4]-t[3]
# deltaT = deltaT.total_seconds()
# print("Tid: " + str(deltaT))
# pf = velocity2(pos)
# print("Vvec: " + str(pf))

# print(pos[0][0][0])
# print(x)
# print(y)

#plt.plot(x,y)
#plt.show()
