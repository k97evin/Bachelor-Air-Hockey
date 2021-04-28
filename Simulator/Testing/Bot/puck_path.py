import pygame
import pymunk
import math
from pymunk import Vec2d

# Screen size
width, height = 1200,600
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

def path(puck_dir,pos):
    #print("se her: ",puck_dir)
    puck_dir = Vec2d(puck_dir[0],puck_dir[1])
    points = [(pos[0],pos[1])]
    x,y = pos
    angle = puck_dir.angle
    k = math.tan(angle)  #Kan sikkert heller bruke dir[0]/dir[1]

    #print(puck_dir.angle_degrees)
    calculate = False

    if -math.pi < angle < -math.pi/2:
        x = x - (y-top-puck_radius-wall_thickness)/k
        i = 0
        calculate = True

    elif math.pi/2 < angle <= math.pi:
        x = x - (y-bottom+puck_radius+wall_thickness)/k
        i = 1
        k = abs(k)
        calculate = True

    while calculate and x > left:

        if i%2 == 0:
            points.append((x,top + puck_radius+wall_thickness))
        else:
            points.append((x,bottom - puck_radius-wall_thickness))
        
        x = x - table_height/k


        i += 1


    if calculate:
        
        # Finne ut treff punk på robot sin side
        if i%2 == 0:
            y = points[-1][1] - (points[-1][0]-left-puck_radius-wall_thickness)*k
        
        else:
            y = points[-1][1] + (points[-1][0]-left- puck_radius-wall_thickness)*k

        
        points.append((left+puck_radius+wall_thickness,y))


 
    #print(points)
    return points