# jetmax_ebap
JetMax extension board access package

## 1.Installation
```
$ git clone https://github.com/JetMaxRoboticArm/jetmax_ebap.git
$ cd jetmax_ebap
$ python3 setup.py install
```

## 2.Usage

```
import hiwonder

hiwonder.serial_servo.set_position(1, 500, 1000) #Servo 1 move to 500 position in 1000 ms
hiwonder.pwm_servo1.set_position(90, 1000) #PWM Servo 1 move to 90deg in 1000ms
hiwonder.motor1.set_speed(100) #Set motor1 speed as 100%

```




