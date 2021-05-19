import pygame
import pymunk
import math
from pymunk import Vec2d
from pymunk import body

import puck_path
import puck_velocity
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

text2 = font.render('Attack mode: ' + "None", True, CYAN)
textRect2 = text2.get_rect()
textRect2.center = (500, 16)

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

        self.maxSpeed = 1000
        self.command  = "center"
        # Bot path: [points to move to, speeds for each line between points, which line the bot is on]
        self.path = [self.body.position,self.maxSpeed,0]
        self.previous_puck_vel = 0
        self.previous_puck_end_pos = [0,0]

    def draw(self):
        x, y = self.body.position

        pygame.draw.circle(display,RED,(int(x),int(y)),pusher_radius)
    
    def reset(self):
        self.body.position = [100, 300]

    def move(self, position, velocity):
        if self.body.position[1] <= self.boundries[1] or self.body.position[1] >= self.boundries[3]:
            self.body.velocity = [0,0]

        else: self.body.velocity = velocity 
    
    def move2(self):
        bot_pos = self.body.position
        vel = self.body.velocity
        
        if self.command == "center":
            threshold = 7
            if bot_pos[1] - center_y > threshold:
                vel = [0,-500]
            elif bot_pos[1] - center_y < threshold:
                vel = [0,500]
            else: 
                vel = [0,0]
        
        elif self.command == "defence":
            pass

    def move3(self):

        bot_pos = self.body.position

        if self.command == "center":
            middle_pos = [self.boundries[0],center_y]
            self.path = [[bot_pos,middle_pos],[self.maxSpeed],0]

        
        path_points = self.path[0]

        if len(path_points) > 1:
            path_vel = self.path[1]
            line_num = self.path[2]

            if line_num != -1: #not at end position
                bot_start_pos = path_points[line_num]
                bot_target_pos = path_points[line_num+1]

                threshhold = 7
                # Bot has reach next position within threshold
                if abs(bot_pos[0]-bot_target_pos[0]) < threshhold and abs(bot_pos[1]-bot_target_pos[1]) < threshhold:
                    line_num += 1
                    print("Reached Next position: ", line_num)

                if line_num >= len(path_points)-1:
                    print("Line num before: ",line_num)
                    line_num = -1 #at target position
                    self.body.velocity = [0,0]
                    print("At end position: ", line_num)

                else:
                    vel_dir = bot_target_pos-bot_start_pos
                    vel_dir = Vec2d(vel_dir[0],vel_dir[1])
                    #print("Se her: ", self.path)
                    #print("Se her2: ", line_num)
                    vel = vel_dir.normalized() *path_vel[line_num]
                    self.body.velocity = vel

                
                self.path[2] = line_num

            else: self.body.velocity = [0,0]
        
        else: self.body.velocity = [0,0]

    def algorithm2(self):
        pass

    def CheckCommand(self,puck_last_velocity,points,times):
        puck_vel = puck_last_velocity
        puck_vel_prev = self.previous_puck_vel
        puck_end_pos = points[-1]
        puck_pos_prev = self.previous_puck_end_pos

        # If the puck is headed away from bot: go to center
        if puck_vel[0] >= 0:
            self.command = "center"
            print("Center")
        
        # If the puck is starting to go towards the bot: calculate a new command
        elif self.command == "center" and puck_vel[0] < 0:
            self.NewCommand(points,times,puck_last_velocity)
            print("New commando")

        # If there is only a small change in puck velocity or puck end y-position: use same command
        elif abs(puck_vel[0]-puck_vel_prev[0]) < 1 or abs(puck_vel[1]-puck_vel_prev[1]) < 1 or abs(puck_end_pos[1]-puck_pos_prev[1]) < 1:
            print("Samme kommando")
            #pass #Run the same command
        
        # If there has been small change to puck velocity or puck end y-position: update the command to adjust
        elif abs(puck_vel[0]-puck_vel_prev[0]) < 15 or abs(puck_vel[1]-puck_vel_prev[1]) < 15 or abs(puck_end_pos[1]-puck_pos_prev[1]) < 50:
            self.UpdateCommand()
            print("Update command")

        # If the puck velocity or puck end pos has changed alot: calculate a new command
        else:
            self.NewCommand(points,times,puck_last_velocity)
            print("New Command 2")


        # Run the current command
        self.move3()



    def UpdateCommand(self):
        pass

    def NewCommand(self,points,times,puck_last_velocity):
        
        # If a puck trajectory was calculated
        if len(points) > 1:
            bot_pos = Vec2d(self.body.position[0],self.body.position[1])
            puck_end_pos = Vec2d(points[-1][0],points[-1][1])
            puck_penult_pos = Vec2d(points[-2][0],points[-2][1])


            # Puck hits over or under goal:
            if abs(puck_end_pos[1]-center_y) > 35*7:
                self.command = "center"   #maybe change this later
            
            # Puck hits goal
            else:
                # Time for robot to reach puck end pos in goal at max speed
                #tbot = abs(bot_pos[1]-puck_end_pos[1])/self.maxSpeed
                tbot = (bot_pos - puck_end_pos).length/self.maxSpeed 

                # Time for puck to reach the goal
                tpuck = times[-1]

                # Excess time for robot after blocking goal
                tdiff = tpuck - tbot
                
                bot_defence_point =  Vec2d(self.boundries[0],puck_end_pos[1])
                
                print("her: ", tdiff)

                # ------ DEFENCE ------ #

                # If the puck reaches the goal within 0.5s, Defence algoritm is chosen
                if tdiff < 0.5:
                    self.command = "defence"
                    bot_points = [self.body.position, bot_defence_point]
                    bot_speed = self.maxSpeed
                    self.path = [bot_points,[bot_speed],0]


                # ------ ATTACK ------ #

                elif tdiff < 2.0:
                    
                    print("Jaaa: ", points)
                    # Dont attack if the puck hits the wall too close to bot goal
                    if points[-2][0] < 300:
                        print("punkter: ", points)
                        #max_x_attack = 500
                        self.command = "defence"
                        bot_points = [self.body.position, bot_defence_point]
                        bot_speed = self.maxSpeed
                        self.path = [bot_points,[bot_speed],0]

                    else:
                        # Chosing the bot to attack the puck in the middle of the last puck path
                        puck_middle_pos = (puck_end_pos+puck_penult_pos)/2
                        #puck_middle_pos = [(points[-1][0]+points[-2][0])/2, (points[-1][1]+points[-2][1])/2]
                        
                        # Puck time to reach middle pos (only checking x-direction)
                        tmiddle = (puck_middle_pos[0]-points[-2][0]) / puck_last_velocity[0]  + times[-2]

                        # The time the bot has to reach puck_middle_pos from defence point
                        tmiddle_bot = tmiddle-tbot

                        attack_velocity = (puck_middle_pos-puck_end_pos)/tmiddle_bot
                        #attack_velocity = [(puck_middle_pos[0]-puck_end_pos[0])/tmiddle_bot, (puck_middle_pos[1]-puck_end_pos[1])/tmiddle_bot]


                        self.command = "attack"
                        bot_points = [self.body.position, bot_defence_point, puck_middle_pos]
                        bot_speeds = [self.maxSpeed,attack_velocity.length]
                        self.path = [bot_points,bot_speeds,0]

                        print("Path: ", self.path)



                # ------ DEFENCE/ATTACK ------ #

                elif tdiff < 3.0:

                    if points[0][0] > center_x - 100:
                        self.command = "defence/attack"
                        bot_points = [self.body.position, bot_defence_point]
                        bot_speed = self.maxSpeed
                        self.path = [bot_points,[bot_speed],0]
                        
                    else: 
                        self.command = "defence/attack"
                        
                        t_puck = (points[-1] - points[0])/puck_last_velocity[0]
                        

                        bot_points = [self.body.position, bot_defence_point, ] 

                
                # If the puck takes too long to reach bot goal
                else:
                    self.command = "center"


                self.previous_puck_end_pos = puck_end_pos
                self.previous_puck_vel = puck_last_velocity

        # Puck Trajectory was not calculated, go to center
        else: self.command = "center"


    def algorithm(self,points,times,last_velocity):

        if len(points) > 1:
            bot_pos = self.body.position
            puck_end_pos = points[-1]


            # If the puck is going to hit the goal
            if abs(puck_end_pos[1]-center_y) < 15*7:

                # Time for robot to block the goal 
                tbot = abs(bot_pos[1]-puck_end_pos[1])/self.maxSpeed

                # Time for puck to reach the goal
                tpuck = times[-1]

                tdiff = tpuck - tbot

                if tdiff < 0.5:
                    # Defence algorithm, maxspeed

                    bot_x = self.body.position[0]
                    bot_y = self.body.position[1]
                    puck_Fx = points[-1][0]
                    puck_Fy = points[-1][1]

                    if self.body.position != points[-1] :

                        if abs(bot_y - puck_Fy) >= 5: 
                            if bot_y < puck_Fy:
                                self.move(self.body.position, [0,500])
                        
                            elif bot_y > puck_Fy:
                                self.move(self.body.position, [0,-500])

                            else: self.move(self.body.position, [0,0])

                        else: self.move(self.body.position, [0,0])

                    return "Defence"

                elif tdiff < 2:
                    # Attack algorithm, maxspeed

                    return "Attack"

                elif tdiff < 10:
                    # Attack algorithm, variable speed
                    return "Defence/Attack"
        else: self.move(bot.body.position, [0,0])
        
        return "None"



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

