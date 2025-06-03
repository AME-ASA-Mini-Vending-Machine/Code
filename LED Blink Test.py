from machine import Pin
import time

# set up pin 15 as an input with a pull-down resistor
button = Pin(15, Pin.IN)

# set up pin 16 connected to the LED as an output
led = Pin(16, Pin.OUT)

while True:
    pressed = button.value() == 0
    
    if pressed:
        led.value(1)
    
    else:
        led.value(0)
        
    time.sleep(0.1)