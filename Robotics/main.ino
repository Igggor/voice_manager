void setup() {
  pinMode(14, OUTPUT);
  digitalWrite(14,0);

  Serial.begin(115200);
  Serial1.begin(9600);
}

void loop() {
  
  if(Serial1.available()){
    String str;
    delay(10);
    while(Serial1.available()) str+=String(char(Serial1.read()));
    Serial.println(str);
    if(str=="None"){}
    else if(str=="On") digitalWrite(14,1);
    else if(str=="Off") digitalWrite(14,0);
  }
  
}
