import time

from segment_manager import SegmentManager
from enums import SPEED, COLORS, ColorGenerator

led_manager = SegmentManager()

led_manager.call_on_all(func_name='set_all', kwargs={"color": COLORS.BLUE})
time.sleep(SPEED.SLOWER.value)

led_manager.call_on_all(func_name='set_all', kwargs={"color": COLORS.RED})
time.sleep(SPEED.SLOWER.value)

if True:
    # Flash
    for i in range(10):
        led_manager.call_on_all(func_name='set_all', kwargs={'color': COLORS.RED_BLUE})
        time.sleep(SPEED.SLOW.value)
        led_manager.call_on_all(func_name='set_all', kwargs={'color': COLORS.OFF})
        time.sleep(SPEED.FAST.value)

    for i in range(100):
        led_manager.call_on_all(func_name='sync_sweep_right', kwargs={'percentage': i, 'color_on': COLORS.RED_BLUE, 'color_off': COLORS.OFF})

    for i in range(100):
        led_manager.call_on_all(func_name='sync_sweep_left', kwargs={'percentage': i, 'color_on': COLORS.RED_BLUE, 'color_off': COLORS.OFF})

    # Sweep Back and Forth
    for i in range(120):
        led_manager.call_on_all(func_name='sweep_right', kwargs={'iter_number': i, 'color_on': COLORS.RED_BLUE, 'color_off': COLORS.OFF})
        time.sleep(SPEED.FAST.value)

    for i in range(20):
        led_manager.call_on_all(func_name='sweep_right', kwargs={'iter_number': i, 'color_on': COLORS.OFF, 'color_off': COLORS.RED_BLUE})
        time.sleep(SPEED.FASTEST.value)

    for i in range(20):
        led_manager.call_on_all(func_name='sweep_left', kwargs={'iter_number': i, 'color_on': COLORS.RED_BLUE, 'color_off': COLORS.OFF})
        time.sleep(SPEED.FASTEST.value)


# Skip Some Moving Across Line
for i in range(50):
    led_manager.call_on_all(func_name='skip_some', kwargs={'iter_number': i, 'skip_length': 8, 'color_on': COLORS.BLUE, 'color_off': COLORS.OFF})
    time.sleep(SPEED.FAST.value)

led_manager.wheel_around(SPEED.FAST.value)

led_manager.call_on_all('set_all', kwargs={'color': COLORS.GREEN})

led_manager.sweep_colors(multiplier=50)

led_manager.call_on_all('set_all', kwargs={'color': COLORS.OFF})
