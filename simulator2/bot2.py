from globfile2 import *
from puck2 import velocity

bot_center_bounderies = [left + wall_thickness + 100, top + wall_thickness + pusher_radius, center_x, bottom - wall_thickness - pusher_radius]

class Bot():
    def __init__(self,space):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = bot_start_pos
        self.shape = pymunk.Circle(self.body,pusher_radius)
        self.shape.elasticity = 0.7
        self.shape.mass = 3
        self.shape.friction = 0.5
        self.shape.collision_type = 3
        # [x_left, y_top, x_right, y_bottom]
        self.boundries = [bottom + wall_thickness + 100, left + wall_thickness + pusher_radius, center_x, right - wall_thickness - pusher_radius]
      
        space.add(self.body,self.shape)

        self.maxSpeed = 500
        self.command  = "center"
        # Bot path: [points to move to, speeds for each line between points, which line the bot is on]
        self.path = [self.body.position,self.maxSpeed,0]
        self.previous_puck_vel = [0,0]
        self.previous_puck_end_pos = [0,0]

    def draw(self,display):
        x, y = self.body.position

        pygame.draw.circle(display,RED,(int(x),int(y)),pusher_radius)
    
    def reset(self):
        self.body.position = [100, 300]


    # ----------------------------- #
    # ------- BOT ALGORITHM ------- #
    # ----------------------------- #

    def move(self):

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

                threshhold = 5
                # Bot has reach next position within threshold
                if abs(bot_pos[0]-bot_target_pos[0]) < threshhold and abs(bot_pos[1]-bot_target_pos[1]) < threshhold:
                    line_num += 1

                if line_num >= len(path_points)-1:
                    line_num = -1 #at target position
                    self.body.velocity = [0,0]

                else:
                    vel_dir = bot_target_pos-bot_start_pos
                    vel_dir = Vec2d(vel_dir[0],vel_dir[1])
                    vel = vel_dir.normalized() *path_vel[line_num]
                    self.body.velocity = vel

                
                self.path[2] = line_num

            else: self.body.velocity = [0,0]
        
        else: self.body.velocity = [0,0]


    def CheckCommand(self,puck_last_velocity,puck_path_points,times):
        puck_vel = Vec2d(puck_last_velocity[0],puck_last_velocity[1])
        puck_vel_prev = self.previous_puck_vel
        puck_pos = puck_path_points[0]
        puck_end_pos = puck_path_points[-1]
        puck_pos_prev = self.previous_puck_end_pos
        command = self.command

        # if puck_vel[0] == 0 and puck_vel[1] == 0 and puck_pos[0] < center_x:
        #     self.command = "targeted_attack"
        #     attack_point = directed_hit_stillPuck(self.body.position,puck_pos,[1,0])
        #     bot_points = [self.body.position, attack_point]
        #     #bot_speed = self.maxSpeed
        #     bot_speed = 100
        #     self.path = [bot_points,[bot_speed],0]
        #     print(self.path)

        #kommentere ut
        # If the puck is headed away from bot and at player side: go to center
        if puck_vel[0] >= 0 and  puck_pos[0] > center_x:
            self.command = "center"
            #print("Center")

        # If the puck is starting to go towards the bot: calculate a new command
        elif command == "center":
            self.NewCommand(puck_path_points,times,puck_last_velocity)
            print("New commando")

        elif (command == "attack" or command == "defence" or command == "defence/attack") and len(puck_path_points) < 2:
            self.NewCommand(puck_path_points,times,puck_last_velocity)
            print("New command 2")
        
        elif (command == "targeted_attack") and len(puck_path_points) > 1:
            self.NewCommand(puck_path_points,times,puck_last_velocity)
            print("new commando 4")

        
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
            self.NewCommand(puck_path_points,times,puck_last_velocity)
            print("New Command 3")

        # Run the current command
        self.move()


    def UpdateCommand(self):
        pass

    def NewCommand(self,points,times,puck_last_velocity):
        
        bot_pos = Vec2d(self.body.position[0],self.body.position[1])
        puck_pos = Vec2d(points[0][0],points[0][1])
        
        # If a puck trajectory was calculated
        if len(points) > 1:
            
            puck_end_pos = Vec2d(points[-1][0],points[-1][1])
            puck_penult_pos = Vec2d(points[-2][0],points[-2][1])


            # Puck hits over or under goal:
            if abs(puck_end_pos[1]-center_y) > 15*7:
            #if abs(puck_end_pos[1]-center_y) > 30*7:
                self.command = "center"   #maybe change this later
            
            # Puck hits goal
            else:
                # Time for robot to reach puck end pos in goal at max speed
                tbot = abs(bot_pos[1]-puck_end_pos[1])/self.maxSpeed
                # Time for puck to reach the goal
                tpuck = times[-1]
                # Excess time for robot after blocking goal
                tdiff = tpuck - tbot
                
                bot_defence_point =  Vec2d(self.boundries[0],puck_end_pos[1])             

                # ------- DEFENCE ------- #

                # If the puck reaches the goal within 0.5s, Defence algoritm is chosen
                if tdiff < 1.5:
                    self.command = "defence"

                    #point = defenceReflectionPos(puck_pos,puck_last_velocity,[1,0])
                    point = defenceReflectionPos(points[-2],puck_last_velocity,[1,0])
                    print("point: ", point)
                    #bot_points = [self.body.position, bot_defence_point]
                    bot_points = [self.body.position,point]
                    bot_speed = self.maxSpeed
                    self.path = [bot_points,[bot_speed],0]


                # ------- ATTACK ------- #

                elif tdiff < 2.0:
                    
                    # Dont attack if the puck hits the wall too close to bot goal
                    if points[-2][0] < 300:
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
                        bot_speeds= [self.maxSpeed,attack_velocity.length]
                        self.path = [bot_points,bot_speeds,0]

                        print("Path: ", self.path)



                # ------- DEFENCE/ATTACK ------- #

                elif tdiff < 10.0:
                    self.command = "defence/attack"
                    bot_points = [self.body.position, bot_defence_point]
                    bot_speed = self.maxSpeed
                    self.path = [bot_points,[bot_speed],0]
                
                # If the puck takes too long to reach bot goal
                else:
                    self.command = "center"


                self.previous_puck_end_pos = puck_end_pos
                self.previous_puck_vel = puck_last_velocity


        # if puck Trajectory was not calculated
        else: 
            print("NICE")
            puck_vel = Vec2d(puck_last_velocity[0],puck_last_velocity[1])
            
            # if the puck is not moving too fast
            if(puck_vel.length < 5):
                if(puck_pos[0] < center_x):
                    self.command = "targeted_attack"

                    attack_point = directed_hit_stillPuck(bot_pos,puck_pos,[1,-1])
                    attack_point = hit_stillPuck_to_target_pos(bot_pos,puck_pos,[puck_topPos,center_y])
                    bot_points = [self.body.position, attack_point]
                    bot_speed = self.maxSpeed
                    self.path = [bot_points,[bot_speed],0]
                    



            else:
                self.command = "center"



