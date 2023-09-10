from raspberry_pi_controller.led_panel import Panel
from traceback import print_exc

def main():
    panel = Panel()
    # try:  
    panel.run()
    # except:
        # print_exc()
        # panel.power_down()

if __name__ == "__main__":
    main()
