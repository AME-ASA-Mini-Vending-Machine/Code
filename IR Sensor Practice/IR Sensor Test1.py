from machine import Pin, ADC
import time

ir_sensor = Pin(16, Pin.IN, Pin.PULL_DOWN)

while True:
    val = ir_sensor.value()
    
    print(val)
    time.sleep(0.1)
