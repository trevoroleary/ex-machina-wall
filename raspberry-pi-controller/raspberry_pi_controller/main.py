from traceback import print_exc
import logging
import sys
import os

sys.path.append(os.path.abspath('/home/pi/repos/ex-machina-wall/raspberry-pi-controller/'))
from raspberry_pi_controller.led_panel import Panel

logging.basicConfig(level=logging.DEBUG, format="[%(module)s] %(message)s")

def main():
    logging.info(f"Starting Program..")
    panel = Panel()
    try:  
        panel.run()
    except Exception as e:
        logging.error(e)
        print_exc()
        panel.power_down()
        

if __name__ == "__main__":
    main()
