<<<<<<< HEAD
steps_per_round = 400
stepper_radius = int(2.5*7)

def runStepperRelative(DeltaX,DeltaY,SpeedX,SpeedY):
    DeltaTheta1 = -1/stepper_radius*DeltaY+1/stepper_radius*DeltaX
    DeltaTheta2 = -1/stepper_radius*DeltaY-1/stepper_radius*DeltaX

    maxSpeedTheta1 = -1/stepper_radius*SpeedY+1/stepper_radius*SpeedX
    maxSpeedTheta2 = -1/stepper_radius*SpeedY-1/stepper_radius*SpeedX

    return DeltaTheta1, DeltaTheta2, maxSpeedTheta1, maxSpeedTheta2

def moveStepper(DeltaTheta1, DeltaTheta2, maxSpeedTheta1, maxSpeedTheta2):
    speedY = -1/2 * stepper_radius * maxSpeedTheta1 - 1/2*stepper_radius*maxSpeedTheta2
    speedX = 1/2 * stepper_radius * maxSpeedTheta1 - 1/2*stepper_radius*maxSpeedTheta2

    deltaY = -1/2 * stepper_radius * DeltaTheta1 - 1/2*stepper_radius*DeltaTheta2
    deltaX = 1/2 * stepper_radius * DeltaTheta1 - 1/2*stepper_radius*DeltaTheta2

    return deltaX, deltaY, speedX, speedY



deltaX = 5
deltaY = 10
speedX = 15
speedY = 20

a,b,c,d = runStepperRelative(deltaX,deltaY,speedX,speedY)

print(moveStepper(a,b,c,d))
=======
from Puck_path import puck_path
>>>>>>> 4d1305633d3e89261a489fafa868dff3a44d571d
