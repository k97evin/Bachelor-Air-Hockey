#include "FastAccelStepper.h"


//Stepper pins
#define dirPin_L 27
#define dirPin_R 28
#define enablePin 29
#define stepPin_L 46  //13
#define stepPin_R 44  //12

//End switches
#define endSwitch_L 39  
#define endSwitch_R 41
#define endSwitch_U 35
#define endSwitch_D 37

#define friBryter 43





//Variables
int motorSpeed = 4000; //maximum steps per second (about 3rps / at 16 microsteps)  //max 8000
int motorAccel = 25000; //steps/second/second to accelerate  //max 31000
int SPR = 400; // Steps Per Rev

int i = 0;
int pos_x = 0;
int pos_y = 0;

float radius = 25.205;
// pusher radius = 95.2

//const int ANT_POINTS = 13;
//float pointsArray[ANT_POINTS][2] = {{100,350},{600,600},{100,600},{600,100},{100,100},{100,600},{600,600},{600,100},{100,100},{100,600},{600,600},{600,100},{100,100}};
const int ANT_POINTS = 7;
float pointsArray[ANT_POINTS][2] = {{150,150},{550,550},{150,150},{550,550},{150,150},{550,550},{150,150}};
// const int ANT_POINTS = sizeof(pointsArray);
int pointNum = 0;

int time = 0;

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperL = NULL;
FastAccelStepper *stepperR = NULL;

int x_pos(int thetaL, int thetaR, bool steps) {
  int svar = 0;
  if (steps == true) {
    float thetaL_rad = thetaL*(2*PI)/SPR;
    float thetaR_rad = thetaR*(2*PI)/SPR;

    svar = 0.5*radius*thetaL_rad - 0.5*radius*thetaR_rad;
  }
  else{
    svar = 0.5*radius*thetaL - 0.5*radius*thetaR;
  } 
  return svar;
}

int y_pos(int thetaL, int thetaR, bool steps) {
  int svar = 0;

  if (steps == true) {
    Serial.println("test1:" + String(thetaL));
    Serial.println("test2:" + String(thetaR));
    float thetaL_rad = thetaL*(2*PI)/SPR;
    float thetaR_rad = thetaR*(2*PI)/SPR;
    Serial.println("test3:" + String(thetaL_rad));
    Serial.println("test4:" + String(thetaR_rad));

    
    svar = -0.5*radius*thetaL_rad - 0.5*radius*thetaR_rad;
  }
  else{
    svar = -0.5*radius*thetaL - 0.5*radius*thetaR;
  }
  return svar;
}


int thetaL(float x,float y,bool steps){
  float svar = -1.0/radius *y + 1.0/radius*x;

  if(steps == true){
    svar = SPR*svar/(2*PI);
  }
  return (int)svar;
}


int thetaR(float x, float y, bool steps){
  float svar = -1.0/radius *y - 1.0/radius*x;

  if(steps == true){
    svar = SPR*svar/(2*PI);
  }
  return (int)svar;
}

