import pygame
import pymunk
import math
from pymunk import Vec2d

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
        if self.body.position[1] <= self.boundries[1] or self.body.position[1] >= self.boundries[3]:
            self.body.velocity = [0,0]

        else: self.body.velocity = velocity 

    def moveStepper(self,DeltaTheta1, DeltaTheta2, maxSpeedTheta1, maxSpeedTheta2):
        pass




# Stepper
steps_per_round = 400
stepper_radius = int(2.5*7)

def runStepperRelative(DeltaX,DeltaY,SpeedX,SpeedY):
    DeltaTheta1 = -1/stepper_radius*DeltaY+1/stepper_radius*DeltaX
    DeltaTheta2 = -1/stepper_radius*DeltaY-1/stepper_radius*DeltaX

    maxSpeedTheta1 = -1/stepper_radius*SpeedY+1/stepper_radius*SpeedX
    maxSpeedTheta2 = -1/stepper_radius*SpeedY-1/stepper_radius*SpeedX

    return DeltaTheta1, DeltaTheta2, maxSpeedTheta1, maxSpeedTheta2


def runStepperAbsolute(X,Y):
    pass


def AccelStep_move(DeltaTheta1,DeltaTheta2):
    pass











# Declear objects

wall_top = Wall([left,top],horisontal_wall_size)
wall_left = Wall([left,top],vertical_wall_size)
wall_right = Wall([right-wall_thickness,top],vertical_wall_size)
wall_bottom = Wall([left,bottom-wall_thickness],horisontal_wall_size)
#print(table_width+2*wall_thickness)




# Start simulator
running = True


i = 0
j = 0





bot = Bot()
#bot.move([0,100])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    
    # Reset puck
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        pass


    # Draw
    display.fill(BLACK)

    bot.draw()


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

    i += 1
    j += 1

    if i >= 1:
        

        bot_x = bot.body.position[0]
        bot_y = bot.body.position[1]

        

        #print("Her: ", puck.body.velocity, " og ", puck_dir)
        #print("Her2: ",puck.body.velocity.angle_degrees, " og ", puck_dir.angle_degrees)
        #print(points)
        i = 0

    if j >= 20:
        text = font.render("Pos: " , True, CYAN)
        textRect = text.get_rect()
        textRect.center = (100, 16)
        j = 0
        


pygame.quit()