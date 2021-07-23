from comProtocol import Commands
import threading

import serial
from globfile import *
import puck
from videoStream import VideoStream

class Bot():
    def __init__(self,camera,serialCom):
        self.camera = camera
        self.started = False
        self.startedLock = Lock()
        self.serialCom = serialCom
        #self.puck_pos_vel_points = []
        self.lastYpos = 0
        self.lastPuckEndPos = [0,0]

    def startAlgorithm(self):
        if not self.started:
            self.startedLock.acquire()
            self.started = True
            self.startedLock.release()
            self.thread = Thread(target=self.botThread,daemon=True)
            self.thread.start()

    def stopAlgorithm(self):
        self.startedLock.acquire()
        self.started = False
        self.startedLock.release()


    def botThread(self):
        self.startedLock.acquire()
        started = self.started
        self.startedLock.release()
        i = 1
        j = 0
        k = 0
        puck_pos_vel_points = []
        time.sleep(3)
        while len(puck_pos_vel_points) < 1:
            frame2, current_time, puck_pos = self.camera.get_puck_coordinates()
            if puck_pos != -1:
                puck_pos_vel_points.append([puck_pos, current_time])
                last_puck_pos = puck_pos
        puck_dir = Vec2d.zero()


        while started:
            _, current_time, puck_pos = self.camera.get_puck_coordinates()

            if puck_pos != -1:  
                if current_time != puck_pos_vel_points[-1][1]:
                    
                    puck_pos_vel_points.append([puck_pos, current_time])
                    j += 1
                    k += 1

                    if len(puck_pos_vel_points) == 5:
                        i += 1
                        
                        puck_vel = puck.velocity(puck_pos_vel_points)
                        
                        points, times, last_velocity = puck.path_points2(puck_vel,puck_pos)
                        #print("Her: " , puck_vel, " Points:", points, " times:", times, " lastVel:",last_velocity)
                        moveTo_y = self.defence(points,last_velocity)

                        if moveTo_y != -1 and moveTo_y < 600 and moveTo_y > 100:
                            self.serialCom.writeData(Commands.MOVE_TO,pusher_bottomPos+50,round(moveTo_y,2),3000)
                            time.sleep(0.05)
                        elif last_velocity[0]>=0:
                            self.serialCom.writeData(Commands.MOVE_TO,100,table_center_y,3000)
                            time.sleep(0.05)

                        puck_pos_vel_points.pop(0) 
                        i = 0
                        time.sleep(0.001)
            

            self.startedLock.acquire()
            started = self.started
            self.startedLock.release()



    def defence(self,puck_points,last_velocity):
        puck_endPoint_y = puck_points[-1][1]

        if last_velocity[0] < -100:
            if abs(self.lastYpos - puck_endPoint_y) > 50:
                self.lastYpos = puck_endPoint_y
                return puck_endPoint_y

            else: return -1

        else:
            return -1

    def attack(self):
        pass