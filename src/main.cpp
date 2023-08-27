#include <RF24.h>

#define PIN_RF24_CSN             8            // CSN PIN for RF24 module.
#define PIN_RF24_CE              7            // CE PIN for RF24 module.

#define NRF24_CHANNEL            100          // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_PA_LEVEL           RF24_PA_MIN  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX    

                             
// Cretate NRF24L01 radio.
RF24 radio(PIN_RF24_CE, PIN_RF24_CSN);

struct DataPacket {
    uint8_t starting_number;
    uint8_t brightness;
    uint8_t rgb_list[30];
};

byte rf24_tx[6] = "RAPI";     // Address used when transmitting data.
byte rf24_rx[6] = "EXWLL";    // Address used when receiving data

void setup() {
  
  // Initialize serial connection.
  Serial.begin(115200);
  
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
  radio.openReadingPipe(1, rf24_rx);
  radio.startListening();  
  radio.printDetails();
  Serial.println("Configuration complete! Listening...");
}

void loop() {
  uint8_t pipe;
  if (radio.available(&pipe)) {              // is there a payload? get the pipe number that recieved it

    uint8_t bytes = radio.getPayloadSize();  // get the size of the payload
    byte payload[32];             // Payload bytes. Used both for transmitting and receiving
    radio.read(&payload, bytes);             // fetch payload from FIFO
    DataPacket receivedData;
    memcpy(&receivedData, payload, bytes);
    Serial.print("Recieved: "); Serial.print(sizeof(bytes)); Serial.println(" bytes...");
    Serial.print("Starting Number: "); Serial.println(receivedData.starting_number);
    Serial.print("Brightness: "); Serial.println(receivedData.brightness);
    for (int i = 0; i < 30; i += 3) {
      Serial.print("LED #"); Serial.print(i/3);
      Serial.print(" r: "); Serial.print(receivedData.rgb_list[i]);
      Serial.print(" g: "); Serial.print(receivedData.rgb_list[i+1]);
      Serial.print(" b: "); Serial.println(receivedData.rgb_list[i+2]);
    }
    Serial.println();
    // Serial.println(payload);  // print the payload's value
  }
}