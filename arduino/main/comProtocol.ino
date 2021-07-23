const byte numChars = 50;

boolean newData = false;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing
char sendChars[numChars];
char sendArgument[numChars];
char buff[numChars];
char botpathPointsChars[numChars];
char botpathSpeedsChars[numChars];
// variables to hold the parsed data
//char command[numChars] = {0};
int command = 0;
char parameters[numChars] = {0};
float bot_x_pos = 0.0;
float bot_y_pos = 0.0;
float bot_x_dist = 0.0;
float bot_y_dist = 0.0;
float bot_speed = 0.0;
int numOfArguments = 3;
int argsInt[3];
float argsFloat[3];



struct botPoint{
  float posX;
  float posY;
};

const byte maxNumOfBotPoints = 3;
byte numOfBotPoints;
botPoint botpathPoints[maxNumOfBotPoints];

float botpathSpeeds[maxNumOfBotPoints];

enum Commands{
  CONNECTED = 1,
  RECEIVED = 2,
  ILLEGAL_COMMAND = 3,
  ZERO = 4,
  MOVE = 5,
  MOVE_TO = 6,
  CENTER = 7,
  BOTPATH = 8,
  SOLENOID = 9,
  FAN = 10,
  LIGHT = 11,
  GET_BOTPOS = 12,
  GET_STEPPERPOS = 13,
  GET_LIMIT_SWITCHES = 14,
  MOVE_OUT_OF_LIMITSWITCHES = 15
};

enum Arguments{
  ON = 1,
  OFF = 2,
};

void receiveData() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char beginCommand = '<';
  char endCommand = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
      rc = Serial.read();

      if (recvInProgress == true) {
          if (rc != endCommand) {
              receivedChars[ndx] = rc;
              ndx++;
              if (ndx >= numChars) {
                  ndx = numChars - 1;
              }
          }
          else {
              receivedChars[ndx] = '\0';
              recvInProgress = false;
              ndx = 0;
              newData = true;
          }
      }

      else if (rc == beginCommand) {
          recvInProgress = true;
      }
  }
}


void extractCommand(){
  //Serial.println("Start:");
  //Serial.println(tempChars);
  char * strtokIndx;
  strtokIndx = strtok(tempChars,":"); 
  command = atoi(strtokIndx);
  if(command == MOVE or command == MOVE_TO or command == CENTER){
    for(int i = 0; i < numOfArguments; i++){
      strtokIndx = strtok(NULL, ",");
      argsFloat[i] = atof(strtokIndx);
    }
  }
  else if (command == BOTPATH){
    strtokIndx = strtok(NULL,"|");
    strcpy(botpathPointsChars,strtokIndx);
    strtokIndx = strtok(NULL,"\0");
    strcpy(botpathSpeedsChars,strtokIndx);

    strtokIndx = strtok(botpathPointsChars,",");

    numOfBotPoints = maxNumOfBotPoints;
    for(i=0; i<3; i++){
      float posX = atof(strtokIndx);
      strtokIndx = strtok(NULL," ");
      float posY = atof(strtokIndx);
      strtokIndx = strtok(NULL,",");

      if(posX == 0.0 or posY == 0.0){
        numOfBotPoints = i;
        i = maxNumOfBotPoints;

      }
      else{
        botpathPoints[i].posX =  posX;
        botpathPoints[i].posY = posY;
      }
    }
    // Serial.println("p1X:" + String(botpathPoints[1].posX));
    // Serial.println("p1Y:" + String(botpathPoints[1].posY));
    // Serial.println("num:" + String(numOfBotPoints));

    //Serial.println("SPEEED:");
    //Serial.println(botpathSpeedsChars);
    strtokIndx = strtok(botpathSpeedsChars,",");
    for(i=0;i<numOfBotPoints;i++){
      botpathSpeeds[i] = atof(strtokIndx);
      strtokIndx = strtok(NULL,",");
    }
    //Serial.println("HER:" + String(botpathPoints[0].posX));
    //Serial.println("HER:" + String(botpathPoints[0].posY));
    //Serial.println("HER:" + String(botpathPoints[1].posX));
    //Serial.println("HER:" + String(botpathPoints[1].posY));
    //Serial.println("HER:" + String(botpathSpeeds[0]));
    //Serial.println("HER:" + String(botpathSpeeds[1]));
    //Serial.println("Num points:" + String(numOfBotPoints));
    botpathNum = 0;
    followBotpath_bool = true;
    // Serial.println("Speed:" + String(botpathSpeeds[1]));

    // Serial.println(botpathPointsChars);
    // Serial.println(botpathSpeedsChars);
  }

  else{
    for(int i = 0; i < numOfArguments; i++){
      strtokIndx = strtok(NULL, ",");
      argsInt[i] = atoi(strtokIndx);
    }
  }
}

void executeCommand(){
  sendArgument[0] = '\0';

  switch(command){
    case CONNECTED:
      sendData();
      break;
    case MOVE:
      followBotpath_bool = false;
      sendData();
      //Serial.println("Move: x:" + String(argsFloat[0]) + " y:" + String(argsFloat[1]) + " v:" + String(argsFloat[2]));
      MovePosition(argsFloat[0],argsFloat[1],argsFloat[2]);
      break;
    case MOVE_TO:
      followBotpath_bool = false;
      sendData();
      MoveToPosition(argsFloat[0],argsFloat[1],argsFloat[2]);
      //Serial.println("MoveTo: x:" + String(argsFloat[0]) + " y:" + String(argsFloat[1]) + " v:" + String(argsFloat[2]));
      break;
    case ZERO:
      followBotpath_bool = false;
      sendData();
      goto_zero();
      break;
    case CENTER:
      followBotpath_bool = false;
      sendData();
      goto_center(argsFloat[0]);
      break;
    case BOTPATH:
      sendData();
      followBotpath();
      break;
    case SOLENOID:
      sendData();
      setOutput(solenoid);
      break;
    case FAN:
      sendData();
      setOutput(fan);
      break;
    case LIGHT:
      sendData();
      setOutput(light);
      break;
    case GET_BOTPOS:
      getBotPos(sendArgument);
      sendData();
      break;
    case GET_STEPPERPOS:
      getStepperPos(sendArgument);
      sendData();
      break;
    case GET_LIMIT_SWITCHES:
      sprintf(sendArgument,"%d,%d,%d,%d",digitalRead(endSwitch_L),digitalRead(endSwitch_R),digitalRead(endSwitch_U),digitalRead(endSwitch_D));
      sendData();
      //sprintf(sendArgument,"%d,%d,%d,%d",1,0,1,1);
      break;
    case MOVE_OUT_OF_LIMITSWITCHES:
      followBotpath_bool = false;
      sendData();
      MoveOutOfLimitSwitch();
      break;
    default:
      sendData();
      break;
  }
}

void sendData(){
  sprintf(sendChars,"<%d:%s>",command,sendArgument);
  Serial.println(sendChars);
}


void setOutput(int outputPin){
  int changeOutputTo = argsInt[0];
  if(changeOutputTo == 0){
    digitalWrite(outputPin,LOW);
  }
  else if(changeOutputTo == 1){
    digitalWrite(outputPin,HIGH);
  }
  else if(changeOutputTo == 2){
    digitalWrite(outputPin,HIGH);
    delay(500);
    digitalWrite(outputPin,LOW);
  }
}


void serialCom(){
  receiveData();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    extractCommand();
    executeCommand();
    newData = false;
  }
}
