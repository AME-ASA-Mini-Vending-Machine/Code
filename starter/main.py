from DIYables_Pico_Keypad import Keypad
import time
from machine import I2C, Pin, PWM
from I2C_LCD import I2CLcd


# corresponds to 3x4 keypad layout
KEYMAP = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]

COSTMAP = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3]


# initialize i2c protocol
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
devices = i2c.scan()

# initialize lcd
try:
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        lcd.move_to(0, 0)
    else:
        print("LCD not found.")
except:
    print("Error initializing LCD.")

# initialize keypad
# keymap, number of row pins, GPIO pins of row pins, GPIO pins of column pins
keypad = Keypad(
    KEYMAP, ROW_PINS=4, COLUMN_PINS=3, NUM_ROWS=[3, 4, 5, 6], NUM_COLS=[0, 1, 2]
)
# >400 ms between each button press
keypad.set_debounce_time(400)

# initialize ir sensor
ir_sensor = Pin(17, Pin.IN, Pin.PULL_DOWN)

# intialize servos with pins 0-9
servos = [PWM(Pin(i)) for i in range(10)]

# Set Duty Cycle for Different Speeds
max_duty = 7864  # max cw rotation
min_duty = 1802  # max ccw rotation
half_duty = int((max_duty - min_duty) / 2)  # stop rotation

# vending machine state variables
queue = ""
confirmed = False
paid = False
cost = 1000
balance = 0

#function to read keys from keypad and add it to a queue, press # to finish reading keys
def read_key():
    global confirmed, cost,queue
    if confirmed==False:
        key = keypad.get_key()
        if key in "123456789":
            queue += key
        elif key == "#":
            if len(queue) == 1:
                confirmed = True
                cost = COSTMAP[int(queue)]
            else:
                lcd.putstr("Not a valid code. Try again.")
                time.sleep(1)
                queue = ""

#function to display text on LCD screen based on state of vending machine
def display():
    global queue,confirmed,paid,cost,balance
    if len(queue) == 0:
        lcd.putstr("Enter key for candy. Press # when done.")
    elif confirmed == False:
        lcd.putstr(queue)
    elif paid == False:
        lcd.putstr("Required: " + cost + "\nBalance: " + balance)
    else:
        lcd.pustr("Enjoy your snack.")
        time.sleep(5)
        queue = ""
        confirmed = False
        paid = False
        cost = 1000
        balance = 0

#function to detect inputted coins
def read_coin():
    global balance
    val = ir_sensor.value()
    if val == 0:
        balance += 1
        time.sleep(0.1)

#function to dispense queued item after cost is paid
def dispense_item():
    global paid
    if balance >= cost:
        paid = True
        servos[int(queue) - 1].duty_u16(max_duty)
        time.sleep(0.4)


# Main loop
while True:
    read_key()
    display()
    read_coin()
    dispense_item()
