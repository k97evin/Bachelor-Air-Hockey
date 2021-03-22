import pygame
import pymunk
import math

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


# ball start values
ball_start_pos = [800,300]
ball_activated = False
ball_activated_pos = [0,0]


# Pygame and Pymunk setup
pygame.init()
display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.damping = 0.9
FPS = 100



class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = ball_start_pos
        self.shape = pymunk.Circle(self.body,puck_radius)
        self.shape.density = 1
        self.shape.elasticity = 0.90
        self.shape.mass = 2
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        
        space.add(self.body,self.shape)

    def draw(self):
        global ball_activated, ball_activated_pos
        x, y = self.body.position
        pygame.draw.circle(display,ORANGE,(int(x),int(y)),puck_radius)

        if ball_activated:
            pygame.draw.circle(display,GREEN,(int(x),int(y)),puck_radius,3)
            pygame.draw.line(display,GREEN,pygame.mouse.get_pos(), ball_activated_pos,3)

    def apply_force(self, mouse_pos):
        force = 1000*(mouse_pos-self.body.position).rotated(-self.body.angle)
        self.body.apply_force_at_local_point(force)

    def reset(self):
        self.body.position = ball_start_pos
        self.body.velocity = 0,0


class Wall():
    def __init__(self, pos,size):

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = self.rect.center

        self.shape = pymunk.Poly.create_box(self.body,size)
        self.shape.elasticity = 0.95

        self.shape.density = 1

        space.add(self.body, self.shape)

    def draw(self):      
        pygame.draw.rect(display,WHITE,pygame.Rect(self.rect))


# Declear objects
ball = Ball()


wall_top = Wall([left,top],horisontal_wall_size)
wall_left = Wall([left,top],vertical_wall_size)
wall_right = Wall([right-wall_thickness,top],vertical_wall_size)
wall_bottom = Wall([left,bottom-wall_thickness],horisontal_wall_size)
print(table_width+2*wall_thickness)

# Start simulator
running = True


i = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                p = pygame.mouse.get_pos()
                dist = ball.shape.point_query(p)
                if dist[2] < 0:
                    ball_activated = True
                    ball_activated_pos = ball.body.position
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and ball_activated:
                ball_activated = False
                p = pygame.mouse.get_pos()
                ball.apply_force(p)

    
    # Reset ball
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        ball.reset()


    # Draw
    display.fill(BLACK)

    ball.draw()

    wall_left.draw()
    wall_right.draw()
    wall_top.draw()
    wall_bottom.draw()

    pygame.display.update()

    # Step
    clock.tick(FPS)
    space.step(1/(FPS))

    i += 1

    if i == 100:
        #print(ball.body.velocity.length/700)
        #print(clock.get_time)
        #print(space.current_time_step)
        #print(math.sqrt(ball.body.velocity[0]**2 + ball.body.velocity[1]**2))
        i = 0


pygame.quit()