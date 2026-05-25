#include <Servo.h>

int ledLight = 13;
int ledMotion = 12;
int ledTemp = 8;
int ledFan = 5;

int emergencyButton = 2;
int lightButton = 3;

int redEmergencyLed = 6;
int greenEmergencyLed = 7;

int servoPin = 4;
int trigPin = 9;
int echoPin = 10;

int tempPin = A1;

Servo garageServo;

bool emergencyMode = false;
bool fanOn = false;

bool motionActive = false;
unsigned long motionStart = 0;

float stableTemperature = 0;

void setup() {
  pinMode(ledLight, OUTPUT);
  pinMode(ledMotion, OUTPUT);
  pinMode(ledTemp, OUTPUT);
  pinMode(ledFan, OUTPUT);

  pinMode(redEmergencyLed, OUTPUT);
  pinMode(greenEmergencyLed, OUTPUT);

  pinMode(emergencyButton, INPUT_PULLUP);
  pinMode(lightButton, INPUT_PULLUP);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  garageServo.attach(servoPin);
  garageServo.write(0);

  Serial.begin(9600);

  digitalWrite(greenEmergencyLed, HIGH);
  digitalWrite(redEmergencyLed, LOW);
}

float readStableTemperature() {
  long sum = 0;

  for (int i = 0; i < 30; i++) {
    sum += analogRead(tempPin);
    delay(2);
  }

  int avgReading = sum / 30;
  float newTemperature = map(avgReading, 0, 1023, 0, 100);

  if (abs(newTemperature - stableTemperature) > 1.5) {
    stableTemperature = newTemperature;
  }

  return stableTemperature;
}

void loop() {
  float temperature = readStableTemperature();

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "MOTION") {
      motionActive = true;
      motionStart = millis();
      digitalWrite(ledMotion, HIGH);
    }

    if (cmd == "EMERGENCY OFF") {
      emergencyMode = false;
    }
  }

  if (digitalRead(emergencyButton) == LOW) {
    emergencyMode = true;
    delay(200);
  }

  if (emergencyMode) {
    digitalWrite(greenEmergencyLed, LOW);
    digitalWrite(redEmergencyLed, HIGH);

    digitalWrite(ledLight, LOW);
    digitalWrite(ledTemp, LOW);
    digitalWrite(ledFan, LOW);

    garageServo.write(0);
    return;
  } else {
    digitalWrite(greenEmergencyLed, HIGH);
    digitalWrite(redEmergencyLed, LOW);
  }

  if (digitalRead(lightButton) == LOW) {
    digitalWrite(ledLight, HIGH);
  } else {
    digitalWrite(ledLight, LOW);
  }

  if (motionActive && millis() - motionStart >= 10000) {
    digitalWrite(ledMotion, LOW);
    motionActive = false;
  }

  digitalWrite(ledTemp, temperature > 50 ? HIGH : LOW);

  if (temperature > 30) fanOn = true;
  if (temperature < 24) fanOn = false;

  digitalWrite(ledFan, fanOn ? HIGH : LOW);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  int distance = duration * 0.034 / 2;

  if (distance > 0 && distance < 10) {
    garageServo.write(90);
  } else {
    garageServo.write(0);
  }

  Serial.print("TEMP=");
  Serial.print(temperature);
  Serial.print(";DIST=");
  Serial.print(distance);
  Serial.print(";FAN=");
  Serial.print(fanOn ? 1 : 0);
  Serial.print(";EMERGENCY=");
  Serial.println(emergencyMode ? 1 : 0);

  delay(1000);
}