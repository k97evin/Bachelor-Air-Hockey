#include "FastAccelStepper.h"

// Stepper pins
#define dirPin_L 27
#define dirPin_R 28
#define enablePin 29
#define stepPin_L 46  //13
#define stepPin_R 44  //12

// End switches
#define endSwitch_L 39  
#define endSwitch_R 41
#define endSwitch_U 35
#define endSwitch_D 37

#define friBryter 43

//Emergency swtiches
#define emergency_switch_bot 45
#define emergency_switch_player 47

//IR sensors
#define ir_bot 20
#define ir_player 21

// Relay
#define solenoid 22
#define light 23
#define fan 24


#define fan_pwm_player 9
#define fan_pwm_bot 10
#define fan_taco_player 18
#define fan_taco_bot 19

// Variables
int motorSpeed = 1000; // mm/s
int motorAccel = 31000; // steps/s^2 to accelerate  //max 31000
int SPR = 400; // Steps Per Rev

int i = 0;
int pos_x = 0;
int pos_y = 0;

float radius = 25.205;

int time = 0;


// Stepper declearation 
FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperL = NULL;
FastAccelStepper *stepperR = NULL;

int botpathNum = -1;
bool followBotpath_bool = false;

void setup() {
  // --- Pins and Serial --- //
  Serial.begin(115200);
  pinMode(enablePin, OUTPUT);
  pinMode(solenoid,OUTPUT);
  pinMode(light,OUTPUT);
  pinMode(fan,OUTPUT);
  pinMode(fan_pwm_player,OUTPUT);
  pinMode(fan_pwm_bot,OUTPUT);
  pinMode(endSwitch_L,INPUT);
  pinMode(endSwitch_R,INPUT);
  pinMode(endSwitch_U, INPUT);
  pinMode(endSwitch_D, INPUT);
  pinMode(friBryter,INPUT);
  
  // --- Connecting to steppers --- //
  bool stepper_connection = Connect_to_steppers();

  if(!stepper_connection){
    Serial.println("Couldnt connect to steppers");
  }


  // --- Stepper starting speed --- //
  stepperL->setSpeedInHz(motorSpeed);
  stepperR->setSpeedInHz(motorSpeed);

  time = millis();
  digitalWrite(enablePin,LOW);
  digitalWrite(fan_pwm_bot,HIGH);
  digitalWrite(fan_pwm_player,HIGH);
}

void loop(){
  serialCom();
  if(followBotpath_bool == true && botpathNum != -1){
    followBotpath();
  }
}
