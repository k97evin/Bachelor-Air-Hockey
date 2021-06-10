#include <AccelStepper.h>

int motorSpeed = 1200; //maximum steps per second (about 3rps / at 16 microsteps)
int motorAccel = 1000; //steps/second/second to accelerate
int SPR = 400; // Steps Per Rev

int i = 0;
int pos_x = 0;
int pos_y = 0;

int mDir1 = 7; //digital pin 2     < ===THIS IS A DIRECTION PIN
int mStep1 = 6; //digital pin 3
int mDir2 = 9;
int mStep2 = 8;
int enablePin = 2;
float radius = 25.35;


//End switches
int endSwitch_L = 28;
int endSwitch_R = 26;
int endSwitch_U = 22;
int endSwitch_D = 24;



//set up the accelStepper intance
//the "1" tells it we are using a driver
AccelStepper stepperL(1, mStep1, mDir1);
AccelStepper stepperR(1, mStep2, mDir2);


void setup(){
 pinMode(enablePin, OUTPUT);
 pinMode(endSwitch_L,INPUT);
 pinMode(endSwitch_R,INPUT);
 pinMode(endSwitch_U, INPUT);
 pinMode(endSwitch_D, INPUT);
  
 stepperL.setMaxSpeed(motorSpeed);
 stepperL.setAcceleration(motorAccel);
 stepperR.setMaxSpeed(motorSpeed);
 stepperR.setAcceleration(motorAccel);

 
 digitalWrite(enablePin, LOW);
 
 Serial.begin(9600);

 Serial.println("I'm comming home");
 goto_zero();
 Serial.println("stepperL_pos: " +String(stepperL.currentPosition())); 
 Serial.println("stepperR_pos: " +String(stepperR.currentPosition())); 
 pos_x = x_pos(stepperL.currentPosition(), stepperR.currentPosition(), true);
 pos_y = y_pos(stepperL.currentPosition(), stepperR.currentPosition(), true);
 Serial.println("POS: (" + String(pos_x) + "," + String(pos_y) + ")"); 

 stepperL.moveTo(thetaL(450,350,true));
 stepperR.moveTo(thetaR(450,350,true));
}

void loop(){
//Serial.println("End switches: Left:" + String(digitalRead(endSwitch_L))+ " Right: " + String(digitalRead(endSwitch_R))+ " Up: " + String(digitalRead(endSwitch_U))+ " Down: " + String(digitalRead(endSwitch_D)));

//delay(200);
stepperL.run();
stepperR.run();

}

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

  int homing_speed = 20;

  //Zero y-axis
  
  stepperL.setSpeed(homing_speed);
  stepperR.setSpeed(homing_speed);
  
  Serial.println("Before loop");
  while(digitalRead(endSwitch_L) == HIGH){
    //Serial.println(endSwitch_L);
    stepperL.runSpeed();
    stepperR.runSpeed();
  }
  Serial.println("After loop");

  stepperL.stop();
  stepperR.stop();

  delay(500);

  //Move stepper outside left end switch (5mm)
  int steps_stepperL = thetaL(0,5,true);
  Serial.println("Steps_stepperL: " + String(steps_stepperL));
  
  stepperL.move(steps_stepperL);
  stepperR.move(steps_stepperL);


  Serial.println("Before WHile loop");
  while(stepperL.distanceToGo() != 0 || stepperR.distanceToGo() != 0){
    //Serial.println("inside While loop");
    if(stepperL.distanceToGo() != 0){
      stepperL.run();
    }
    if(stepperR.distanceToGo() != 0){
      stepperR.run();
    }
  }
  Serial.println("after while");

  //Zero x-axis
  stepperL.setSpeed(-homing_speed);
  stepperR.setSpeed(homing_speed);
  
  while(digitalRead(endSwitch_D) == HIGH){
    stepperL.runSpeed();
    stepperR.runSpeed();
  }

  stepperL.stop();
  stepperR.stop();

  delay(500);

  //Move stepper outside down end switch (5mm)
  steps_stepperL = thetaL(5,0,true);
  stepperL.move(steps_stepperL);
  stepperR.move(-steps_stepperL);
  
  while(stepperL.distanceToGo() != 0 || stepperR.distanceToGo() != 0){
    //Serial.println("inside While loop");
    if(stepperL.distanceToGo() != 0){
      stepperL.run();
    }
    if(stepperR.distanceToGo() != 0){
      stepperR.run();
    }
  }
  Serial.println("After last loop");

  //zero x = 67 mm, y = 58.5mm
  int stepsL = thetaL(67.0,58.5,true);
  int stepsR = thetaR(67.0,58.5,true);

  Serial.println("StepsL: " + String(stepsL));
  Serial.println("StepsR: " + String(stepsR));
  
  stepperL.setCurrentPosition(stepsL);
  stepperR.setCurrentPosition(stepsR);
  

  digitalWrite(enablePin,LOW);
}
