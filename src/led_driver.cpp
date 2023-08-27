#include <led_driver.h>

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

Pixel_S allPixels[NUMPIXELS];

void setupPixels(){
    pixels.begin();
};

void setPixelTargets(DataPacket &datapacket){
    // Get the starting led Number.
    uint8_t starting_number = datapacket.starting_number;

    uint8_t iter = 0;
    for (uint8_t i = starting_number; i < (starting_number + 10); i++){
        if (i < NUMPIXELS){
            uint8_t r = datapacket.rgb_list[iter];
            uint8_t g = datapacket.rgb_list[iter+1];
            uint8_t b = datapacket.rgb_list[iter+2];
            iter+=3;
            setPixelTarget(&allPixels[i], r, g, b);
            Serial.print("Setting pixel target: r"); 
            Serial.print(r); Serial.print(" g"); Serial.print(g); Serial.print(" b"); Serial.println(b);
        }
    }
};

void setPixelTarget(Pixel_S *pixel, uint8_t r_new, uint8_t g_new, uint8_t b_new){
    pixel->r_target = r_new;
    pixel->g_target = g_new;
    pixel->b_target = b_new;
};

void updatePixelColors(){
    for (uint8_t i = 0; i < NUMPIXELS; i++){
        iterPixel(&allPixels[i]);
    }
    for (uint8_t i = 0; i < NUMPIXELS; i++){
        pixels.setPixelColor(i, allPixels[i].r, allPixels[i].g, allPixels[i].b);
    }
    pixels.show();
};

void iterPixel(Pixel_S *pixel){
    if (pixel->r < pixel->r_target){
        pixel->r++;
    } else if (pixel->r > pixel->r_target){
        pixel->r--;
    }

    if (pixel->g < pixel->g_target){
        pixel->g++;
    } else if (pixel->g > pixel->g_target){
        pixel->g--;
    }
    
    if (pixel->b < pixel->b_target){
        pixel->b++;
    } else if (pixel->b > pixel->g_target){
        pixel->b--;
    }
}
