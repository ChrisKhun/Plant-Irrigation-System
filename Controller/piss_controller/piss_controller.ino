#include <DHT.h>

#define DHTPIN 15
#define SOIL_PIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("DHT11 Sensor Test");
}

void loop() {
  float temperature = dht.readTemperature(true);
  float humidity = dht.readHumidity();
  float soilMoisture = analogRead(SOIL_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT11!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" F | Humidity: ");
    Serial.print(humidity);
    Serial.println("%");
    Serial.print("Soil Moisture: ");
    Serial.println(soilMoisture);
  }

  delay(2000);
}