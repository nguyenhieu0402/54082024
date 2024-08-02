#include "functions.h"

void setup()
{
    Serial.begin(115200);
    init();
}

void loop() 
{
    serverHandler();
}