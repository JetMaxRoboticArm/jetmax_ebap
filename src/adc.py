import smbus2
from . import const

ADC1_ADDRESS = 0
ADC2_ADDRESS = 2
BAT_ADDRESS = 10


class ADC:
    def __init__(self, i2c_port, adc_id):
        self.i2c_port = i2c_port
        if adc_id == 0:
            self.address = BAT_ADDRESS
        elif adc_id == 1:
            self.address = ADC1_ADDRESS
        elif adc_id == 2:
            self.address = ADC2_ADDRESS
        else:
            raise ValueError("Invalid adc id {}".format(adc_id))

    def get_adc(self):
        value = [0, 0]
        with smbus2.SMBus(self.i2c_port) as bus:
            bus.write_byte(const.MCU_ADDRESS, self.address)
            value[0] = bus.read_byte(const.MCU_ADDRESS)
            value[1] = bus.read_byte(const.MCU_ADDRESS)
        if self.address == BAT_ADDRESS:
            return (value[0] + (value[1] << 8)) * 3
        else:
            return value[0] + (value[1] << 8)
