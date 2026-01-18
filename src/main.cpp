#include <Arduino.h>
#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    16
#define BRIGHTNESS  255
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define MATRIX_HEIGHT 4
#define MATRIX_LENGTH 4

byte led_mode;
bool waiting_for_conf = true;
byte led_counter = 0;

byte led_bit_counter;
byte led_conf[5]; //for x, y coords and colours 

void setLED_by_coord(byte conf[5]) {
  int x = conf[0];
  int y = conf[1];

  int led_index;
  if (y % 2 == 0) {
    led_index = y * MATRIX_HEIGHT + (MATRIX_LENGTH - 1)  - (x % MATRIX_LENGTH);
  } else {
    led_index = y * MATRIX_HEIGHT + (x % MATRIX_LENGTH);
  }
  leds[led_index] = CRGB((int)conf[2], (int)conf[3] , (int)conf[4]);
}

void setup() {
  // Initialize serial communication over USB
  Serial.begin(115200); 

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  FastLED.show();

}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();

    if (waiting_for_conf) {
      led_mode = incomingByte;
      int led_to_num_configure = led_mode;
      if (led_to_num_configure > NUM_LEDS || led_to_num_configure == 0){
        Serial.printf("Invalid configuration, min LED num is 1, max is %i, sent: %i", NUM_LEDS, led_to_num_configure);        
      } else {
        led_counter = 0;
        waiting_for_conf = false;
        led_bit_counter = 0;
        Serial.println("Reading configuration");
        Serial.printf("number of led configured: %i\n", led_to_num_configure);
    }
    } else {
        if (led_bit_counter < 4) {
        led_conf[led_bit_counter] = incomingByte;
        led_bit_counter++;
        } else {
          led_conf[led_bit_counter] = incomingByte; // for the last byte comming
          setLED_by_coord(led_conf);
          led_counter++;
          led_bit_counter = 0;
          Serial.printf("LED %i configured\n", led_counter);
          if (led_counter >= ((led_mode << 2) >> 2)){
            Serial.println("Configuration recived.");
            FastLED.show();
            FastLED.clear();
            waiting_for_conf = true;
          }
        }
    }
  }
}
