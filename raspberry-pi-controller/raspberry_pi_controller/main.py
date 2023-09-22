from traceback import print_exc
import logging
import sys
import os

sys.path.append(os.path.abspath('/home/pi/repos/ex-machina-wall/raspberry-pi-controller/'))
from raspberry_pi_controller.led_panel import Panel


logging.basicConfig(filename='/home/pi/repos/ex-machina-wall/raspberry-pi-controller/log.txt',
                    filemode='a',
                    format='%(asctime)s-[%(name)s] [%(levelname)s] | %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
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
