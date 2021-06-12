import threading
from globfile import *

import serial
from enum import Enum
import re

class Commands(Enum):
    NONE = 0
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


class SerialCom():
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
        self.lastArgsLock = Lock()
        self.lastRecievedArgs = []
        self.lastMessageLock = Lock()
        self.lastReceivedMessage = ""
        #Thread(target=self.writingThread,daemon=True).start()


    def connect(self):
        self.ser = serial.Serial(self.comport,self.baudrate,timeout=1)
        time.sleep(2)
        Thread(target=self.readingThread,daemon=True).start()
        self.emptyCom()
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
            #print("se:", self.sendtCommands)
            if not command.value in self.sendtCommands:
                receivedResponse = True
            self.sendtCommandsLock.release()
            
            time.sleep(0.01)

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
                #print("incommingLine:" + line)
                newMessage = True
            self.serLock.release()

            if newMessage:
                self.lastMessageLock.acquire()
                self.lastReceivedMessage = ""
                command,arguments = self.extractData(line)
                if command != Commands.NONE:
                    if self.checkIfReturnValue(command):
                        self.lastArgsLock.acquire()
                        self.lastRecievedArgs = arguments
                        self.lastArgsLock.release()
                    self.sendtCommandsLock.acquire()

                    try:
                        self.sendtCommands.remove(command.value)
                    except:
                        print("received wrong command:", command)
                        print(self.sendtCommands)

                    self.sendtCommandsLock.release()
                    #print("Sema value: ",self.sema._value)
                    self.sema.release()
                else:
                    self.lastReceivedMessage = line

                newMessage = False
                self.lastMessageLock.release()
            time.sleep(0.1)

    
    def getLastReceivedMessage(self):
        self.lastMessageLock.acquire()
        message = self.lastReceivedMessage
        self.lastMessageLock.release()
        return message

    def writeBotpath(self,botpathPoints,botpathSpeeds):
        data = f"<{Commands.BOTPATH}:"
        pointArgument = ""
        speedArgument = ""
        for i in range(len(botpathPoints)):
            pointArgument += f"{botpathPoints[i][0]},{botpathPoints[i][1]} "
            speedArgument += f"{botpathSpeeds[i]},"

        data += pointArgument[:-1] + "|" + speedArgument[:-1] + ">"

        return data
        
     
    def readData(self, command):
        args = []
        if self.checkIfReturnValue(command):
            data = f"<{command.value}:"

            self.sendtCommandsLock.acquire()
            self.sendtCommands.append(command.value)
            self.sendtCommandsLock.release()

            self.sema.acquire()
            self.ser.write((data.encode('utf-8')))

            self.waitForResponse(command)
            self.lastArgsLock.acquire()
            args = self.lastRecievedArgs 
            self.lastArgsLock.release()

        else:
            print("Use writeData")

        return args

    def writeData(self,command,*args):
        if self.checkIfReturnValue(command):
            print("Use readData")
        else:
            data = f"<{command.value}:"
            self.sendtCommandsLock.acquire()
            self.sendtCommands.append(command.value)
            self.sendtCommandsLock.release()

            for arg in args:
                data += f"{arg},"
            data = data[:-1] + ">"

            self.sema.acquire()
            self.ser.write((data.encode('utf-8')))



    def extractData(self,line):
        command = Commands.NONE
        arguments = []
        data = re.search("<([0-9]+):?(-?[a-zA-Z0-9\.\, -]*)>",line)

        if data != None:
            command = Commands(int(data.group(1)))
            arguments_string = data.group(2).split(',')  
            if self.checkIfReturnValue(command):
                if command == Commands.GET_LIMIT_SWITCHES:
                    arguments = [int(x) for x in arguments_string]
                else:
                    arguments = [float(x) for x in arguments_string]

       
        else: print("Incomming line:"  + line)

        return command,arguments


    def checkIfReturnValue(self,command):
        if command == Commands.GET_BOTPOS or command == Commands.GET_STEPPERPOS or command == Commands.GET_LIMIT_SWITCHES:
            return True
        else: 
            return False

    def emptyCom(self):
        self.serLock.acquire()
        self.lastArgsLock.acquire()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.lastRecievedArgs = []
        self.sema = threading.Semaphore(7)
        time.sleep(1)
        self.lastArgsLock.release()
        self.serLock.release()


