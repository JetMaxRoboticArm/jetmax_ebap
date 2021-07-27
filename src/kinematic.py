#!/usr/bin/env python3
import math
from hiwonder import serial_servo as ssr

L0 = 84.4
L1 = 8.14
L2 = 128.41
L3 = 138.0
L4 = 0.
L5 = 0.


class IKinematic:
    def __init__(self):
        self.cur_x = None
        self.cur_y = None

    def resolve(self, x, y, z, move=False, t = 500):
        if y == 0:
            if x < 0:
                theta1 = -90
            elif x > 0:
                theta1 = 90
            else:
                raise ValueError('Invalid coordinate x:{} y:{}'.format(x, y))
        else:
            theta1 = math.atan(x / y)
            theta1 = 0.0 if x == 0 else theta1 * 180.0 / math.pi
            if y < 0:
                if theta1 < 0 < x:
                    theta1 = 180 + theta1
                elif theta1 > 0 > x:
                    theta1 = -180 + theta1
                else:
                    pass

        x = math.sqrt(x * x + y * y) - L1
        z = z - L0 + L4

        if math.sqrt(x * x + z * z) > L2 + L3:
            return None

        alpha = math.atan(z / x) * 180.0 / math.pi
        beta = math.acos((L2 * L2 + L3 * L3 - (x * x + z * z)) / (2 * L2 * L3)) * 180.0 / math.pi
        gama = math.acos((L2 * L2 - L3 * L3 + (x * x + z * z)) / (2 * L2 * math.sqrt(x * x + z * z))) * 180.0 / math.pi

        pos1 = (theta1 + 120) / 240 * 1000

        theta2 = alpha + gama
        pos2 = (theta2 + 30) / 240 * 1000  # 90 degree ~~ 500 position

        theta3 = beta + theta2
        pos3 = 1000 - (theta3 - 60) / 240 * 1000
        if move:
            ssr.set_position(3, int(pos3), t)
            ssr.set_position(2, int(pos2), t)
            ssr.set_position(1, int(pos1), t)
        return pos1, pos2, pos3
