
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// ---------------------------------------------------------------------------
// Configuration
//
// When uploaded via upload-nodemcu.py, a config.h is generated automatically
// with station-specific values and USE_CONFIG_H is defined at compile time.
//
// For manual upload through Arduino IDE, edit the defaults below instead.
// ---------------------------------------------------------------------------
#ifdef USE_CONFIG_H
  #include "config.h"
#else
  // --- Edit these for manual Arduino IDE upload ---
  #define STATION_ID       0
  #define UDP_PORT         5006
  #define DISPLAY_INTERVAL 3

  static const char* const _ssids[]     = {"your_wifi_ssid"};
  static const char* const _passwords[] = {"your_wifi_password"};
  static const int         WIFI_NO      = 1;
  static const char* const UDP_IP_STR   = "192.168.1.100";
  // ------------------------------------------------
#endif

const int      station         = STATION_ID;
const uint16_t udpPort         = UDP_PORT;
const int      displayInterval = DISPLAY_INTERVAL;

Adafruit_BMP085 pressure;
WiFiUDP Udp;

int           statusBMP;
unsigned long t_times;
int           timestop = 0;

// Connect to the strongest available WiFi from the configured list.
// Blocks until a connection is established.
void connectWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  while (1) {
    int nwifi = WiFi.scanNetworks();
    const char* bestSsid = nullptr;
    const char* bestPass = nullptr;
    int         bestRssi = -999;

    for (int i = 0; i < nwifi; i++) {
      String scanned = WiFi.SSID(i);
      int    rssi    = WiFi.RSSI(i);
      for (int j = 0; j < WIFI_NO; j++) {
        if (scanned == _ssids[j] && rssi < 0 && rssi > bestRssi) {
          bestRssi = rssi;
          bestSsid = _ssids[j];
          bestPass = _passwords[j];
        }
      }
      delay(10);
    }

    if (bestSsid != nullptr) {
      Serial.print("Connecting to ");
      Serial.println(bestSsid);
      WiFi.begin(bestSsid, bestPass);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println();
      Serial.print("IP: ");
      Serial.println(WiFi.localIP());
      return;
    }
  }
}

void setup() {
  Serial.begin(9600);
  delay(2000);

  connectWifi();

  statusBMP = pressure.begin();
  if (!statusBMP) {
    while (1) { Serial.println("Wrong BMP180 Connection"); }
  }
}

void loop() {
  t_times = millis() / 1000;

  if (t_times % displayInterval == 0) {
    if (timestop == 0) {
      double Temp  = pressure.readTemperature();
      double Press = pressure.readPressure();

      char tempChar[100];
      sprintf(tempChar, "%i %.2f %.1f\n", station, Temp, Press);
      Serial.print(tempChar);

      // Reset if WiFi signal is too weak or connection dropped
      if (WiFi.RSSI() < -90 || WiFi.status() != WL_CONNECTED) { ESP.reset(); }

      Udp.beginPacket(UDP_IP_STR, udpPort);
      Udp.write(tempChar);
      Udp.endPacket();

      timestop = 1;
    }
  } else {
    timestop = 0;
  }
}
