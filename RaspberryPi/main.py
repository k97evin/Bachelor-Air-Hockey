from globfile import *
import os
from KivyApp import MyApp
#from videoStream import VideoStream
import threading
import serial
#import puck
#import bot
import comProtocol
from comProtocol import Commands
#com = comProtocol.Com('/dev/ttyACM0',115200)
# com = comProtocol.Com('COM7',115200)

# print("Starting connection")
# if com.connect():
#     print("Connected with arduino")



# com.writeData(Commands.MOVE,100,10,20)
def main():
    try:
        app = MyApp()
        app.run()
    except Exception as e:
        print("Exception: ",str(e))
        os._exit(1)

if __name__ == "__main__":
	main()




