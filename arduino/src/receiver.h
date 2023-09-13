// receiver.h

// Include guards to prevent multiple inclusion
#ifndef RECEIVER_H
#define RECEIVER_H

// Include necessary libraries or other headers
#include <Arduino.h>
#include <RF24.h>

#define PIN_RF24_CSN             8            // CSN PIN for RF24 module.
#define PIN_RF24_CE              7            // CE PIN for RF24 module.
#define NRF24_CHANNEL            0          // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_PA_LEVEL           RF24_PA_MAX  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX    

// Define your struct
struct DataPacket {
    uint8_t starting_number;
    uint8_t ramp_gain;
    uint8_t rgb_list[30];
};

// Declare your functions
void setupReceiver();
bool receiveData(DataPacket &data);

#endif // RECEIVER_H