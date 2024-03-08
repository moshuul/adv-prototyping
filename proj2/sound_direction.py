import os, sys, io
import M5
from M5 import *
from hardware import *
import time

# Global variables for IMU values
imu_x_val = 0.0
imu_y_val = 0.0
imu_x_last = 0.0
imu_y_last = 0.0

# Thresholds for detecting tilt
THRESHOLD_UP_DOWN = 0.5
THRESHOLD_LEFT_RIGHT = 0.5

# UI widgets
title0 = None
label0 = None
label1 = None
label2 = None
label3 = None

def setup():
    global title0, label0, label1, label2, label3
    M5.begin()
    title0 = Widgets.Title("IMU motion", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("tilt or move", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("up, down", 3, 40, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("left, right", 3, 60, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("--", 3, 80, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)

def send_command(command):
    # Placeholder for sending command to web interface
    print(command)  # Replace with actual send mechanism

def loop():
    global imu_x_val, imu_y_val, imu_x_last, imu_y_last
    M5.update()

    # Read the IMU accelerometer values
    imu_val = Imu.getAccel()
    imu_x_val, imu_y_val = imu_val[0], imu_val[1]

    if imu_x_val < -THRESHOLD_LEFT_RIGHT and imu_x_last >= -THRESHOLD_LEFT_RIGHT:
        # Tilt to the left detected, send command once
        label0.setText('RIGHT')
        send_command('RIGHT')
    elif imu_x_val > THRESHOLD_LEFT_RIGHT and imu_x_last <= THRESHOLD_LEFT_RIGHT:
        # Tilt to the right detected, send command once
        label0.setText('LEFT')
        send_command('LEFT')
    else:
        label0.setText('no X tilt')

    # Detect change in Y-axis tilt and send command if changed
    if imu_y_val < -THRESHOLD_UP_DOWN and imu_y_last >= -THRESHOLD_UP_DOWN:
        label1.setText('DOWN')
        send_command('DOWN')
    elif imu_y_val > THRESHOLD_UP_DOWN and imu_y_last <= THRESHOLD_UP_DOWN:
        label1.setText('UP')
        send_command('UP')
    else:
        label1.setText('no Y tilt')

    # Update last values for next comparison
    imu_x_last, imu_y_last = imu_x_val, imu_y_val

    # Sleep to prevent flooding the output
    time.sleep(0.1)

if __name__ == '__main__':
    setup()
    while True:
        loop()
