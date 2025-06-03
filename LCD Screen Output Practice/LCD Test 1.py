import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd
import random

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
devices = i2c.scan()

try:
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        lcd.move_to(0, 0)
        
        while True:
            ''' Represents the number of inputs from the keypad. If a user presses more than 1 button once, then
                num_inputs > 1 '''
            
            num_inputs = random.randint(1, 5)
            print("Num_inputs: ", num_inputs)
            
            if (num_inputs > 1):
                lcd.putstr("Invalid input!\n1 number only.")
                time.sleep(3)
                lcd.clear()
                
            else:
                lcd.putstr("Enjoy!")
                time.sleep(3)
                lcd.clear()
    
    else:
        print("No address found")
except:
    print("Something went wrong! Good luck!")
