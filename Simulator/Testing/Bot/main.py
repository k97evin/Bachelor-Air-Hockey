import pygame
import pymunk
import math
from pymunk import Vec2d

import puck_path
import puck_velocity


# Screen size
width, height = 1200,600


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
puck_start_pos = [1000,200]
puck_activated = False
puck_activated_pos = [0,0]

bot_start_pos = [100,100]

# Pygame and Pymunk setup
pygame.init()
display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.damping = 0.9
FPS = 100

# Draw text on display
font = pygame.font.SysFont('freesansbold.ttf', 32)
text = font.render('m/s: 0', True, CYAN)
textRect = text.get_rect()
textRect.center = (100, 16)



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
      

        space.add(self.body,self.shape)


    def draw(self):
        x, y = self.body.position

        pygame.draw.circle(display,RED,(int(x),int(y)),pusher_radius)

    def move(self, mouseX, mouseY):
        pass



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
last_puck_pos = puck.body.position
puck_dir = Vec2d.zero()
points = []


# Start simulator
running = True


i = 0
j = 0

wall_hit = space.add_collision_handler(1,2)
wall_hit.begin = puck.printe
wall_hit.post_solve = puck.printe2

multiplier = 100000

start_angle = 70
start_angle = math.radians(90-start_angle)

start_angle = -19*math.pi/20
#force_vec = [- math.sin(start_angle)*multiplier,- math.cos(start_angle)*multiplier]
force_vec = [math.cos(start_angle)*multiplier,math.sin(start_angle)*multiplier]
puck.apply_force2(force_vec)

bot = Bot()


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

    pygame.display.update()

    # Step
    clock.tick(FPS)
    space.step(1/(FPS))

    i += 1
    j += 1

    if i >= 1:
        puck_pos = puck.body.position

        puck_dir = puck_velocity.velocity(puck_pos,last_puck_pos,puck_dir)

        last_puck_pos = puck_pos


        points = puck_path.path(puck_dir,puck_pos)

        

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