from globfile import *

class puck():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = puck_start_pos
        self.shape = pymunk.Circle(self.body,puck_radius)
        self.shape.density = 1
        self.shape.elasticity = 0.90
        self.shape.mass = 2
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        
        space.add(self.body,self.shape)

    def draw(self):
        global puck_activated, puck_activated_pos
        x, y = self.body.position
        pygame.draw.circle(display,ORANGE,(int(x),int(y)),puck_radius)

        if puck_activated:
            pygame.draw.circle(display,GREEN,(int(x),int(y)),puck_radius,3)
            pygame.draw.line(display,GREEN,pygame.mouse.get_pos(), puck_activated_pos,3)

    def apply_force(self, mouse_pos):
        force = 1000*(mouse_pos-self.body.position).rotated(-self.body.angle)
        self.body.apply_force_at_local_point(force)
    
    def apply_force2(self, force_vec):
        self.body.apply_force_at_local_point(force_vec)

    def reset(self):
        self.body.position = puck_start_pos
        self.body.velocity = 0,0


    def printe(self,space, arbiter, data):
        vel = self.body.velocity
        pos = self.body.position
        ang = self.body.velocity.angle

        #ang = math.pi - abs(ang)
        
        print("puck: POS: ",pos, " VEL: ",vel," ANG: ", abs(ang))

        return True
    
    def printe2(self,space, arbiter, data):
        vel = self.body.velocity
        pos = self.body.position
        ang = self.body.velocity.angle

        #ang = math.pi - abs(ang)
        
        print("puck2: POS: ",pos, " VEL: ",vel," ANG: ", abs(ang))

        return True



# ------- PUCK VELOCITY ------- #
# Puck velocity is calculated based of the last few points 
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


# ------- ESTIMATED BOUNCE ANGLE ------- #
import joblib
from pathlib import Path
path =  Path(__file__).parent
model = joblib.load(path/'puck_path'/'model.joblib')
def rotate_vel(velocity):
    angle_inn = velocity.angle
    angle_out = model.predict([[abs(angle_inn)]])[0][0]

    rotated_velocity = velocity
    if angle_inn < 0:
        rotated_velocity = velocity.rotated(-angle_inn+angle_out)

    if angle_inn > 0:
        rotated_velocity = velocity.rotated(-angle_inn-angle_out)

    return rotated_velocity


# ------- ESTIMATED PUCK PATH POINTS ------- #
# This function calculates an estimation of where the puck will hit the walls
# and end up. It returns all of the collision points with the walls.
def path_points(puck_velocity,puck_pos):

    P = puck_pos
    last_velocity = puck_velocity
    totalTime = 0
    t = 0
    points = []
    calculate = False
    while puck_velocity[0] < 0 and puck_pos[0] > puck_leftPos:
        points.append(puck_pos)
        totalTime += t
        if puck_velocity[0] < 0 and puck_velocity[1] < 0:
            t = (puck_topPos - puck_pos[1])/puck_velocity[1]
            Px = puck_pos[0] + puck_velocity[0]*t

            puck_pos  = [Px,puck_topPos]
            last_velocity = puck_velocity
            puck_velocity = rotate_vel(puck_velocity)
            calculate = True

        elif puck_velocity[0] <= 0 and puck_velocity[1] > 0:
            t = (puck_bottomPos - puck_pos[1])/puck_velocity[1]
            Px = puck_pos[0] + puck_velocity[0]*t

            puck_pos = [Px,puck_bottomPos]
            last_velocity = puck_velocity
            puck_velocity = rotate_vel(puck_velocity)
            calculate = True

    if calculate:
        t = (puck_leftPos-points[-1][0])/last_velocity[0]
        totalTime += t

        Py = points[-1][1]+last_velocity[1]*t
        
        puck_pos = [puck_leftPos,Py]
        points.append(puck_pos)
    
    else:
        points.append(puck_pos)

    #print(points)
    return points


# ------- DRAWING PUCK PATH ------- #
def draw_path(points):
    nr_points = len(points)

    if nr_points >= 2:
        for j in range(nr_points-1):
            pygame.draw.line(display, GREEN, points[j],points[j+1],8)