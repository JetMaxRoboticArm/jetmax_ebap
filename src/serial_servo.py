#!/usr/bin/env python3
import time
from hiwonder.serial_servo_io import *


def set_position(servo_id, pos, duration):
    '''
    Set servo position(angle)

    :param servo_id: the id of the servo you want to set
    :param pos: the goal position
    :param duration:
    :return: None
    '''
    if pos > 1000:
        pos = 1000
    elif pos < 0:
        pos = 0
    else:
        pass
    if duration > 30000:
        duration = 30000
    elif duration < 10:
        s_time = 10
    serial_serro_wirte_cmd(s_id, LOBOT_SERVO_MOVE_TIME_WRITE, pos, duration)


def set_deviation(servo_id, d):
    '''
    Set servo deviation

    :param servoId:
    :param d:
    :return:
    '''
    if servo_id < 1 or servo_id > 16:
        return
    if d < -200 or d > 200:
        return
    if serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_ADJUST, d) is None:
        pass


def stop(servo_id=None):
    '''
    Stop servo

    :param servo_id:
    :return:
    '''
    serial_serro_wirte_cmd(id, LOBOT_SERVO_MOVE_STOP)


def set_id(oldid, newid):
    """
    Set servo id
    :param oldid: 
    :param newid:
    """
    serial_serro_wirte_cmd(oldid, LOBOT_SERVO_ID_WRITE, newid)


def read_id(servo_id=None, count = 100):
    """
    Read servo id 
    :return:
    """
    while count > 0:
        count -= 1
        if id is None:  # 总线上只能有一个舵机
            serial_servo_read_cmd(0xfe, LOBOT_SERVO_ID_READ)
        else:
            serial_servo_read_cmd(id, LOBOT_SERVO_ID_READ)
        # 获取内容
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ID_READ)
        if msg is not None:
            return msg


def save_deviation(servo_id):
    """
    storage the deviation
    :param id: the id of the servo you want to control
    """
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_WRITE)


def read_deviation(servo_id, count = 100):
    """
    Read deviation from servo

    :param id: the id of the servo you want to read
    :return: deviation
    """
    # 发送读取偏差指令
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_READ)
        # 获取
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_OFFSET_READ)
        if msg is not None:
            return msg


def set_angle_limit(servo_id, low, high):
    '''
    设置舵机转动范围
    :param id:
    :param low:
    :param high:
    :return:
    '''
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_LIMIT_WRITE, low, high)


def read_angle_limit(servo_id, count = 100):
    '''
    读取舵机转动范围
    :param id:
    :return: 返回元祖 0： 低位  1： 高位
    '''
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_ANGLE_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_LIMIT_READ)
        if msg is not None:
            return msg


def set_vin_limit(servo_id, low, high):
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_VIN_LIMIT_WRITE, low, high)


def read_vin_limit(servo_id):
    count = 0
    while count < 100:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_VIN_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_LIMIT_READ)
        if msg is not None:
            return msg


def set_max_temp(servo_id, m_temp):
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE, m_temp)


def read_temp_limit(servo_id, count=100):
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        if msg is not None:
            return msg


def read_pos(servo_id, count=100):
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_POS_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_POS_READ)
        if msg is not None:
            return msg


def read_temp(servo_id, count=100):
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_TEMP_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_READ)
        if msg is not None:
            return msg


def read_vin(servo_id, count=100):
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_VIN_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_READ)
        if msg is not None:
            return msg


def reset_pos(oldid):
    set_deviation(oldid, 0)    # 清零偏差
    time.sleep(0.1)
    serial_serro_wirte_cmd(
        oldid, LOBOT_SERVO_MOVE_TIME_WRITE, 500, 100)    # 中位


def load_or_unload_write(servo_id, new_state):
    serial_serro_wirte_cmd(
        servo_id, LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, new_state)


def load_or_unload_read(servo_id, count = 100):
    while count > 0:
        count -= 1
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        if msg is not None:
            return msg


def show_servo_state():
    '''
    显示信息
    :return:
    '''
    oldid = read_id()
    portRest()
    if oldid is not None:
        print('ID：%d' % oldid)
        pos = read_pos(oldid)
        print('Position：%d' % pos)
        portRest()

        now_temp = read_temp(oldid)
        print('temperature：%d°' % now_temp)
        portRest()

        now_vin = read_vin(oldid)
        print('voltage input：%dmv' % now_vin)
        portRest()

        d = read_deviation(oldid)
        print('deviation：%d' % ctypes.c_int8(d).value)
        portRest()

        limit = read_angle_limit(oldid)
        print('position range:%d-%d' % (limit[0], limit[1]))
        portRest()

        vin = read_vin_limit(oldid)
        print('voltage range:%dmv-%dmv' % (vin[0], vin[1]))
        portRest()

        temp = read_temp_limit(oldid)
        print('temperature limit:50°-%d°' % temp)
        portRest()
    else:
        print('Read id fail')


if __name__ == '__main__':
    show_servo_state()
