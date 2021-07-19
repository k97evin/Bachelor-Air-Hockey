

import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  

from comProtocol import SerialCom, Commands

import time
# Serial object to communicate
try:
    serialCom = SerialCom('/dev/ttyACM0', 115200)
    #serialCom = SerialCom("COM6", 115200)
    serialCom.connect()
except:
    print("Could not open port")

time.sleep(0.5)


#Example on how to use the python COM protocol

# --- ZEROING --- #
print("Zeroing")
time.sleep(1)
serialCom.writeData(Commands.ZERO)

#If you want to wait for the bot to finish zeroing:
doneZero = False
while not doneZero:
    message = serialCom.getLastReceivedMessage()
    if message == "Done: zero":
        doneZero = True
    time.sleep(0.3)


# --- MOVE --- #
#Relative motion
#Takes three arguments: x-pos [mm], y-pos [mm], speed [mm/s]
print("Moving")
time.sleep(1)
serialCom.writeData(Commands.MOVE,100,100,300)
time.sleep(2)

# --- MOVE TO --- #
#Absolute motion
#Takes three arguments: x-pos [mm], y-pos [mm], speed [mm/s]
print("Moving to")
time.sleep(1)
serialCom.writeData(Commands.MOVE_TO,100,100,300)
time.sleep(2)

# --- CENTER --- #
#Moves to center infront of goal
#Argument: speed [mm/s]
print("Center")
time.sleep(1)
serialCom.writeData(Commands.CENTER,300)
time.sleep(2)


# --- BOTPATH --- #
#Moves from point to point.
#Takes inn up to three points and needs a speed to each point
#Points are in mm and speeds are in mm/s
print("Botpath")
time.sleep(1)
botpath_points = [[100,300],[200,150],[100,100]]
botpath_speeds = [300,300,400]
serialCom.writeBotpath(botpath_points,botpath_speeds)
time.sleep(4)


# --- SOLENOID --- #
#inn(0), out(1), out and inn(2)
print("Solenoid")
time.sleep(1)
serialCom.writeData(Commands.SOLENOID,2)
time.sleep(1)

# --- FAN and LIGHT --- #
#turn on(1) or off(0) fan or light
print("Fan and light")
time.sleep(1)
serialCom.writeData(Commands.FAN,1)
serialCom.writeData(Commands.LIGHT,1)
time.sleep(2)
serialCom.writeData(Commands.FAN,0)
serialCom.writeData(Commands.LIGHT,0)
time.sleep(1)

# --- GET BOTPOS --- #
print("Bot position:")
time.sleep(1)
bot_pos = serialCom.readData(Commands.GET_BOTPOS)
print(bot_pos)
print(bot_pos[0])


# --- GET LIMIT SWITCHES --- #
print("Limit switches")
time.sleep(1)
limit_switches = serialCom.readData(Commands.GET_LIMIT_SWITCHES)
print(limit_switches)
print(limit_switches[0])


# --- MOVE OUT OF LIMIT SWITCHES ---#
#If the bot is stuck at a limit switch then this command will move it away
#Warning: zeroing should be used after this 
print("Moving out of limit switches")
time.sleep(1)
serialCom.writeData(Commands.MOVE_OUT_OF_LIMITSWITCHES)
time.sleep(3)
        