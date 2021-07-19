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

//Defining stepper motors
FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperL = NULL;
FastAccelStepper *stepperR = NULL;

void setup() {
  // Pins and Serial
  Serial.begin(9600);
  pinMode(enablePin, OUTPUT);
  pinMode(endSwitch_L,INPUT);
  pinMode(endSwitch_R,INPUT);
  pinMode(endSwitch_U, INPUT);
  pinMode(endSwitch_D, INPUT);
  pinMode(friBryter,INPUT);
  
  
  // --- Connecting to steppers --- //
  Serial.println("Connectiong to stepper left");
  delay(100);
  engine.init();

  stepperL = engine.stepperConnectToPin(stepPin_L);
  if (stepperL) {
    stepperL->setDirectionPin(dirPin_L);
    stepperL->setEnablePin(enablePin);

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


  // --- activating limit switches --- //
  digitalWrite(enablePin, LOW);
  delay(1000);

  // --- stepper program --- //
  stepperL->setSpeedInHz(150); //steps/sec
  stepperL->setAcceleration(400); //steps/sec^2 
  stepperR->setSpeedInHz(150);
  stepperR->setAcceleration(400);   

  //moving left stepper 400 steps (1 round)
  Serial.println("Moving left stepper");
  stepperL->move(400); 

  delay(5000);

  //moving right stepper 100 steps (1 round)
  Serial.println("Moving right stepper");
  stepperR->move(400); 
}



void loop(){

}
