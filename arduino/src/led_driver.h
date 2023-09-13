
#ifndef LED_DRIVER_H
#define LED_DRIVER_H

#include <Adafruit_NeoPixel.h>
#include <receiver.h>

#define PIN        6
#define NUMPIXELS 73

struct Pixel_S {
    uint8_t r_target;
    uint8_t g_target;
    uint8_t b_target;
    uint8_t r;
    uint8_t g;
    uint8_t b;
};


// Define the functions
void setupPixels();
void setPixelTarget(Pixel_S *pixel, uint8_t r_new, uint8_t g_new, uint8_t b_new);
void setPixelTargets(DataPacket &dataPacket);
void setRampGain(int new_gain);
void updatePixelColors();
void iterPixel(Pixel_S *pixel);

#endif // RECEIVER_H