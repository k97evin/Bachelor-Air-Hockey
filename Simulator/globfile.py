import math
import pymunk
from pymunk import Vec2d
import pygame

# Screen size
width, height = 1200,600

center_y = height/2
center_x = width/2

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,127,80)
BLACK = (0,0,0)
CYAN = (0, 255,255)

# Table dimensions
scaling = 7
table_width = int(160*scaling)
table_height = int(70*scaling)
puck_radius = int(7/2*scaling)
pusher_radius = int(9.6/2*scaling)
goal_size = 30*scaling

# wall varaibles (They show the outside wall positions)
wall_thickness = 10

left = (width-table_width-2*wall_thickness)/2
right = width-left
top = (height-table_height-2*wall_thickness)/2
bottom = height-top




# Puck center reachable positions
puck_topPos = top + wall_thickness + puck_radius
puck_bottomPos = bottom - wall_thickness - puck_radius

# Pusher/bot center reachable positions
pusher_distFromWall = 10 #The closest the pusher can get to the wall
puck_leftPos = left + wall_thickness + pusher_distFromWall + pusher_radius #kanskje ligge til: + puck_radius




# puck start values
puck_start_pos = [1000,300]
puck_activated = False
puck_activated_pos = [0,0]

bot_start_pos = [100,100]