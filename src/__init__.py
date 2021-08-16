from hiwonder import pwm_servo as __pwm_servo
from hiwonder import motor as __motor
from hiwonder.motor import EncoderMotorController
from hiwonder import misc
from hiwonder import adc as __adc
from hiwonder.pid import PID
from hiwonder.colors import colors as COLORS
from hiwonder.colors import colors_bgr as COLORS_BGR
from hiwonder import serial_servo
from hiwonder import stepper
from hiwonder.stepper import Stepper
from hiwonder import kinematic
from hiwonder import jetmax
from hiwonder.jetmax import JetMax
from hiwonder.jetmax import Sucker
from hiwonder import mecanum
from hiwonder.mecanum import MecanumChassis

Kinematic = kinematic

motor1 = __motor.Motor(1, 1)
motor2 = __motor.Motor(1, 2)

pwm_servo1 = __pwm_servo.PWMServo(1, 1)
pwm_servo2 = __pwm_servo.PWMServo(1, 2)
pwm_servo3 = __pwm_servo.PWMServo(1, 3)
pwm_servo4 = __pwm_servo.PWMServo(1, 4)

battery = __adc.ADC(1, 0)
adc1 = __adc.ADC(1, 1)
adc2 = __adc.ADC(1, 2)
