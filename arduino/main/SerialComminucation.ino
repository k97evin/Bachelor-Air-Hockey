const byte numChars = 32;

boolean newData = false;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing
char sendChars[numChars];
char sendArgument[numChars];

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
  char * strtokIndx;
  strtokIndx = strtok(tempChars,":"); 
  command = atoi(strtokIndx);
  Serial.println("Commanden er:" + String(command));
  if(command == MOVE or command == MOVE_TO){
    for(int i = 0; i < numOfArguments; i++){
      strtokIndx = strtok(NULL, ",");
      argsFloat[i] = atof(strtokIndx);
    }
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
      break;
    case MOVE:
      MovePosition(argsFloat[0],argsFloat[1],argsFloat[2]);
      Serial.println("Move: x:" + String(argsFloat[0]) + " y:" + String(argsFloat[1]) + " speed:" + String(argsFloat[2]));
      break;
    case MOVE_TO:
      break;
    case GET_LIMIT_SWITCHES:
      sprintf(sendArgument,"%d,%d,%d,%d",digitalRead(35),digitalRead(37),digitalRead(39),digitalRead(41));
      break;
    case SOLENOID:
      break;
    default:
      break;
  }
}

void sendData(){
  sprintf(sendChars,"<%d:%s>",command,sendArgument);
  Serial.println(sendChars);
}


void serialCom(){
  receiveData();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    extractCommand();
    executeCommand();
    sendData();
    newData = false;
  }
}
