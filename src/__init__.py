from hiwonder import motor as __motor
from hiwonder import adc as __adc
from hiwonder import pwm_servo as __pwm_servo
from hiwonder import misc
from hiwonder import serial_servo
from hiwonder import kinematic
from hiwonder import stepper
from hiwonder.pid import PID
from hiwonder.motor import EncoderMotorController
from hiwonder.colors import colors

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
