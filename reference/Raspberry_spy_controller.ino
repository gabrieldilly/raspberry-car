#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

ESP8266WiFiMulti WiFiMulti;

#define SSID "SSID"
#define PSSWD "PASSWORD"

int pins[3] = {12,13,4};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0; i<3;i++){
    pinMode(pins[i], INPUT_PULLUP);
  }
  WiFiMulti.addAP(SSID, PSSWD);
}

void loop() {
  // put your main code here, to run repeatedly:
  int motor1, motor2;
  if(digitalRead(pins[0])==0){ //Turn left
    Serial.println("left");
    motor1 = 50;
    motor2 = 50;
  }
  else if(digitalRead(pins[1])==0){ //Go forward
    Serial.println("forward");
    motor1 = 50;
    motor2 = -50;
  }
  else if(digitalRead(pins[2])==0){ //Turn right
    Serial.println("right");
    motor1 = -50;
    motor2 = -50;
  }
  else{
    motor1 = 0;
    motor2 = 0;
  }
  
  if(WiFiMulti.run() == WL_CONNECTED){
    HTTPClient http;
    http.begin("http://192.168.0.46:5000/control/");
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST("{\"motor1\":"+String(motor1)+", \"motor2\":"+String(motor2)+"}");
    String payload = http.getString();
    Serial.print('\t');
    Serial.println(httpCode);
    Serial.println(payload);
  }
  delay(40);
}