void goto_zero(){
  digitalWrite(enablePin,HIGH);
  int homing_speed = 15;
 
  // --- Zero y-axis ---//
  stepperL->setSpeedInHz(homing_speed);
  stepperR->setSpeedInHz(homing_speed);

  Serial.println("Before loop");
  stepperL->runForward();
  stepperR->runForward();
  while(digitalRead(endSwitch_L) == HIGH){
    if(digitalRead(friBryter) == LOW){
      while(digitalRead(friBryter) == LOW){
        digitalWrite(enablePin,LOW);
      }
      digitalWrite(enablePin,HIGH);
    }
  }
  stepperL->stopMove();
  stepperR->stopMove();
  Serial.println("After loop");

  delay(500);

  //Move stepper outside left end switch (5mm)
  int steps_stepperL = thetaL(0,5,true);
  Serial.println("Steps_stepperL: " + String(steps_stepperL));

  stepperL->move(steps_stepperL);
  stepperR->move(steps_stepperL);

  Serial.println("Before WHile loop");
  delay(200);
  while(stepperL->isMotorRunning() || stepperR->isMotorRunning()){
  }


  Serial.println("Ferdig med y-zero");



  while(stepperL->isMotorRunning() || stepperR->isMotorRunning()){
  }

  //Zero x-axis
  //stepperL->setSpeedInHz(-homing_speed);
  //stepperR->setSpeedInHz(homing_speed);
  stepperL->runBackward();
  stepperR->runForward();
  
  while(digitalRead(endSwitch_D) == HIGH){
  }
  stepperL->stopMove();
  stepperR->stopMove();

  delay(500);

  //Move stepper outside down end switch (5mm)
  steps_stepperL = thetaL(5,0,true);
  stepperL->move(steps_stepperL);
  stepperR->move(-steps_stepperL);
  delay(200);
  while(stepperL->isMotorRunning() || stepperR->isMotorRunning()){
  }

  int stepsL = thetaL(62.7,56.0,true);
  int stepsR = thetaR(62.7,56.0,true);

  Serial.println("StepsL: " + String(stepsL));
  Serial.println("StepsR: " + String(stepsR));

  stepperL->setCurrentPosition(stepsL);
  stepperR->setCurrentPosition(stepsR);

  digitalWrite(enablePin,LOW);

}


void MoveToPosition(float x, float y){
 stepperL->moveTo(thetaL(x,y,true));
 stepperR->moveTo(thetaR(x,y,true));
}

void setup() {
  // Pins and Serial
  Serial.begin(9600);
  pinMode(enablePin, OUTPUT);
  pinMode(endSwitch_L,INPUT);
  pinMode(endSwitch_R,INPUT);
  pinMode(endSwitch_U, INPUT);
  pinMode(endSwitch_D, INPUT);
  pinMode(friBryter,INPUT);
  

  //TCCR5B = TCCR5B & B11111000 | B00000001;
  
  // --- Connecting to steppers --- //
  Serial.println("Connectiong to stepper left");
  delay(100);
  engine.init();

  stepperL = engine.stepperConnectToPin(stepPin_L);
  if (stepperL) {
    stepperL->setDirectionPin(dirPin_L);
    stepperL->setEnablePin(enablePin);
    //stepperL->setAutoEnable(true);

    Serial.println("stepper left found");
    Serial.println(stepperL->getCurrentPosition());
  }

  else{
    Serial.println("Error: Cant connect to stepper left");
  }

  Serial.println("Connectiong to stepper right");
  delay(100);

  stepperR = engine.stepperConnectToPin(stepPin_R);
  if (stepperR) {
    stepperR->setDirectionPin(dirPin_R);
    stepperR->setEnablePin(enablePin);
    //stepperR->setAutoEnable(true);

    Serial.println("stepper right found");

    Serial.println(stepperR->getCurrentPosition());
  }

  else{
    Serial.println("Error: Cant connect to stepper right");
  }

  // --- stepper start values --- //
  stepperL->setSpeedInHz(motorSpeed);
  stepperL->setAcceleration(motorAccel);    
  stepperR->setSpeedInHz(motorSpeed);
  stepperR->setAcceleration(motorAccel);   

  // --- zeroing --- //
  digitalWrite(enablePin, LOW);
  goto_zero();

  stepperL->setSpeedInHz(motorSpeed);
  stepperR->setSpeedInHz(motorSpeed);

  time = millis();
}

void loop(){
  MoveToPosition(pointsArray[pointNum][0],pointsArray[pointNum][1]);
  if(stepperL->targetPos() == stepperL->getCurrentPosition() && stepperR->targetPos() == stepperR->getCurrentPosition()){
    if(pointNum == ANT_POINTS-1){
      pointNum = 0;
      //Serial.println("Tid: " + String(millis()-time));
      //delay(10000);
    }
    else{
      pointNum ++;
      motorSpeed += 100;
      if(motorSpeed == 3000){
        motorSpeed = 4500;
      }
      stepperL->setSpeedInHz(motorSpeed);
      stepperR->setSpeedInHz(motorSpeed);
      Serial.println(motorSpeed);
    }
  }
}


