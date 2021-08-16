import rospy
import threading
import hiwonder


class Sucker:
    def __init__(self):
        self.__state = False  # False for release, True for suck
        self.__timer = threading.Timer(0.1, self.release_cb)
        self.__timer.start()

    def suck(self):
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None
        hiwonder.motor2.set_speed(0)  # Close the vent valve
        hiwonder.motor1.set_speed(100)  # Turn on the air pump
        self.__state = True

    def release(self, duration=0.5):
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None
        hiwonder.motor1.set_speed(0)  # Turn off the air pump
        hiwonder.motor2.set_speed(100)  # Open the vent valve
        self.__timer = threading.Timer(duration, self.release_cb)
        self.__timer.start()
        self.__state = False

    def release_cb(self):
        self.__timer = None
        hiwonder.motor1.set_speed(0)
        hiwonder.motor2.set_speed(0)

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        if new_state:
            self.suck()
        else:
            self.release()


class JetMax:
    ORIGIN = 0, -(hiwonder.kinematic.L1 + hiwonder.kinematic.L3), hiwonder.kinematic.L0 + hiwonder.kinematic.L2

    def __init__(self, origin=ORIGIN):
        self.__lock = threading.RLock()
        self.origin = origin
        self.position = self.origin
        self.joints = 120, 90, 0
        self.servos = 500, 500, 500  # [servo id 1, servo id 2, servo id 3]

    def set_servo_in_range(self, servo_id, p, duration):
        if servo_id == 3 and p < 490:
            return False
        if servo_id == 2 and p > 700:
            return False
        hiwonder.serial_servo.set_position(servo_id, int(p), duration)
        return True

    def set_position(self, position, duration):
        duration = int(duration * 1000)
        x, y, z = position
        angles = hiwonder.kinematic.inverse_kinematic((x, y, z))
        pulses = hiwonder.kinematic.deg_to_pulse(angles)
        with self.__lock:
            for i in range(3):
                ret = self.set_servo_in_range(i + 1, pulses[i], duration)
                if not ret:
                    raise ValueError("{} Out of limit range".format(pulses[i]))
            self.servos = pulses
            self.joints = angles
            self.position = x, y, z

    def set_position_relatively(self, values, duration):
        with self.__lock:
            x, y, z = self.position
            x_v, y_v, z_v = values
            x += x_v
            y += y_v
            z += z_v
            return self.set_position((x, y, z), duration)

    def set_servo(self, servo_id, pulse, duration):
        if not 0 < servo_id < 4:
            raise ValueError("Invalid servo id:{}".format(servo_id))
        pulse = 0 if pulse < 0 else pulse
        pulse = 1000 if pulse > 1000 else pulse
        duration = int(duration * 1000)
        with self.__lock:
            ret = self.set_servo_in_range(servo_id, pulse, duration)
            if not ret:
                raise ValueError("Out of limit range")
            servos = list(self.servos)
            servos[servo_id - 1] = pulse
            self.servos = tuple(servos)
            self.joints = hiwonder.kinematic.pulse_to_deg(self.servos)
            self.position = hiwonder.kinematic.forward_kinematics(self.joints)

    def set_servo_relatively(self, servo_id, value, duration):
        if not 0 < servo_id < 4:
            raise ValueError("Invalid servo id:{}".format(servo_id))
        index = servo_id - 1
        with self.__lock:
            pulse = self.servos[index]
            pulse += value
            return self.set_servo(servo_id, pulse, duration)

    def set_joint(self, joint_id, angle, duration):
        if not 0 < joint_id < 4:
            raise ValueError("Invalid joint id:{}".format(joint_id))
        with self.__lock:
            angles = list(self.joints)
            angles[joint_id - 1] = angle
            servos = hiwonder.kinematic.deg_to_pulse(angles)
            return self.set_servo(joint_id, servos[joint_id - 1], duration)

    def set_joint_relatively(self, joint_id, value, duration):
        if not 0 < joint_id < 4:
            raise ValueError("Invalid joint id:{}".format(joint_id))
        with self.__lock:
            angles = list(self.joints)
            angles[joint_id - 1] += value
            servos = hiwonder.kinematic.deg_to_pulse(angles)
            return self.set_servo(joint_id, servos[joint_id - 1], duration)

    def go_home(self, duration=2):
        self.set_position(self.origin, duration)
