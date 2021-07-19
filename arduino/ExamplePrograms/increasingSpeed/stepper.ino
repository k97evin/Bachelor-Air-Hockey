// --- CONVERTION FORMULAS --- //
float x_pos(int thetaL, int thetaR, bool steps) {
  float svar = 0;
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

float y_pos(int thetaL, int thetaR, bool steps) {
  float svar = 0;

  if (steps == true) {
    float thetaL_rad = thetaL*(2*PI)/SPR;
    float thetaR_rad = thetaR*(2*PI)/SPR;

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


bool Connect_to_steppers(){

  bool stepper_connection_success = true;

  delay(100);
  engine.init();

  stepperL = engine.stepperConnectToPin(stepPin_L);
  if (stepperL) {
    stepperL->setDirectionPin(dirPin_L);
    stepperL->setEnablePin(enablePin);
  }

  else{
    stepper_connection_success = false;
  }

  delay(100);

  stepperR = engine.stepperConnectToPin(stepPin_R);
  if (stepperR) {
    stepperR->setDirectionPin(dirPin_R);
    stepperR->setEnablePin(enablePin);
  }

  else{
    stepper_connection_success = false;
  }

  // --- stepper start values --- //
  stepperL->setSpeedInHz(motorSpeed);
  stepperL->setAcceleration(motorAccel);    
  stepperR->setSpeedInHz(motorSpeed);
  stepperR->setAcceleration(motorAccel);   

  return stepper_connection_success;
}

void goto_zero(){
  //deactivating stepper enable
  digitalWrite(enablePin,HIGH);

  int homing_speed = 15;
 
  // --- Zero y-axis ---//
  stepperL->setSpeedInHz(homing_speed);
  stepperR->setSpeedInHz(homing_speed);

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

  delay(500);

  //Move stepper outside left end switch (5mm)
  int steps_stepperL = thetaL(0,5,true);
  //Serial.println("Steps_stepperL: " + String(steps_stepperL));

  stepperL->move(steps_stepperL);
  stepperR->move(steps_stepperL);

  delay(200);
  while(stepperL->isMotorRunning() || stepperR->isMotorRunning()){
  }
  //Serial.println("done with y-zero");


  while(stepperL->isMotorRunning() || stepperR->isMotorRunning()){
  }

  //Zero x-axis
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
  stepperL->setCurrentPosition(stepsL);
  stepperR->setCurrentPosition(stepsR);

  //Activating stepper enable
  digitalWrite(enablePin,LOW);

  Serial.println("Done: zero");
}




void MoveToPosition(float posX, float posY, float stepperSpeed){
  if(posX<70.0) posX = 70;
  else if(posX > 620) posX = 620;
  if(posY<65) posY = 65;
  else if (posY > 635) posY = 635;
  
  int stepperL_pos = stepperL->getCurrentPosition();
  int stepperR_pos = stepperR->getCurrentPosition();
  float current_posX = x_pos(stepperL_pos,stepperR_pos,true);
  float current_posY = y_pos(stepperL_pos,stepperR_pos,true);

  float x_dist = posX-current_posX;
  float y_dist = posY-current_posY;
  float dist = sqrt(sq(x_dist) + sq(y_dist));

  float velX = x_dist/dist * stepperSpeed;
  float velY = y_dist/dist * stepperSpeed;

  stepperL_vel = abs(thetaL(velX,velY,true));
  stepperR_vel = abs(thetaR(velX,velY,true));
  
  //Unstable speeds
  int minUnstable = 2900;
  int maxUnstable = 4300;
  int middleUnstable = (maxUnstable+minUnstable)/2;
  if( minUnstable < stepperL_vel && stepperL_vel < middleUnstable) stepperL_vel = minUnstable;
  else if(middleUnstable <= stepperL_vel && stepperL_vel < maxUnstable) stepperL_vel = maxUnstable;
  if( minUnstable < stepperR_vel && stepperR_vel < middleUnstable) stepperR_vel = minUnstable;
  else if(middleUnstable <= stepperR_vel && stepperR_vel < maxUnstable) stepperR_vel = maxUnstable;
  
  stepperL->setSpeedInHz(stepperL_vel); 
  stepperR->setSpeedInHz(stepperR_vel);

  //Serial.println("Moving to: X:"+ String(posX) + " Y:" + String(posY));
  stepperL->moveTo(thetaL(posX,posY,true));
  stepperR->moveTo(thetaR(posX,posY,true));

  //Serial.println("curr posX:"+ String(current_posX) + " curr posY:" + String(current_posY) +" posX:" + String(posX) + " posY:" + String(posY) + " dist"  + String(dist));
  //Serial.println("velx:"+ String(velX) + " Vely:" + String(velY) +" stepperL_vel:" + String(stepperL_vel) + " stepperR_vel:" + String(stepperR_vel));

}