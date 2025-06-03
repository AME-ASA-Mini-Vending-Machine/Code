import time
from servo import Servo
my_servo = Servo(pin_id=28)
my_servo.write(30)
time.sleep(2.0)
my_servo.write(60)
time.sleep(2.0)
my_servo.write(90)

# from machine import Pin, PWM
# from time import sleep
# from servo import Servo
# 
# # Initialize Servo on pin 0 with micropythonservo library
# servo = Servo(pin_id=0)
# 
# # Sweep the servo from 0 to 180 degrees and back
# while True:
#     for angle in range(0, 180, 5):  # start at 0 and count in 5s until 180 is reached
#         
#         # angle will be updated every loop so we will use it to set the servo angle
#         servo.write(angle)
#         sleep(0.1)
# 
#     for angle in range(180, 0, -5):  # 180 to 0 degrees, 5 degrees at a time
#                 
#         # angle will be updated every loop so we will use it to set the servo angle
#         servo.write(angle)
#         sleep(0.1)