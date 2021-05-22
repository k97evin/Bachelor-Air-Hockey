from globfile import *
import datetime
import bot
import puck

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
puck = puck()
a = puck.body.position

bot = bot.Bot()


vertical_wall_size = [wall_thickness, table_height+2*wall_thickness]
horisontal_wall_size = [table_width+2*wall_thickness, wall_thickness]

wall_top = Wall([left,top],horisontal_wall_size)
wall_left = Wall([left,top],vertical_wall_size)
wall_right = Wall([right-wall_thickness,top],vertical_wall_size)
wall_bottom = Wall([left,bottom-wall_thickness],horisontal_wall_size)

#Start variables
puck_pos = []
puck_pos_vel = []
last_puck_pos = puck.body.position
puck_dir = Vec2d.zero()
points = []





i = 0
j = 0
k = 0

wall_hit = space.add_collision_handler(1,2)
wall_hit.begin = puck.printe
wall_hit.post_solve = puck.printe2


# Puck start force
multiplier = 100000
start_angle = 70
start_angle = math.radians(90-start_angle)
start_angle = 15*math.pi/20
#force_vec = [- math.sin(start_angle)*multiplier,- math.cos(start_angle)*multiplier]
force_vec = [math.cos(start_angle)*multiplier,math.sin(start_angle)*multiplier]
puck.apply_force2(force_vec)

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
                dist = puck.shape.point_query(p)
                if dist[2] < 0:
                    puck_activated = True
                    puck_activated_pos = puck.body.position
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and puck_activated:
                puck_activated = False
                p = pygame.mouse.get_pos()
                puck.apply_force(p)

    

    keys = pygame.key.get_pressed()

    # Reset puck position
    if keys[pygame.K_r]:
        puck.reset()
    
    # Reset bot poistion
    if keys[pygame.K_t]:
        bot.reset()


    # Draw
    display.fill(BLACK)

    bot.draw()
    puck.draw_puck_path(points)
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

            #print(puck_vel[0])
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