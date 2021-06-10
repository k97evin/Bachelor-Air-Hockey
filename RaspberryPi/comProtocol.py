import threading
from globfile import *

import serial
from enum import Enum
import re

class Commands(Enum):
    CONNECTED = 1
    RECIEVED = 2
    ILLEGAL_COMMAND = 3
    ZERO = 4
    MOVE = 5
    MOVE_TO = 6
    CENTER = 7
    BOTPATH = 8
    SOLENOID = 9
    FAN = 10
    LIGHT = 11
    GET_BOTPOS = 12
    GET_STEPPERPOS = 13
    GET_LIMIT_SWITCHES = 14
    
#class Parameter(Enum):
#    LIMITSWITCHES = 1
#    BOTPOS = 2
#    STEPPERPOS = 3

class Com():
    def __init__(self,comport, baudrate):
        self.comport = comport
        self.baudrate = baudrate
        self.ser = None
        self.runThread = True
        self.runThreadLock = Lock()
        self.serLock = Lock()
        self.sendtCommandsLock = Lock()
        self.sema = threading.Semaphore(7)
        self.sendtCommands = []
        #Thread(target=self.writingThread,daemon=True).start()


    def connect(self):
        self.ser = serial.Serial(self.comport,self.baudrate,timeout=1)
        time.sleep(2)
        Thread(target=self.readingThread,daemon=True).start()
        self.ser.flush()
        time.sleep(0.5)
        self.writeData(Commands.CONNECTED)
        arduinoConnected = False

        arduinoConnected =  self.waitForResponse(Commands.CONNECTED)

        return arduinoConnected
        
    
    # def writingThread(self):
    #     self.runThreadLock.acquire()
    #     runThreadBuff = self.runThread
    #     self.runThreadLock.release()

    #     while runThreadBuff:
    #         pass

    def waitForResponse(self,command):
        '''
        Warning: This method is blocking
        '''

        receivedResponse = False
        while not receivedResponse:
            self.sendtCommandsLock.acquire()
            if not command.value in self.sendtCommands:
                receivedResponse = True
            self.sendtCommandsLock.release()
            
            time.sleep(0.1)

        return receivedResponse
        


    def readingThread(self):
        runThreadBuff = True
        newMessage = False
        line = ""
        while runThreadBuff:
            self.runThreadLock.acquire()
            runThreadBuff = self.runThread
            self.runThreadLock.release()

            self.serLock.acquire()
            if self.ser.inWaiting() > 0 and runThreadBuff:
                line = self.ser.readline().decode('utf-8').rstrip()
                print("incommingLine:" + line)
                newMessage = True
            self.serLock.release()

            if newMessage:
                command,parametres = self.extractData(line)
                if command != "":
                    self.sendtCommandsLock.acquire()
                    try:
                        self.sendtCommands.remove(int(command))
                    except:
                        print("received wrong command:" + command)
                        print(self.sendtCommands)
                    self.sendtCommandsLock.release()
                    print("Sema value: ",self.sema._value)
                    self.sema.release()
                newMessage = False




    def writeData(self,command,*args):
        data = f"<{command.value}:"
        self.sendtCommandsLock.acquire()
        self.sendtCommands.append(command.value)
        self.sendtCommandsLock.release()

        for arg in args:
            data += f"{arg},"
        data = data[:-1] + ">"
        print("Sema value: ",self.sema._value)
        print("sendingData: ", data)
        self.sema.acquire()
        self.ser.write((data.encode('utf-8')))


    def extractData(self,line):
        command = ""
        parameters = ""
        data = re.search("<([0-9]+):?([a-zA-Z0-9\.\,]*)>",line)

        if data != None:
            command = data.group(1)
            parameters = data.group(2)         
        else: print("line:"  + line)

        return command,parameters
