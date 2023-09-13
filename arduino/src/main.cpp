#include <receiver.h>
#include <led_driver.h>
#include <Arduino.h>

void setup() {
  // Initialize serial connection.
  // Having serial on causes signal dropouts
  // Serial.begin(115200);
  setupReceiver();
  setupPixels();
}

struct BrightnessControl {
  uint8_t current_value = 0; 
};

void loop() {
    DataPacket receivedData;
    bool received = receiveData(receivedData);
    if (received) {
        // Serial.print("Setting pixels starting at: "); Serial.println(receivedData.starting_number);
        setPixelTargets(receivedData);
        setRampGain(receivedData.ramp_gain);
        // Serial.println("");
        // Serial.println(" ---- ");
        // Serial.print("Recieved: "); Serial.print(32); Serial.println(" bytes...");
        // Serial.print("Starting Number: "); Serial.println(receivedData.starting_number);
        // Serial.print("Brightness: "); Serial.println(receivedData.brightness);
        // for (int i = 0; i < 30; i += 3) {
        //   Serial.print("LED #"); Serial.print(i/3);
        //   Serial.print(" r: "); Serial.print(receivedData.rgb_list[i]);
        //   Serial.print(" g: "); Serial.print(receivedData.rgb_list[i+1]);
        //   Serial.print(" b: "); Serial.println(receivedData.rgb_list[i+2]);
        // }
        // Serial.println();
        // Serial.println(payload);  // print the payload's value
    }
    updatePixelColors();

}