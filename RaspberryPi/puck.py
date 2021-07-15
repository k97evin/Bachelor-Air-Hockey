from globfile import *

def velocity(puck_pos):
    
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


def rotate_vel(velocity):
    angle_inn = velocity.angle
    angle_out = angle_inn

    rotated_velocity = velocity
    if angle_inn < 0:
        rotated_velocity = velocity.rotated(-angle_inn+angle_out)

    if angle_inn > 0:
        rotated_velocity = velocity.rotated(-angle_inn-angle_out)

    return rotated_velocity

def path_points2(puck_velocity,puck_position):

    puck_pos = puck_position
    last_velocity = puck_velocity
    totalTime = 0
    t = 0
    points = []
    times = []
    calculate = False

    # Variable to break out of while loop if it gets stuck
    i = 0

    #puck_vel_vec = Vec2d(puck_velocity[0],puck_velocity[1])

    # The threshold is to not calculate puck path if the puck is moving slow in negative x-direction
    puck_vel_threshold = -5

    while puck_velocity[0] < puck_vel_threshold and puck_pos[0] > pusher_bottomPos:
        i += 1
        totalTime += t
        points.append(puck_pos)
        times.append(totalTime)
        if puck_velocity[0] < 0 and puck_velocity[1] < 0:
            t = (puck_leftPos - puck_pos[1])/puck_velocity[1]
            Px = puck_pos[0] + puck_velocity[0]*t

            puck_pos  = [Px,puck_leftPos]
            last_velocity = puck_velocity
            puck_velocity = rotate_vel(puck_velocity)
            calculate = True

        elif puck_velocity[0] < 0 and puck_velocity[1] > 0:
            t = (puck_rightPos - puck_pos[1])/puck_velocity[1]
            Px = puck_pos[0] + puck_velocity[0]*t

            puck_pos = [Px,puck_rightPos]
            last_velocity = puck_velocity
            puck_velocity = rotate_vel(puck_velocity)
            calculate = True

        if i > 50:
            calculate = False
            times = []
            break

    if calculate:
        t = (pusher_bottomPos-points[-1][0])/last_velocity[0]
        totalTime += t

        Py = points[-1][1]+last_velocity[1]*t
        
        puck_pos = [pusher_bottomPos,Py]
        points.append(puck_pos)
        times.append(totalTime)
    
    else:
        points = [puck_position]
        times = [0]

 
    #print(points)
    return points, times, last_velocity