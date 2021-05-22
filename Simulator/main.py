from globfile import *
import datetime
import bot
import puck


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



# Declear objects
Puck = puck.Puck(space)
Bot = bot.Bot(space)

vertical_wall_size = [wall_thickness, table_height+2*wall_thickness]
horisontal_wall_size = [table_width+2*wall_thickness, wall_thickness]

wall_top = Wall([left,top],horisontal_wall_size)
wall_left = Wall([left,top],vertical_wall_size)
wall_right = Wall([right-wall_thickness,top],vertical_wall_size)
wall_bottom = Wall([left,bottom-wall_thickness],horisontal_wall_size)

#Start variables
puck_pos = []
puck_pos_vel = []
last_puck_pos = Puck.body.position
puck_dir = Vec2d.zero()
points = []


i = 1
j = 0
k = 0

# Collison 
wall_hit = space.add_collision_handler(1,2)
wall_hit.begin = Puck.printe
wall_hit.post_solve = Puck.printe2


# Puck start force
multiplier = 100000
start_angle = 70
start_angle = math.radians(90-start_angle)
start_angle = 15*math.pi/20
#force_vec = [- math.sin(start_angle)*multiplier,- math.cos(start_angle)*multiplier]
force_vec = [math.cos(start_angle)*multiplier,math.sin(start_angle)*multiplier]
Puck.apply_force2(force_vec)

#print(puck_pos_vel)


# ------- START SIMULATOR ------- #
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                p = pygame.mouse.get_pos()
                dist = Puck.shape.point_query(p)
                if dist[2] < 0:
                    puck_activated = True
                    puck_activated_pos = Puck.body.position
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and puck_activated:
                puck_activated = False
                p = pygame.mouse.get_pos()
                Puck.apply_force(p)

    

    keys = pygame.key.get_pressed()

    # Reset puck position
    if keys[pygame.K_r]:
        Puck.reset()
    
    # Reset bot poistion
    if keys[pygame.K_t]:
        Bot.reset()

    # Draw
    display.fill(BLACK)

    puck.draw_path(points,display)

    Bot.draw(display)
    Puck.draw(display,puck_activated,puck_activated_pos)

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
    puck_pos_vel.append([Puck.body.position, t])


    j += 1
    k += 1

    # Dont calculate before enough points are added
    if k>4:
        i += 1

        # How often puck path and bot command should be updated
        if i>=1:
            puck_vel = puck.velocity(puck_pos_vel)
            puck_pos = Puck.body.position
            print("puck_vel: ", puck_vel)
            print("puck_pos: ", puck_pos)
            points, times, last_velocity = puck.path_points(puck_vel,puck_pos)
            Bot.CheckCommand(last_velocity,points,times)
            puck_pos_vel.pop(0) 
            i = 0

    if j >= 20:
        text = font.render("v = " + str(round(Puck.body.velocity.length/700,2)) + " m/s", True, CYAN)
        textRect = text.get_rect()
        textRect.center = (100, 16)

        text2 = font.render("Attack mode: " + Bot.command, True, CYAN)
        textRect2 = text2.get_rect()
        textRect2.center = (500, 16)
        j = 0

pygame.quit()