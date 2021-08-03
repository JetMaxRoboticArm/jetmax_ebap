#!/usr/bin/env python3
# encoding: utf-8
import sys
import time
import smbus2
import threading

STEPPER_ADDRESS = 0x35


class Stepper:
    EN = 0x04
    SLEEP = 0x03
    RST = 0x01
    DIV_1 = 0
    DIV_1_2 = 1
    DIV_1_4 = 2
    DIV_1_8 = 3
    DIV_1_16 = 7

    def __init__(self, i2c_port):
        self.i2c_port = i2c_port
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 21, [self.DIV_1_4, ])

    def set_mode(self, mode):
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 20, [mode, ])

    def set_div(self, new_div):
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 21, [new_div, ])

    def go_home(self):
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 22, [1, ])

    def goto(self, steps):
        a = steps & 0xFF
        b = (steps >> 8) & 0xFF
        c = (steps >> 16) & 0xFF
        d = (steps >> 24) & 0xFF
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 24, [a, b, c, d, ])

    def set_speed(self, speed):
        a = speed & 0xFF
        b = (speed >> 8) & 0xFF
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(STEPPER_ADDRESS, 28, [a, b])

