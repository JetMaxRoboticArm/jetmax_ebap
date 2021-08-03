import time
import smbus2
import threading
from . import const

SERVO_ADDRESS = 21


class PWMServo:
    def __init__(self,
                 i2c_port,
                 servo_id,
                 min_position=0,
                 max_position=180,
                 min_duration=20,
                 max_duration=30000,
                 deviation=0):
        self.i2c_port = i2c_port
        if servo_id > 4 or servo_id < 1:
            raise ValueError('invalid servo id {}'.format(servo_id))
        self.servo_id = 5 - servo_id
        self.address = self.servo_id - 1 + SERVO_ADDRESS
        self.min_position = min_position
        self.max_position = max_position
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.deviation = deviation

        self.inc_times = 0
        self.pos_cur = 90
        self.pos_set = self.pos_cur
        self.pos_inc = 0
        self.lock = threading.Lock()
        threading.Thread(target=self.update_pos_task, daemon=True).start()

    def get_position(self):
        """
        :return:
        """
        return self.pos_cur

    def set_position(self, new_pos, duration=0):
        """
        :param new_pos:
        :param duration:
        :return:
        """
        new_pos = self.min_position if new_pos < self.min_position else new_pos
        new_pos = self.max_position if new_pos > self.max_position else new_pos
        new_pos = int(new_pos)
        duration = self.min_duration if duration < self.min_duration else duration
        duration = self.max_duration if duration > self.max_duration else duration
        duration = int(duration)
        inc_times = int(duration / 20 + 0.5)
        with self.lock:
            self.inc_times = inc_times
            self.pos_set = new_pos
            self.pos_inc = (self.pos_cur - new_pos) / inc_times

    def update_pos_task(self):
        while True:
            with self.lock:
                self.inc_times -= 1
                if self.inc_times > 0:
                    pos_cur = self.pos_set + int(self.pos_inc * self.inc_times)
                    with smbus2.SMBus(self.i2c_port) as bus:
                        bus.write_word_data(const.MCU_ADDRESS, self.address, pos_cur + self.deviation)
                    self.pos_cur = pos_cur
                elif self.inc_times == 0:
                    with smbus2.SMBus(self.i2c_port) as bus:
                        bus.write_word_data(const.MCU_ADDRESS, self.address, self.pos_set + self.deviation)
                    self.pos_cur = self.pos_set
                else:
                    self.inc_times = -1
            time.sleep(0.02)

    def set_deviation(self, new_deviation=0):
        """
        set deviation

        :param new_deviation:
        :return:
        """
        if not -300 < new_deviation < 300:
            raise ValueError("new deviation out range. it must be betweent -300~300")
        else:
            self.deviation = int(new_deviation)

    def get_deviation(self):
        """
        :return:
        """
        return self.deviation
