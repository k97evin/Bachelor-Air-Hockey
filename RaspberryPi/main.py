from globfile import *
#from videoStream import VideoStream
import threading
import serial
#import puck
#import bot
import comProtocol
from comProtocol import Commands
#com = comProtocol.Com('/dev/ttyACM0',115200)
com = comProtocol.Com('COM7',115200)

print("Starting connection")
if com.connect():
    print("Connected with arduino")



com.writeData(Commands.MOVE,100,10,20)
print("venter")
a = com.waitForResponse(Commands.MOVE)
print("a:",a)






