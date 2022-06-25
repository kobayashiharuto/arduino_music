#include "pitches.h"

int inputMelody = 0;

void setup() {
  Serial.begin(9600);
}



void loop() {
  int inputData = Serial.read();
  if (inputData != -1) {
    inputMelody = inputData * 8;
  }

  if (inputMelody != 0) {
    tone(8, inputMelody, 100);
  }
}