#include <SoftwareSerial.h>
#include <ParallaxRFID.h>

ParallaxRFID RFIDclient(9, 8);

const int ENTERING_READY_LAMP = 10;
const int EXIT_READY_LAMP = 11;

const int ENTERING_BTN = 12;
const int EXIT_BTN = 13;

int selectedBtn = ENTERING_BTN;

void setup()
{
  // set serial
  Serial.begin(9600);
  
  // set output mode
  pinMode(ENTERING_READY_LAMP, OUTPUT);
  pinMode(EXIT_READY_LAMP, OUTPUT);

  // set input mode
  pinMode(ENTERING_BTN, INPUT);
  pinMode(EXIT_BTN, INPUT);
}

void loop()
{ 
  getSelectedBtn();
  switchReadyLamp();

  int userId = RFIDclient.readRFID(4);
  if (userId != 0) {
    sendToSerial(userId);
  }

  delay(400);
}

void getSelectedBtn()
{
  if (digitalRead(ENTERING_BTN) != 0) {
    selectedBtn = ENTERING_BTN;
  }
 
  if (digitalRead(EXIT_BTN) != 0) {
    selectedBtn = EXIT_BTN;
  } 
}

void switchReadyLamp()
{
  if (selectedBtn == ENTERING_BTN) {
    digitalWrite(ENTERING_READY_LAMP, HIGH);
    digitalWrite(EXIT_READY_LAMP, LOW);
  }

  if (selectedBtn == EXIT_BTN) {
    digitalWrite(EXIT_READY_LAMP, HIGH);
    digitalWrite(ENTERING_READY_LAMP, LOW);
  }
}

void sendToSerial(int userId) 
{
  if (selectedBtn == ENTERING_BTN) {
    Serial.print(userId); 
    Serial.println(",in");
  }
  
  if (selectedBtn == EXIT_BTN) {
    Serial.print(userId); 
    Serial.println(",out");
  }
}
