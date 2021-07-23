#include "FastAccelStepper.h"
// With the current stepper pins selected the FastAccelStepper library needs to be changed. 
// Open the file ...\Arduino\libraries\FastAccelStepper\src\AVRStepperPins.h and change line 27 to: #define FAS_TIMER_MODULE 5

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
int motorSpeed = 100; //maximum steps per second (about 3rps / at 16 microsteps)  //max 8000
int motorAccel = 31000; //steps/second/second to accelerate  //max 31000
int SPR = 400; // Steps Per Rev

int stepperL_vel = 0 ;
int stepperR_vel = 0;

int i = 0;
int pos_x = 0;
int pos_y = 0;

float radius = 25.205;

// --- DIFFERENT PATHS --- //

//Only stepper right
//float pointsArray[][2] = {{150,150},{550,550}};

//Only stepper left
//float pointsArray[][2] = {{150,550},{550,150}};

//Square path
//float pointsArray[][2] = {{150,150},{150,550},{550,550},{550,150}};

//Cross and square path
float pointsArray[][2] = {{100,100},{600,600},{100,600},{600,100},{100,100},{100,600},{600,600},{600,100}};

const int ANT_POINTS = sizeof(pointsArray)/8;
int pointNum = 0;

int time = 0;

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperL = NULL;
FastAccelStepper *stepperR = NULL;



//void MoveToPosition(float x, float y){
// stepperL->moveTo(thetaL(x,y,true));
// stepperR->moveTo(thetaR(x,y,true));
//}

void setup() {
  // Pins and Serial
  Serial.begin(9600);
  pinMode(enablePin, OUTPUT);
  pinMode(endSwitch_L,INPUT);
  pinMode(endSwitch_R,INPUT);
  pinMode(endSwitch_U, INPUT);
  pinMode(endSwitch_D, INPUT);
  pinMode(friBryter,INPUT);
  
  Serial.println("Begynner");

  //TCCR5B = TCCR5B & B11111000 | B00000001;
  
  // --- Connecting to steppers --- //
  Connect_to_steppers();

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
  MoveToPosition(pointsArray[pointNum][0],pointsArray[pointNum][1],motorSpeed);
  delayMicroseconds(500);
  if(stepperL->targetPos() == stepperL->getCurrentPosition() && stepperR->targetPos() == stepperR->getCurrentPosition()){
    if(pointNum == ANT_POINTS-1){
      pointNum = 0;
      motorSpeed += 100;
      Serial.println("Speed:" + String(motorSpeed) +"mm/s  stepperL:" + String(stepperL_vel) + "steps/s   stepperR:" + String(stepperR_vel)  + "step/s");

      //Serial.println("Tid: " + String(millis()-time));
      //delay(10000);
    }
    else{
      pointNum ++;
      //if(motorSpeed == 3000){
       // motorSpeed = 4500;
      //}
      //int speedStepsL = stepperL->getSpeedInMilliHz();
      //int speedStepsR = stepperR->getSpeedInMilliHz();
      delayMicroseconds(500);
    }
  }
}


