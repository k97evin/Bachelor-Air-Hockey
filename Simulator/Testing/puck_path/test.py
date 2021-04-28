import puck_path2
from pymunk import Vec2d

point = [1000,300]
velocity = Vec2d(-10,-10)

print(puck_path2.path_points(velocity,point))

