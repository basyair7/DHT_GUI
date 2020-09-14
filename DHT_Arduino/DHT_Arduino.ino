/* Name Project : DHT for python
 * Code Pr0ject : *
 * Version      : v 1.1
 * By @Ahul07
 */

/* Before verify/upload, don't forget to install the libraries
 *  go to sketch >> Include Library >> Add .ZIP File >> Select the Downloaded ZIP fiels From the Above links
 */
 
/*
 ************************************************************************************************************** 
 * Credit : Thanks Allah SWT., Nabi Muhammad SAW., Thanks My Mother & My Father, Thanks My Brother; and Thank * 
 *          you My Friends from Electrical Engineering'19 USK, Syiah Kuala University                         *
 *                                                                                                            *
 **************************************************************************************************************          
 */ 
 
#include <DHT.h> 

#define DHTPIN 4 // Digital pin connected to the DHT sensor

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);

void setup(){
  Serial.begin(9600);
  dht.begin();
}

void loop(){
  float celcius = dht.readTemperature(); // Read temperature as Celsius (the default)
  float humidity = dht.readHumidity();
  float fahrenheit = dht.readTemperature(true); // Read temperature as Fahrenheit (isFahrenheit = true)

  // Check if any reads failed and exit early (to try again).
  if (isnan(celcius) || isnan(humidity) || isnan(fahrenheit)){
    Serial.print("Humidity: 0% ");
    Serial.println("Temperature: 0°C (0°F)");
    delay(2000);
    return 0;
  }
  
  // Humidity
  Serial.print("Humidity : ");
  Serial.print(humidity);
  Serial.print("% ");
  // Temperature
  Serial.print("Temperature : ");
  // Celcius
  Serial.print(celcius);
  Serial.print("°C (");
  // Fahrenheit
  Serial.print(fahrenheit);
  Serial.println("°F)");
  //delay(1200000); //20 minutes = 1200000ms
  delay(2000); // 2 seconds
  
}