multiplier = 80000

start_angle = 70
start_angle = math.radians(90-start_angle)

start_angle = -19.5*math.pi/20
#force_vec = [- math.sin(start_angle)*multiplier,- math.cos(start_angle)*multiplier]
#force_vec = [math.cos(start_angle)*multiplier,math.sin(start_angle)*multiplier]
#puck.apply_force2(force_vec)

bot = Bot()
#bot.move([0,100])


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

    if keys[pygame.K_t]:
        bot.reset()


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
    display.blit(text2, textRect2)

    rect = pygame.Rect(left,center_y-105, 10, 210)
    pygame.draw.rect(display, RED, rect)

    pygame.display.update()

    # Step
    clock.tick(FPS)
    space.step(1/(FPS))

    i += 1
    j += 1

    if i >= 1:
        puck_pos = puck.body.position

        puck_dir = puck_velocity.velocity(puck_pos,last_puck_pos,puck_dir)
        puck_dir = puck_dir/(1/FPS)
        last_puck_pos = puck_pos


        points = puck_path.path(puck_dir,puck_pos)
        #last_last_velocity = last_velocity
        points, times, last_velocity = puck_path2.path_points(puck_dir,puck_pos)
        #print(times)


        
        
        bot.CheckCommand(last_velocity,points,times)

        #attackMode = bot.algorithm(points,times,last_velocity)

        

        #print("Her: ", puck.body.velocity, " og ", puck_dir)
        #print("Her2: ",puck.body.velocity.angle_degrees, " og ", puck_dir.angle_degrees)
        #print(points)
        i = 0

    if j >= 20:
        text = font.render("v = " + str(round(puck.body.velocity.length/700,2)) + " m/s", True, CYAN)
        textRect = text.get_rect()
        textRect.center = (100, 16)


        text2 = font.render("Attack mode: " + bot.command, True, CYAN)
        textRect2 = text2.get_rect()
        textRect2.center = (500, 16)
        j = 0
        


pygame.quit()