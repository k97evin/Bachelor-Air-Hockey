import math


# Maybe add puck velocity to check if the ball will collide in the next frame
# Maybe calculate reflection angle both directions

# Table dimensions
scaling = 7
table_width = int(160*scaling)
table_height = int(70*scaling)
puck_radius = int(7/2*scaling)
pusher_radius = int(9.6/2*scaling)
goal_size = 30*scaling



wall_thickness = 10

left = (width-table_width-2*wall_thickness)/2
right = width-left
top = (height-table_height-2*wall_thickness)/2
bottom = height-top

distance_from_wall = 10


direction = -1  # 0 is up, 1 is down

def estimate_angle(puck_pos, puck_angle):   

    if -math.pi < puck_angle < -math.pi/2 and direction != 0:
        if puck_pos[1] < top + wall_thickness + puck_radius + distance_from_wall:
            
        
    elif math.pi/2 < puck_angle <= math.pi:


