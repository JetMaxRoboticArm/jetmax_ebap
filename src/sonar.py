import os
import sys
import time
from smbus2 import SMBus, i2c_msg


class Sonar:
    __units = {"mm":0, "cm":1}
    __dist_reg = 0

    __RGB_MODE = 2
    __RGB1_R = 3
    __RGB1_G = 4
    __RGB1_B = 5
    __RGB2_R = 6
    __RGB2_G = 7
    __RGB2_B = 8

    __RGB1_R_BREATHING_CYCLE = 9
    __RGB1_G_BREATHING_CYCLE = 10
    __RGB1_B_BREATHING_CYCLE = 11
    __RGB2_R_BREATHING_CYCLE = 12
    __RGB2_G_BREATHING_CYCLE = 13
    __RGB2_B_BREATHING_CYCLE = 14
    def __init__(self):
        self.i2c_addr = 0x77
        self.i2c = 1
        self.Pixels = [0,0]
        self.RGBMode = 0

    def __getattr(self, attr):
        if attr in self.__units:
            return self.__units[attr]
        if attr == "Distance":
            return self.getDistance()
        else:
            raise AttributeError('Unknow attribute : %s'%attr)

    def set_rgb_mode(self, mode):
        with SMBus(self.i2c) as bus:
            try:
                bus.write_byte_data(self.i2c_addr, self.__RGB_MODE, mode)
            except:
                pass

    def set_color(self, index, rgb):
        if index != 0 and index != 1:
            return 
        start_reg = 3 if index == 0 else 6
        with SMBus(self.i2c) as bus:
            try:
                bus.write_byte_data(self.i2c_addr, start_reg, 0xFF & (rgb >> 16))
                bus.write_byte_data(self.i2c_addr, start_reg+1, 0xFF & (rgb >> 8))
                bus.write_byte_data(self.i2c_addr, start_reg+2, 0xFF & rgb)
                self.Pixels[index] = rgb
            except:
                pass

    def get_color(self, index):
        if index != 0 and index != 1:
            raise ValueError("Invalid pixel index", index)
        return ((self.Pixels[index] >> 16) & 0xFF,
                (self.Pixels[index] >> 8) & 0xFF,
                self.Pixels[index] & 0xFF)

    def set_breath_cycle(self, index, rgb, cycle):
        if index != 0 and index != 1:
            return
        if rgb < 0 or rgb > 2:
            return
        start_reg = 9 if index == 0 else 12
        cycle = int(cycle / 100)
        with SMBus(self.i2c) as bus:
            try:
                bus.write_byte_data(self.i2c_addr, start_reg + rgb, cycle)
            except:
                pass

    def start_symphony(self):
        self.set_rgb_mode(1)
        self.set_breath_cycle(1,0, 2000)
        self.set_breath_cycle(1,1, 3300)
        self.set_breath_cycle(1,2, 4700)
        self.set_breath_cycle(0,0, 4600)
        self.set_breath_cycle(0,1, 2000)
        self.set_breath_cycle(0,2, 3400)


    def get_distance(self):
        dist = 99999
        with SMBus(self.i2c) as bus:
            try:
                msg = i2c_msg.write(self.i2c_addr, [0,])
                bus.i2c_rdwr(msg)
                read = i2c_msg.read(self.i2c_addr, 2)
                bus.i2c_rdwr(read)
                dist = int.from_bytes(bytes(list(read)), byteorder='little', signed=False)
            except:
                pass
            if dist > 5000:
                dist = 5000
        return dist


