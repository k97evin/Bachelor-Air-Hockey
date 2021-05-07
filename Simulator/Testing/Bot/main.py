import pygame
import pymunk
import math
from pymunk import Vec2d
import datetime

import puck_path
from puck_velocity import velocity2
from Puck_path import puck_path2

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

vertical_wall_size = [wall_thickness, table_height+2*wall_thickness]
horisontal_wall_size = [table_width+2*wall_thickness, wall_thickness]


# puck start values
puck_start_pos = [1000,300]
puck_activated = False
puck_activated_pos = [0,0]

bot_start_pos = [100,100]

# Pygame and Pymunk setup
pygame.init()
display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.damping = 0.9
FPS = 90

# Draw text on display
font = pygame.font.SysFont('freesansbold.ttf', 32)
text = font.render('m/s: 0', True, CYAN)
textRect = text.get_rect()
textRect.center = (100, 16)

print("Top: ", top)
print("Bottom: ", bottom)
print("Center: ", 45+ (bottom-top)/2)


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
        bot.body.position = [100, 300]


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
    

class Wall():
    def __init__(self, pos,size):

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])

        

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = self.rect.center

        self.shape = pymunk.Poly.create_box(self.body,size)
        self.shape.elasticity = 0.95

        self.shape.density = 1

        self.shape.collision_type = 2

        space.add(self.body, self.shape)

    def draw(self):      
        pygame.draw.rect(display,WHITE,pygame.Rect(self.rect))




class Bot():
    def __init__(self):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = bot_start_pos
        self.shape = pymunk.Circle(self.body,pusher_radius)
        self.shape.elasticity = 0.7
        self.shape.mass = 3
        self.shape.friction = 0.5
        self.shape.collision_type = 3
        # [x_left, y_top, x_right, y_bottom]
        self.boundries = [left + wall_thickness + 100, top + wall_thickness + pusher_radius, center_x, bottom - wall_thickness - pusher_radius]
      

        space.add(self.body,self.shape)


    def draw(self):
        x, y = self.body.position

        pygame.draw.circle(display,RED,(int(x),int(y)),pusher_radius)

    def move(self, position, velocity):
        if self.body.position[1] <= self.boundries[1] and velocity[1] < 0:
            self.body.velocity = [0,0]
        
        elif self.body.position[1] >= self.boundries[3] and velocity[1] > 0:
            self.body.velocity = [0,0]

        else: self.body.velocity = velocity 

def draw_puck_path(points):

    #print("Tegn:", points)
    nr_points = len(points)

    if nr_points >= 2:
        for j in range(nr_points-1):
            pygame.draw.line(display, GREEN, points[j],points[j+1],8)



# Declear objects
puck = puck()
a = puck.body.position

wall_top = Wall([left,top],horisontal_wall_size)
wall_left = Wall([left,top],vertical_wall_size)
wall_right = Wall([right-wall_thickness,top],vertical_wall_size)
wall_bottom = Wall([left,bottom-wall_thickness],horisontal_wall_size)
#print(table_width+2*wall_thickness)


puck_pos = []
puck_pos_vel = []
last_puck_pos = puck.body.position
puck_dir = Vec2d.zero()
points = []


# Start simulator
running = True


i = 0
j = 0
k = 0

wall_hit = space.add_collision_handler(1,2)
wall_hit.begin = puck.printe
wall_hit.post_solve = puck.printe2

multiplier = 100000

start_angle = 70
start_angle = math.radians(90-start_angle)

start_angle = 15*math.pi/20
#force_vec = [- math.sin(start_angle)*multiplier,- math.cos(start_angle)*multiplier]
force_vec = [math.cos(start_angle)*multiplier,math.sin(start_angle)*multiplier]
puck.apply_force2(force_vec)

bot = Bot()
#bot.move([0,100])


#print(puck_pos_vel)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                p = pygame.mouse.get_pos()
                dist = puck.shape.point_query(p)
                if dist[2] < 0:
                    puck_activated = True
                    puck_activated_pos = puck.body.position
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and puck_activated:
                puck_activated = False
                p = pygame.mouse.get_pos()
                puck.apply_force(p)

    
    # Reset puck
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        puck.reset()


    # Draw
    display.fill(BLACK)

    bot.draw()

    draw_puck_path(points)

    puck.draw()

    wall_left.draw()
    wall_right.draw()
    wall_top.draw()
    wall_bottom.draw()

    display.blit(text, textRect)

    rect = pygame.Rect(left,center_y-105, 10, 210)
    pygame.draw.rect(display, RED, rect)

    pygame.display.update()

    # Step
    clock.tick(FPS)
    space.step(1/(FPS))


    # collect object in list
    t = datetime.datetime.now()
    puck_pos_vel.append([puck.body.position, t])

    i += 1
    j += 1
    k += 1

  

    if i >= 1:
        puck_pos = puck.body.position
       
        #puck_dir = puck_velocity.velocity(puck_pos,last_puck_pos,puck_dir)

        #last_puck_pos = puck_pos

        #points = puck_path.path(puck_dir,puck_pos)
        #points = puck_path2.path_points(puck_dir,puck_pos)

        bot_x = bot.body.position[0]
        bot_y = bot.body.position[1]
        #puck_Fx = points[-1][0]
        #puck_Fy = points[-1][1]

        if k > 4:
            puck_vel = velocity2(puck_pos_vel)

            points = puck_path.path(puck_vel, puck_pos)
            points = puck_path2.path_points(puck_vel, puck_pos)

            puck_Fx = points[-1][0]
            puck_Fy = points[-1][1]

            print(puck_vel[0])
            #print("points: " + str(points))
            #print("vec: " + str(puck_vel))
            #print(puck_pos_vel)
            puck_pos_vel.pop(0)

        if len(points) > 1:
            if bot.body.position != points[-1]:

                if abs(bot_y - puck_Fy) >= 3 and puck_vel[0] <= 0 : 
                    if bot_y < puck_Fy:
                        bot.move(bot.body.position, [0,500])
                
                    elif bot_y > puck_Fy:
                        bot.move(bot.body.position, [0,-500])

                    else: bot.move(bot.body.position, [0,0])

                else:
                        bot.move(bot.body.position, [0,0])


        else: 
            if bot_y < height/2:
                bot.move(bot.body.position, [0,500])

            elif bot_y > height/2:
                bot.move(bot.body.position, [0,-500])

            else: 
                bot.move(bot.body.position, [0,0])
        

        #print("Her: ", puck.body.velocity, " og ", puck_dir)
        #print("Her2: ",puck.body.velocity.angle_degrees, " og ", puck_dir.angle_degrees)
        #print(points)
        i = 0

    if j >= 20:
        text = font.render("v = " + str(round(puck.body.velocity.length/700,2)) + " m/s", True, CYAN)
        textRect = text.get_rect()
        textRect.center = (100, 16)
        j = 0
        


pygame.quit()