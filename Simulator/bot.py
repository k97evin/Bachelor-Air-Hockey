from globfile import *


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

        self.maxSpeed = 500
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


    def CheckCommand(self,puck_last_velocity,points,times):
        puck_vel = puck_last_velocity
        puck_vel_prev = self.previous_puck_vel
        puck_end_pos = points[-1]
        puck_pos_prev = self.previous_puck_end_pos

        # If the puck is headed away from bot: go to center
        if puck_vel[0] >= 0:
            self.command = "center"
            #print("Center")
        
        # If the puck is starting to go towards the bot: calculate a new command
        elif self.command == "center" and puck_vel[0] < 0:
            self.NewCommand(points,times,puck_last_velocity)
            #print("New commando")

        # If there is only a small change in puck velocity or puck end y-position: use same command
        elif abs(puck_vel[0]-puck_vel_prev[0]) < 1 or abs(puck_vel[1]-puck_vel_prev[1]) < 1 or abs(puck_end_pos[1]-puck_pos_prev[1]) < 1:
            #print("Samme kommando")
            pass #Run the same command
        
        # If there has been small change to puck velocity or puck end y-position: update the command to adjust
        elif abs(puck_vel[0]-puck_vel_prev[0]) < 15 or abs(puck_vel[1]-puck_vel_prev[1]) < 15 or abs(puck_end_pos[1]-puck_pos_prev[1]) < 50:
            self.UpdateCommand()
            #print("Update command")

        # If the puck velocity or puck end pos has changed alot: calculate a new command
        else:
            self.NewCommand(points,times,puck_last_velocity)
            #print("New Command 2")

        # Run the current command
        self.move()


    def UpdateCommand(self):
        pass

    def NewCommand(self,points,times,puck_last_velocity):
        
        # If a puck trajectory was calculated
        if len(points) > 1:
            bot_pos = Vec2d(self.body.position[0],self.body.position[1])
            puck_end_pos = Vec2d(points[-1][0],points[-1][1])
            puck_penult_pos = Vec2d(points[-2][0],points[-2][1])


            # Puck hits over or under goal:
            if abs(puck_end_pos[1]-center_y) > 15*7:
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
                if tdiff < 0.5:
                    self.command = "defence"
                    bot_points = [self.body.position, bot_defence_point]
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

        # if puck Trajectory was not calculated, go to center
        else: self.command = "center"