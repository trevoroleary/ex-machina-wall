import argparse
from datetime import datetime
import struct
import sys
import time
import traceback
from random import normalvariate, randint
import pigpio
from nrf24 import *
import os
import logging


class LEDPacket:
    def __init__(self, starting_number: int, ramp_rate: int, led_rgbs: list):
        self.logger = logging.getLogger("LEDPacket")
        self.starting_number = starting_number
        self.ramp_rate = ramp_rate
        self.led_rgbs = led_rgbs
    
    def get_payload(self) -> bytes:
        string_format = "@" + "".join(["B" for _ in range(32)])
        
        led_rgb_list = list()
        # print(f"Starting Number: {self.starting_number}")
        # print(f"Ramp Rate: {self.ramp_rate}")
        for i, (r, g, b) in enumerate(self.led_rgbs):
            led_rgb_list += [r, g, b]
            # print(f"LED #{i}   |   r: {r}, g: {g}, b: {b}")
        args = [self.starting_number, self.ramp_rate] + led_rgb_list
        payload = struct.pack(string_format, *args)
        return payload

class Transmitter:
    RADIO_CHIP_SELECT = 25
    RADIO_CHANNEL = 0
    RADIO_PAYLOAD = RF24_PAYLOAD.DYNAMIC
    RADIO_DATA_RATE = RF24_DATA_RATE.RATE_250KBPS
    RADIO_PA = RF24_PA.HIGH
    RADIO_RX_ADDRESS = "RAPI"
    RADIO_TX_ADDRESS = "EXWLL"

    PIGPIO_HOSTNAME = 'localhost'
    PIGPIO_PORT = 8888

    def __init__(self):
        self.logger = logging.getLogger("Transmitter")
        self.pi_gpios = pigpio.pi(
            self.PIGPIO_HOSTNAME, 
            self.PIGPIO_PORT
            )
        if not self.pi_gpios.connected:
            self.logger.error("Not connected to Raspberry Pi ... goodbye.")
            sys.exit()
        
        # Create NRF24 object.
        # PLEASE NOTE: if PA level is set to MIN, its because test sender/receivers are often 
        # close to each other, and then MIN works better.
        self.radio = NRF24(
            self.pi_gpios, 
            ce=self.RADIO_CHIP_SELECT, 
            payload_size=self.RADIO_PAYLOAD, 
            channel=self.RADIO_CHANNEL, 
            data_rate=self.RADIO_DATA_RATE, 
            pa_level=self.RADIO_PA
            )
        self.radio.set_address_bytes(len(self.RADIO_TX_ADDRESS))

        # Write to the specified address
        self.radio.open_writing_pipe(self.RADIO_TX_ADDRESS)
        
        # Display the content of NRF24L01 device registers.
        self.radio.show_registers()    
        pass

    def send_packet(self, led_packet: LEDPacket):
        # Send the payload to the address specified above.
        payload = led_packet.get_payload()
        # self.radio.reset_packages_lost()
        self.radio.send(payload)
        try:
            self.radio.wait_until_sent()
            
        except TimeoutError:
            print("Timeout waiting for transmission to complete.")
            time.sleep(10)
            return
        if self.radio.get_retries() == 0:
            # print(f"Success: lost={self.radio.get_packages_lost()}, retries={self.radio.get_retries()}")
            pass
        else:
            # self.logger.error(f"Error: lost={self.radio.get_packages_lost()}, retries={self.radio.get_retries()}")
            pass

    def power_down(self):
        self.pi_gpios.stop()
        # self.radio.power_down()

def rand_int(base_color: int):
    value = int(normalvariate(base_color, 100))
    if value < 0:
        value = 0
    if value > 255:
        value = 255
    return value
