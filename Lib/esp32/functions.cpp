#include "functions.h"
#include "config.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>

WiFiServer server(client_port);

// INIT
void init()
{
    wifiConfig();
    pinConfig();
    serverConfig();
}

// CONFIG SET UP
void wifiConfig()
{
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    Serial.println(WiFi.localIP());
}

void pinConfig()
{
    pinMode(MOTOR_1, OUTPUT);
    pinMode(MOTOR_2, OUTPUT);
    pinMode(MOTOR_3, OUTPUT);
    pinMode(MOTOR_4, OUTPUT);
}

void serverConfig()
{
  server.begin();
}



// CONTROL CAR FUNCTION
void up()
{
    Serial.println("1");
}

void down()
{
    Serial.println("2");
}

void left()
{
    Serial.println("3");
}

void right()
{
    Serial.println("4");
}

void stop()
{
    Serial.println("5");
}




//LOOP
void serverHandler()
{
    WiFiClient client = server.available();  // Lắng nghe các kết nối đến
    if (client) 
    {
        Serial.println("New Client Connected.");
        if (client.connected()) 
        {
          if (client.available())
          {
              String data = client.readStringUntil('\n');
              Serial.println("Received from client: " + data);
          }
        }
        else
        {
            client.stop();
        }
        Serial.println("Client Disconnected.");
    }
}