# This function calculates where to position the bot in defence mode to deflect the puck to a chosen desired velocity
def defenceReflectionPos(puck_position,puck_velocity,puck_desired_velocity):
    puck_pos = Vec2d(puck_position[0],puck_position[1])
    puck_vel = Vec2d(puck_velocity[0],puck_velocity[1])
    puck_des_vel = Vec2d(puck_desired_velocity[0],puck_desired_velocity[1])

    # normal vector to the surface of the bot to reflect the ball to the desired direction:
    norm_vec = (puck_des_vel.normalized() - puck_vel.normalized()).normalized()

    # x position of the collision between bot and puck
    collision_pos_x = bot_center_bounderies[0] + norm_vec[0]*pusher_radius

    # time when the collison happends
    collision_time = (collision_pos_x-puck_position[0])/puck_vel[0]

    collision_pos_y = puck_pos[1]+puck_vel[1]*collision_time

    bot_pos = [bot_center_bounderies[0], collision_pos_y - norm_vec[1]*pusher_radius]
    return bot_pos



# function to 
def directed_hit_stillPuck(bot_position, puck_position, puck_desired_velocity):
    bot_pos = Vec2d(bot_position[0],bot_position[1])
    puck_pos = Vec2d(puck_position[0],puck_position[1])
    puck_des_vel = Vec2d(puck_desired_velocity[0],puck_desired_velocity[1])
    
    puck_des_vel_norm = puck_des_vel.normalized()

    # There are based of a desired puck velocity pointing towards player side
    bot_collision_point = bot_pos + puck_des_vel_norm*pusher_radius

    puck_collision_point = puck_pos - puck_des_vel_norm*puck_radius

    bot_movement = puck_collision_point - bot_collision_point
    bot_movement = bot_movement*1.2

    #bot_target_pos = puck_collision_point + (bot_pos - bot_collision_point)
    bot_target_pos = bot_movement + bot_pos # extending the path so the bot pushes through the puck and not just hit it

    return bot_target_pos

