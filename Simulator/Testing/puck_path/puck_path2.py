import pygame
import pymunk
import math
from pymunk import Vec2d

# Screen size
width, height = 1200,600

# Table dimensions
scaling = 7
table_width = int(160*scaling) #Playable area
table_height = int(70*scaling) #Playable area
puck_radius = int(7/2*scaling)
pusher_radius = int(9.6/2*scaling)
goal_size = 30*scaling

# wall varaibles
wall_thickness = 10

# Outer values
left = (width-table_width-2*wall_thickness)/2
right = width-left
top = (height-table_height-2*wall_thickness)/2
bottom = height-top

# Puck center reachable positions
puck_topPos = top + wall_thickness + puck_radius
puck_bottomPos = bottom - wall_thickness - puck_radius
# Pusher center reachable positions
pusher_distFromWall = 10 #The closest the pusher can get to the wall
puck_leftPos = left + wall_thickness + pusher_distFromWall + pusher_radius #kanskje ligge til: + puck_radius

import joblib
from pathlib import Path
path =  Path(__file__).parent

model = joblib.load(path/'model.joblib')
def rotate_vel(velocity):
    print("Roter")
    angle_inn = velocity.angle
    print(angle_inn)
    angle_out = model.predict([[abs(angle_inn)]])[0][0]
    print(angle_out)

    rotated_velocity = velocity
    if angle_inn < 0:
        rotated_velocity = velocity.rotated(angle_inn+angle_out)

    if angle_inn > 0:
        rotated_velocity = velocity.rotated(-angle_inn-angle_out)

    return rotated_velocity

def path_points(puck_velocity,puck_pos):

    P = puck_pos
    last_velocity = puck_velocity
    totalTime = 0
    t = 0
    points = []
    calculate = False
    #while P[0] > puck_leftPos:
    points.append(P)
    print(points)
    totalTime += t
    if last_velocity[0] < 0 and last_velocity[1] < 0:
        print("ja")
        t = (puck_topPos - puck_pos[1])/puck_velocity[1]
        Px = puck_pos[0] + puck_velocity[0]*t
        print(Px)
        print(t)


        P  = [Px,puck_topPos]
        print(P)
        puck_velocity = rotate_vel(last_velocity)
        print(puck_velocity)
        calculate = True

    if puck_velocity[0] <= 0 and puck_velocity[1] > 0:
        print("ja2")
        t = (puck_bottomPos - puck_pos[1])/puck_velocity[1]
        Px = puck_pos[0] + puck_velocity[0]*t

        P = [Px,puck_bottomPos]
        puck_velocity = rotate_vel(last_velocity)
        calculate = True


    if calculate:
        t = (puck_leftPos-points[-1][0])/last_velocity[0]
        totalTime += t

        Py = points[-1][1]+last_velocity[1]*t
        
        P = [puck_leftPos,Py]
        points.append(P)

 
    #print(points)
    return points