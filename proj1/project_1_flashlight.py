import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from random import randint

pin_label = None
program_state_label = None

input_pin = None
input_value = 0
input_timer = 0
button_value = None
pin41 = None
moshuu = None
button = None
label0 = None

program_state = 'START'

def setup():
    global pin_label, program_state_label, input_pin
    global rgb2, i
    global pin41

    M5.begin()
    pin41 = Pin(41, mode=Pin.IN)
    moshuu = M5.Widgets.Title("moshuu@liu", 3, 0x6b3131, 0xffd4fa, M5.Widgets.FONTS.DejaVu18)
    pin_label = M5.Widgets.Label("input", 50, 20, 1.0, 0xffff66, 0x000000, M5.Widgets.FONTS.DejaVu18)
    button = M5.Widgets.Circle(62, 62, 15, 0xd6c2f8, 0xffb9fa)
    label0 = M5.Widgets.Label("press to change color", 0, 87, 1.0, 0xffffff, 0x222222, M5.Widgets.FONTS.DejaVu9)
    program_state_label = M5.Widgets.Label("", 50, 105, 1.0, 0xffff66, 0x000000, M5.Widgets.FONTS.DejaVu18)
    input_pin = Pin(1, mode=Pin.IN, pull=Pin.PULL_UP)
    rgb2 = RGB(io=38, n=10, type="SK6812")

def loop():
    global pin_label, program_state_label
    global input_value
    global input_timer
    global program_state
    global rgb2, i
    global moshuu, button, label0, random

    M5.update()

    if time.ticks_ms() > input_timer + 400:
        input_timer = time.ticks_ms()
        input_value = input_pin.value()

        if input_value == 0:
            pin_label.setText('0_0')
            rgb2.fill_color(0xffff66)
            if pin41.value() == 0:  # Check if the button connected to pin 41 is pressed
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                for i in range(10):  # Assuming you have 14 LEDs in your strip
                    rgb2.set_color(i, (r << 16) | (g << 8) | b)
                time.sleep_ms(20)

        else:
            pin_label.setText('-_-')
            rgb2.fill_color(0x000000)

        if program_state == 'START' and input_value == 0:
            program_state = 'RUN'  
            program_state_label.setText('***')

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
