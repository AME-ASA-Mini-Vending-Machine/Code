from DIYables_Pico_Keypad import Keypad
from machine import I2C, Pin
from I2C_LCD import I2CLcd
import time

lcd_screen = I2C(0, sda = Pin(16), scl = Pin(17), freq = 400000)
devices = lcd_screen.scan()

try:
    if devices != []:
        lcd = I2CLcd(lcd_screen, devices[0], 2, 16)
        lcd.move_to(0, 0)
        
        
    
    else:
        print("No address found")
except:
    print("Something went wrong! Good luck!")