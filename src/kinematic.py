#!/usr/bin/env python3
import math

L0 = 84.4
L1 = 8.14
L2 = 128.4
L3 = 138.0

RAD_PER_DEG = math.pi / 180
DEG_PER_RAD = 180 / math.pi
DOUBLE_PI = math.pi * 2


def forward_kinematics(angles):
    """
    JetMax forward kinematics

    @param angles: active angles [rotate, angle left, angle right]
    @return: end point position (x, y, z)
    """

    alpha1, alpha2, alpha3 = [angle * RAD_PER_DEG for angle in angles]
    alpha1 += 150 * RAD_PER_DEG
    alpha1 = alpha1 - DOUBLE_PI if alpha1 > DOUBLE_PI else alpha1
    beta = alpha2 - alpha3
    side_beta = math.sqrt(L2 ** 2 + L3 ** 2 - 2 * L2 * L3 * math.cos(beta))
    cos_gamma = ((side_beta ** 2 + L2 ** 2) - L3 ** 2) / (2 * side_beta * L2)
    cos_gamma = cos_gamma if cos_gamma < 1 else 1
    gamma = math.acos(cos_gamma)
    alpha_gamma = math.pi - alpha2
    alpha = alpha_gamma - gamma
    z = side_beta * math.sin(alpha)
    r = math.sqrt(side_beta ** 2 - z ** 2)
    z = z + L0
    r = r + L1
    x = r * math.cos(alpha1)
    y = r * math.sin(alpha1)
    return x, y, z


def inverse_kinematic(position):
    """
    JetMax inverse kinematics

    @param position: target position (x, y, z)
    @return: joint angles list
    """
    x, y, z = position
    r = math.sqrt(x ** 2 + y ** 2)
    if x == 0:
        theta1 = math.pi / 2 if y >= 0 else math.pi / 2 * 3  # pi/2 90deg, (pi * 3) / 2  270deg
    else:
        if y == 0:
            theta1 = 0 if x > 0 else math.pi
        else:
            theta1 = math.atan(y / x)  # θ=arctan(y/x) (x!=0)
            if x < 0:
                theta1 += math.pi
            else:
                if y < 0:
                    theta1 += math.pi * 2

    r = r - L1
    z = z - L0
    if math.sqrt(r ** 2 + z ** 2) > (L2 + L3):
        raise ValueError('Unreachable position: x:{}, y:{}, z:{}'.format(x, y, z))

    alpha = math.atan(z / r)
    beta = math.acos((L2 ** 2 + L3 ** 2 - (r ** 2 + z ** 2)) / (2 * L2 * L3))
    gamma = math.acos((L2 ** 2 + (r ** 2 + z ** 2) - L3 ** 2) / (2 * L2 * math.sqrt(r ** 2 + z ** 2)))

    theta1 = theta1
    theta2 = math.pi - (alpha + gamma)
    theta3 = math.pi - (beta + alpha + gamma)

    theta1 = theta1 * DEG_PER_RAD
    if 30 < theta1 < 150:  # The servo motion range is 240 deg. 150~360+0~30 = 240
        raise ValueError('Unreachable position: x:{}, y:{}, z:{}'.format(x, y, z))
    theta1 = theta1 + 360 if theta1 <= 30 else theta1  # 0~360 to 30~390
    theta1 = theta1 - 150
    return theta1, theta2 * DEG_PER_RAD, theta3 * DEG_PER_RAD


def pulse_to_deg(pulses):
    pulse1, pulse2, pulse3 = pulses
    angle1 = pulse1 * 240 / 1000  # 0~1000 map to 0~240
    angle2 = pulse2 * -240 / 1000 + 210  # 0~1000 map to 210~-30
    angle3 = pulse3 * 240 / 1000 - 120  # 0~1000 map to -120~120
    return angle1, angle2, angle3


def deg_to_pulse(angles):
    angle1, angle2, angle3 = angles
    pulse1 = angle1 * 1000 / 240  # 0~240 map to 0~1000
    pulse2 = (angle2 - 210) * 1000 / -240  # 210~-30 map to 0~1000
    pulse3 = (angle3 - -120) * 1000 / 240  # -120~120 map to 0~1000
    return pulse1, pulse2, pulse3
