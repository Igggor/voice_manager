#define MY_PERIOD 10    // период в мс
#define LED_PIN 14      // номер пина светодиода

uint32_t myTimer; // переменная времени
String str;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200); // для вывода информации в serial порт
  Serial1.begin(9600);  // для считывания информации с serial порта
}

void loop() {
  if(Serial1.available() && millis() - myTimer >= MY_PERIOD){
    while(Serial1.available()) {
      str += String(char(Serial1.read()));
    }
    Serial.println(str);
    if(str=="None"){}
    else if(str=="On") digitalWrite(LED_PIN, HIGH);
    else if(str=="Off") digitalWrite(LED_PIN, LOW);
    myTimer = millis();         // сбросить таймер
  }
}
