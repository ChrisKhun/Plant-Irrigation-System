#include <DHT.h>

#define PUMP_PIN 2
#define SOIL_SENSOR 15
#define DHT_SENSOR 4
#define DHTTYPE DHT11

DHT dht(DHT_SENSOR, DHTTYPE);

bool pumpOn = false;

// Default pump duration: 5 seconds
int pumpDuration = 5;

unsigned long pumpStartTime = 0;
unsigned long lastSensorUpdate = 0;
unsigned long activeDuration = 5000;

String command = "";

void setup() {
  // Pump OFF by default (active-HIGH MOSFET)
  digitalWrite(PUMP_PIN, LOW);
  pinMode(PUMP_PIN, OUTPUT);

  Serial.begin(115200);
  dht.begin();
}

void loop() {
  // Read commands from Tkinter
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      command.trim();
      handleCommand(command);
      command = "";
    }
    else if (c != '\r') {
      if (command.length() < 40) {
        command += c;
      } else {
        command = "";
      }
    }
  }

  // Automatically stop pump after selected duration
  if (pumpOn &&
      millis() - pumpStartTime >= activeDuration) {
    stopPump();
  }

  // Send sensor data every 2 seconds
  if (millis() - lastSensorUpdate >= 2000) {
    lastSensorUpdate = millis();
    sendSensorData();
  }
}

void handleCommand(String cmd) {

  // Update pump duration from Tkinter
  // Example: DURATION:10
  if (cmd.startsWith("DURATION:")) {
    int seconds = cmd.substring(9).toInt();

    if (seconds >= 1 && seconds <= 30) {
      pumpDuration = seconds;
      sendSensorData();
    }
  }

  // Start watering when Water Now is clicked
  else if (cmd == "WATER") {
    if (!pumpOn) {
      pumpOn = true;
      pumpStartTime = millis();
      activeDuration = (unsigned long)pumpDuration * 1000UL;

      // MOSFET ON
      digitalWrite(PUMP_PIN, HIGH);

      sendSensorData();
    }
  }

  // Stop watering manually
  else if (cmd == "STOP") {
    stopPump();
  }
}

void stopPump() {
  // MOSFET OFF
  digitalWrite(PUMP_PIN, LOW);

  pumpOn = false;
  sendSensorData();
}

void sendSensorData() {
  float temperature = dht.readTemperature(true);
  float humidity = dht.readHumidity();
  int soilMoisture = analogRead(SOIL_SENSOR);

  Serial.print("{\"temperature\":");

  if (isnan(temperature)) Serial.print("null");
  else Serial.print(temperature);

  Serial.print(",\"humidity\":");

  if (isnan(humidity)) Serial.print("null");
  else Serial.print(humidity);

  Serial.print(",\"soil_moisture\":");
  Serial.print(soilMoisture);

  Serial.print(",\"pump\":");
  Serial.print(pumpOn ? "true" : "false");

  Serial.print(",\"pump_duration\":");
  Serial.print(pumpDuration);

  Serial.println("}");
}
