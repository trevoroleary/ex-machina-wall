#include <RF24.h>

#define PIN_RF24_CSN             8            // CSN PIN for RF24 module.
#define PIN_RF24_CE              7            // CE PIN for RF24 module.

#define NRF24_CHANNEL          100            // 0 ... 125
#define NRF24_CRC_LENGTH         RF24_CRC_16  // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE          RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_DYNAMIC_PAYLOAD    1
#define NRF24_PAYLOAD_SIZE      32            // Max. 32 bytes.
#define NRF24_PA_LEVEL           RF24_PA_MIN  // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX    
#define NRF24_RETRY_DELAY        5            // Delay bewteen retries, 1..15.  Multiples of 250µs.
#define NRF24_RETRY_COUNT       15            // Number of retries, 1..15.

#define PROTOCOL 0x01                         // 0x01 (byte), temperature (float), humidity (float)
                                              // Python 1: "<Bff"
                             
// Cretate NRF24L01 radio.
RF24 radio(PIN_RF24_CE, PIN_RF24_CSN);


byte rf24_tx[6] = "EXWLL";    // Address used when transmitting data.
byte payload[32];             // Payload bytes. Used both for transmitting and receiving

unsigned long last_reading;                // Milliseconds since last measurement was read.
unsigned long ms_between_reads = 2000;    // 10000 ms = 10 seconds

void setup() {
  
  // Initialize serial connection.
  Serial.begin(115200);
  delay(1000);
  
  // Show that program is starting.
  Serial.println("\n\nNRF24L01 Arduino Simple Sender.");

  // Configure the NRF24 tranceiver.
  Serial.println("Configure NRF24 ...");
  if (!radio.begin()) {
    Serial.println(F("radio hardware not responding!!"));
    while (1) {} // hold program in infinite loop to prevent subsequent errors
  }
  radio.enableDynamicPayloads();
  radio.setAutoAck(true);
  radio.setPALevel(NRF24_PA_LEVEL);
  radio.setRetries(NRF24_RETRY_DELAY, NRF24_RETRY_COUNT);    
  radio.setDataRate(NRF24_DATA_RATE);          
  radio.setChannel(NRF24_CHANNEL);
  radio.setCRCLength(NRF24_CRC_LENGTH);
  radio.setPayloadSize(NRF24_PAYLOAD_SIZE);
  radio.openWritingPipe(rf24_tx);  
  radio.startListening();
  
  // Show debug information for NRF24 tranceiver.
  radio.printDetails();
  
  // Take the current timestamp. This means that the next (first) measurement will be read and
  // transmitted in "ms_between_reads" milliseconds.
  last_reading = 0;
}

void loop() {
unsigned int cmd;
  boolean relay;

  radio.startListening();
  // Wait here until we get a response, or timeout
  unsigned long started_waiting_at = millis();
  bool timeout = false;
  while (!radio.available() && !timeout) {
    if (millis() - started_waiting_at > 500 ) {
      timeout = true;
    }
  }

  if (timeout) {
    Serial.println("Timeout waiting for response.");
    return;
  }

  uint8_t plen = radio.getDynamicPayloadSize();
  radio.read(&payload, plen);

  // Extract command from payload
  memcpy(&cmd, payload, sizeof(cmd));
  Serial.print("Response: cmd="); Serial.println(cmd);
    
  if (cmd == 0x01) {
    // Response to command #1.
    Serial.print("Response #1: uuid=");
    print_bytes(payload, 2, 16);
    Serial.println();
  }
  else if (cmd == 0x02) {
    // Response to command #2.
    Serial.print("Response #2: relay=");
    memcpy(&relay, payload + 2, sizeof(relay));  
    Serial.println(relay);    
  }
  else {
    // We process only responses to command 0x01 (get uuid) and 0x02 (get relay state).
    Serial.print(">>> BAD response received: "); Serial.println(cmd);
  }
}


