#include <SPI.h>
#include <WiFi.h>
#include "ConnectNoEncryption.ino"
#include "ConnectWithWEP.ino"
#include "ConnectWithWPA.ino"
#include "ScanNetworks.ino"
#include "SimpleWebServerWiFi.ino"
#include "WiFiChatServer.ino"
#include "WiFiUdpNtpClient.ino"
#include "WiFiUdpSendReceiveString.ino"
#include "WiFiWebClient.ino"
#include "WiFiWebClientRepeating.ino"
#include "WiFiWebServer.ino"

void loop() {
    // check the network connection once every 10 seconds:
    delay(10000);
    printCurrentNet();
}

void ConnectWithWEP(char ssid[], char key[], int keyIndex, int status){
    //Initialize serial and wait for port to open:
    Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
    }

    // check for the presence of the shield:
    if (WiFi.status() == WL_NO_SHIELD) {
      Serial.println("WiFi shield not present");
      // don't continue:
      while (true);
    }

    String fv = WiFi.firmwareVersion();
    if (fv != "1.1.0") {
      Serial.println("Please upgrade the firmware");
    }

    // attempt to connect to Wifi network:
    while (status != WL_CONNECTED) {
      Serial.print("Attempting to connect to WEP network, SSID: ");
      Serial.println(ssid);
      status = WiFi.begin(ssid, keyIndex, key);

      // wait 10 seconds for connection:
      delay(10000);
    }

    // once you are connected :
    Serial.print("You're connected to the network");
    printCurrentNet();
    printWifiData();
}

void ConnectNoEncryption(char ssid[], int status){
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv != "1.1.0") {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to open SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  printCurrentNet();
  printWifiData();
}
