import pygame
import pymunk
import math
from pymunk import Vec2d

# Screen size
width, height = 1200,600

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,127,80)
BLACK = (0,0,0)

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