#ifndef _FUNCTIONS_H_
#define _FUNCTIONS_H_
#include "Arduino.h"

// INIT
void init();

// CONFIG SET UP
void wifiConfig();
void pinConfig();
void serverConfig();

// CONTROL CAR FUNCTION
void up();
void down();
void left();
void right();
void stop();


// LOOP
void serverHandler();

#endif