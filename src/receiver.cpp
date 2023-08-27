// receiver.cpp

#include "receiver.h"

RF24 radio(PIN_RF24_CE, PIN_RF24_CSN);

void setupReceiver() {
    
    // Let the Serial connection 'start'
    delay(1000);
    
    // Show that program is starting.
    Serial.println("\n -- Ex Machina Wall --");

    // Configure the NRF24 tranceiver.
    Serial.println("Configuring NRF24 ...");
    if (!radio.begin()) {
        Serial.println("radio hardware not responding!!");
        while (1) {} // hold program in infinite loop to prevent subsequent errors
    }
    radio.setAutoAck(true);
    radio.setPALevel(NRF24_PA_LEVEL);
    radio.setDataRate(NRF24_DATA_RATE);          
    radio.setChannel(NRF24_CHANNEL);
    radio.setCRCLength(NRF24_CRC_LENGTH);  
    radio.enableAckPayload();

    // If sending data enable this
    // radio.openWritingPipe(rf24_tx);

    // We are reading data so just open a reading pipe  
    byte rf24_rx[6] = "EXWLL";    // Address used when receiving data
    radio.openReadingPipe(1, rf24_rx);
    radio.startListening();  
    radio.printDetails();
    Serial.println("Configuration complete! Listening...");
}

bool receiveData(DataPacket &receivedData) {
    // Your data receiving and unpacking code here
    uint8_t pipe;
    byte payload[32];                               // Payload bytes. Used both for transmitting and receiving
    if (radio.available(&pipe)) {                   // is there a payload? get the pipe number that recieved it

        // get the size of the payload
        uint8_t bytes = radio.getPayloadSize();     
        
        // fetch payload from FIFO
        radio.read(&payload, bytes);                
        memcpy(&receivedData, payload, 32);
        return true;
    } else {
        return false;
    }
}