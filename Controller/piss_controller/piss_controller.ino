#include <DHT.h>

#define DHT_PIN 4
#define SOIL_PIN 15
#define PUMP_PIN 2
#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature(true);
  float humidity = dht.readHumidity();
  float soilMoisture = analogRead(SOIL_PIN);

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" F | Humidity: ");
  Serial.print(humidity);
  Serial.println("%");
  Serial.print("Soil Moisture: ");
  Serial.println(soilMoisture);
}
