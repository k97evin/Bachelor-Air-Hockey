'''

This script is for testing communication with the Arduino either with a pc or Raspberry pi.
Upload the main program in the Arduino folder to the Arduino.

The Arduino will accept the commands listed below. Write "exit" when done.
NB: Zeroing is recommended before using move_to, center ro botpath

List of commands:
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
    MOVE_OUT_OF_LIMITSWITCHES = 15

Command structure:
    without arguments:
        <CommandNumber>
        or
        <CommandNumber:> 

    wtih arguments:
        <CommandNumber:Argument>
        <CommandNumber:Argument,Argument,...>
    


Command Example:
    zeroing:
        <4>
    move:
        Relative motion.
        Takes three arguments: x-pos [mm], y-pos [mm], speed [mm/s]
        <5:100,100,50>
    move_to:
        Absolute motion
        Takes three arguments: x-pos [mm], y-pos [mm], speed [mm/s].
        <6:100,100,50>
    center:
        Moves to center infront of goal
        Argument: speed [mm/s]
        <7:300>
    botpath:
        Moves from point to point.
        Takes inn up to three points and needs a speed to each point
        Arguments: point1 point2 point3|speed1,speed2,speed3 
        <8:100,100 150,100 100,150|100,200,300>
        or
        <8:100,100 150,100|100,300>
    solenoid:
        inn(0), out(1), out and inn(2)
        <9:2>
    fan and light:
        turn on(1) or off(0) fan or light
        <10:1>
        <11:1>
    
    the rest dosent have arguments and can be used like this:
        <12>

'''



#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    #ser = serial.Serial(port="COM7", baudrate=115200, timeout=1)
    ser.flush()

    done = False
    while not done:
        data = input("commando: ")

        if data == "exit" or data == "Exit":
            done = True

        else:
            ser.write((data.encode('utf-8')))
            time.sleep(2)
            while ser.inWaiting() > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print("line: " + line)
            time.sleep(1)
