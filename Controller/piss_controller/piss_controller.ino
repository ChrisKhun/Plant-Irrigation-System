
#define PUMP_PIN 2

void setup() {
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
}

void loop() {
  digitalWrite(PUMP_PIN, LOW);
  delay(5000);

  digitalWrite(PUMP_PIN, HIGH);
  delay(5000);
}