def hit_stillPuck_to_target_pos(bot_position, puck_position, puck_target_position):
    bot_pos = Vec2d(bot_position[0],bot_position[1])
    puck_pos = Vec2d(puck_position[0],puck_position[1])

    puck_target_pos = Vec2d(puck_target_position[0],puck_target_position[1])
    puck_target_vel = (puck_target_pos-puck_pos).normalized()
    
    bot_collision_point = bot_pos + puck_target_vel*pusher_radius
    puck_collision_point = puck_pos - puck_target_vel*puck_radius
    
    bot_movement = puck_collision_point - bot_collision_point
    bot_movement = bot_movement*1.2

    # global point
    bot_target_pos = bot_movement + bot_pos

    return bot_target_pos


def hit_stillPuck_to_target_pos2(bot_position, puck_position, puck_target_position):
    bot_pos = Vec2d(bot_position[0],bot_position[1])
    puck_pos = Vec2d(puck_position[0],puck_position[1])
    puck_target_pos = Vec2d(puck_target_position[0],puck_target_position[1])
    
    puck_target_vel = (puck_target_pos-puck_pos).normalized()
    
    bot_collision_point = bot_pos + puck_target_vel*pusher_radius
    puck_collision_point = puck_pos - puck_target_vel*puck_radius
    
    bot_movement = puck_collision_point - bot_collision_point
    bot_movement = bot_movement*1.2

    # global point
    bot_target_pos = bot_movement + bot_pos

    return bot_target_pos

    


    


# This function calculates which position the bot should move to to hit a moving puck
# NB: The bot_speed is not a velocity, just a speed
def CollisionPos2(bot_pos,bot_speed, puck_pos,puck_velocity):
    bx = bot_pos[0]
    bx2 = bx**2
    by = bot_pos[1]
    by2 = by**2
    bS = bot_speed
    bS2 = bot_speed**2

    px = puck_pos[0]
    px2 = px**2
    py = puck_pos[1]
    py2 = py**2
    pVx = puck_velocity[0]
    pVx2 = pVx**2
    pVy = puck_velocity[1]
    pVy2 = pVy**2


    time = -1
    collisionPos = [0,0]
    

    # Calculating the time of impact:
    under_sqrt = bx2*bS2 - bx2*pVy2 - 2*bx*px*bS2 + 2*bx*px*pVy2 + 2*bx*by*pVx*pVy - 2*bx*py*pVx*pVy + px2*bS2 - px2*pVy2 - 2*px*by*pVx*pVy + 2*px*py*pVx*pVy + by2*bS2 - by2*pVx2 - 2*by*py*bS2 + 2*by*py*pVx2 + py2*bS2 - py2*pVx2
    denominator = pVx2 + pVy2 - bS2
    print(under_sqrt)
    
    if under_sqrt >= 0 and denominator != 0:
        time = - (px*pVx - bx*pVx - by*pVy + py*pVy + math.sqrt(under_sqrt)) / denominator

        collisionPos[0] = px + pVx*time
        collisionPos[1] = py + pVy*time

    return time, collisionPos


    






