import sys
import time
import smbus2
import threading
import const

MOTOR_ADDRESS = 31
ENCODER_MOTOR_MODULE_ADDRESS = 0x34

class Motor:

    def __init__(self, 
                 i2c_port,
                 motor_id):
        self.i2c_port = i2c_port
        self.motor_id = motor_id
        self.address = MOTOR_ADDRESS + self.motor_id - 1
        self.speed = 0
        self.lock = threading.Lock()
                    
    def set_speed(self, speed):
        speed = 100 if speed > 100 else speed
        speed = -100 if speed < -100 else speed
        with self.lock:
            with smbus2.SMBus(self.i2c_port) as bus:
                bus.write_i2c_block_data(const.MCU_ADDRESS, self.address, [speed])
                self.speed = speed
 

class EncoderMotorController:
    def __init__(self, i2c_port, motor_type = 3):
        self.i2c_port = i2c_port
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_i2c_block_data(ENCODER_MOTOR_MODULE_ADDRESS, 20, [motor_type,])

    def set_speed(self, speed, motor_id=None, offset=0):
        with smbus2.SMBus(self.i2c_port) as bus:
            if motor_id is None:
                bus.write_i2c_block_data(ENCODER_MOTOR_MODULE_ADDRESS,  51 + offset, speed) 
            else:
                bus.write_i2c_block_data(ENCODER_MOTOR_MODULE_ADDRESS,  51 + motor_id - 1, [speed, ]) 












