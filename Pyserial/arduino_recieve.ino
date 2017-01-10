char buffer[18];
int bad = 8;
int good = 7;
int motor11 = 10;
//On delay
int x = 500;
//Off delay
int y = 1000;

void setup(){
  Serial.begin(9600);
  Serial.flush();
  pinMode(bad, OUTPUT);
  pinMode(good, OUTPUT);
  pinMode(motor11, OUTPUT);
}

void loop(){
  if(Serial.available() > 0){
    int index=0;
    delay(100);
    int numChar = Serial.available();
    if(numChar>150){
      numChar=150;
    }
    while (numChar--){
      buffer[index++] = Serial.read();
    }
    splitString(buffer);
  }
  digitalWrite(motor11, HIGH);
}
void splitString(char* data){
  Serial.println(data);
  char* parameter;
  parameter = strtok(data,",");
  while(parameter != NULL){
    setLED(parameter);
    parameter = strtok(NULL,",");
  }
  for(int x=0; x<16; x++){
    buffer[x]='\0';
  }
  Serial.flush();
}
void setLED(char* data){
  if ((data[0]=='R')){
    digitalWrite(good, HIGH);
    delay(600);
    digitalWrite(good, LOW);
    delay(100);
    digitalWrite(motor11, LOW);
    delay(2000);
  }
  
  if ((data[0]=='W')){
    digitalWrite(bad, HIGH);
    delay(600);
    digitalWrite(bad, LOW);
  }
}


