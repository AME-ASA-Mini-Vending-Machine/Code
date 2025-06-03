from machine import Pin
import time

ir_sensor = Pin(17, Pin.IN, Pin.PULL_DOWN)

def countCoins(c):
    
    numCoins = 0
    
    while numCoins < c:
        val = ir_sensor.value()
        
        if val == 0:
            numCoins += 1
            
        time.sleep(0.1)
    
    return numCoins

costReached = false

# If the cost was 1, the IR sensor would count 1 quarter
cost = 1
print(countCoins(cost))

cost = 2
print(countCoins(cost))

cost = 3
print(countCoins(cost))
