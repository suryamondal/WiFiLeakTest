
 
#include <Time.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

int station = 1;

const int wifiNo = 3;
const String ssids[wifiNo] = {"iichep1_ng","iichep2_ng","iichep3_ng"};
const String passwords[wifiNo] = {"xxxxxx","yyyyyyy","zzzzzzz"};

uint16_t udpPort = 5006;
IPAddress ipAddress(192,168,183,121);

int displayInterval = 3;

Adafruit_BMP085 pressure;
WiFiUDP Udp;

int statusBMP;
unsigned long t_times;
int timestop = 0;

void setup()  {
  Serial.begin(9600);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  delay(2000);
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  char ssid[20];
  char password[20];

  while(1) {
    int nwifi = WiFi.scanNetworks();
    String sssid = "";
    String spassword = "";
    String tssid;
    int stren = -999;
    for (int ij = 0; ij < nwifi; ij++) {
      tssid = WiFi.SSID(ij);
      int tstren = WiFi.RSSI(ij);
      for (int jk = 0; jk < wifiNo; jk++) {
        if(tssid == ssids[jk] && tstren<0) {
          if(stren<tstren) { 
            sssid = tssid;
            stren = tstren;
            spassword = passwords[jk];
          } 
        }
      } // for (int jk = 0; jk < wifiNo; jk++) {
      delay(10);
    } // for (int ij = 0; ij < nwifi; ij++) {
    if(sssid!="") {
      sssid.toCharArray(ssid,20); 
      spassword.toCharArray(password,20);
      break;
    }
  } // while(1) {

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid,password);
  while(WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.println(".");
  }
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  
  statusBMP = pressure.begin();
  if(!statusBMP) {while(1) {Serial.println("Wrong BMP180 Connection");}}
}

void loop(){

  t_times = millis()/1000;
  
  if(t_times%displayInterval==0) {
    if(timestop==0) {

      double Temp = pressure.readTemperature();
      double Press = pressure.readPressure();

      char tempChar[100];
      sprintf(tempChar,"%i %.2f %.1f\n",station,Temp,Press);
      Serial.print(tempChar);

      if(WiFi.RSSI()<-90 || WiFi.status()!=WL_CONNECTED) {ESP.reset();}

      statusBMP = Udp.beginPacket(ipAddress,udpPort);
      statusBMP = Udp.write(tempChar);
      Udp.endPacket();
      
      timestop = 1;
    } // if(timestop==0) {
  } // if(t_times%5==0) {
  else{timestop = 0;}
} // void loop(){
