import cv2
import numpy as np
import numpy as np
import cv2.aruco as aruco
from threading import Thread, Lock
from datetime import datetime
from pymunk import Vec2d
import time

#  all units are in mm
#  left, right, top, bottom are relative to the robots perspective 
# height and width are relative to the cameras perspective 

# --- TABLE --- #
table_width = 1600.0
table_height = 700.0
table_center_x = table_width/2
table_center_y = table_height/2
camera_height = 1055.0

goal_size = 300.0


# --- PUCK --- #
puck_radius = 69.2/2

# maximum position values for the puck
puck_leftPos = puck_radius
puck_rightPos = table_height - puck_radius
puck_topPos = table_height - puck_radius
puck_bottomPos = puck_radius


# --- ROBOT/PUSHER --- #
pusher_radius = 95.0/2
pusher_height = 95

# maximum position values for the pusher
pusher_leftPos = 65.0
pusher_rightPos = table_height - 65.0
pusher_bottomPos = 70.0
pusher_topPos = 620.0
