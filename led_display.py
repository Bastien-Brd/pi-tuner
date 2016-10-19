import math
from gpiozero import LED
from time import sleep


g0 = LED(12)
f0 = LED(16)
a0 = LED(20)
b0 = LED(21)
e0 = LED(17)
d0 = LED(27)
c0 = LED(22)

g1 = LED(25)
f1 = LED(24)
a1 = LED(23)
b1 = LED(18)
e1 = LED(5)
d1 = LED(6)
c1 = LED(13)

PITCHES = {
    'E2': ((a0, d0, e0, f0, g0), (b0, c0)),
    'A2': ((a0, b0, c0, e0, f0, g0), (d0, )),
    'D3': ((b0, c0, d0, e0, g0), (a0, f0,)),
    'G3': ((a0, b0, c0, d0, f0, g0), (e0, )),
    'B3': ((c0, d0, e0, f0, g0), (a0, b0,)),
    'E4': ((a0, d0, e0, f0, g0), (b0, c0)),
}

DIRECTIONS = {
    -1: ((a1, b1, g1, f1,), (c1, d1, e1,)),
    0: ((g1, ), (a1, b1, c1, d1, e1, f1, )),
    1: ((c1, d1, e1, g1), (a1, b1, f1)),
}

def display_tuning_guidance(pitch, direction, duration=1):
    leds_on = PITCHES[pitch][0]
    leds_off = PITCHES[pitch][1] + DIRECTIONS[direction][1]
    animated_leds = DIRECTIONS[direction][0]
    # Turn the appropriate leds on or off
    for led in leds_on:
        led.off()
    for led in leds_off:
        led.on()
    timer = duration
    while timer > 0:
        for led in animated_leds:
            led.on()
            map(lambda x: x.off(), [l for l in animated_leds if l != led])
            sleep(duration/8.0)
        timer -= duration/2.0
            
        

