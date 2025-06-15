from DIYables_Pico_Keypad import Keypad
import time
from machine import I2C, Pin, PWM
from I2C_LCD import I2CLcd
from micropython_servo_pdm_360 import ServoPDM360


# corresponds to 3x4 keypad layout
KEYMAP = ["1", "2", "3",
          "4", "5", "6",
          "7", "8", "9",
          "*", "0", "#"]

COSTMAP = [1, 1, 1,
           2, 2, 2,
           3, 3, 3]


# Initialize I2C protocol
i2c = I2C(0, sda = Pin(6), scl = Pin(7), freq = 400000)
devices = i2c.scan()

# Initialize LCD
try:
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        lcd.move_to(0, 0)
    else:
        print("LCD not found.")
except:
    print("Error initializing LCD.")

# Initialize keypad
# keymap, number of row pins, GPIO pins of row pins, GPIO pins of column pins
keypad = Keypad(KEYMAP, ROW_PINS = [11, 12, 13, 14], COLUMN_PINS = [8, 9, 10], NUM_ROWS = 4, NUM_COLS = 3)

# > 400 ms between each button press
keypad.set_debounce_time(400)

# Initialize IR sensor
ir = Pin(20, Pin.IN, Pin.PULL_DOWN)

# Initialize servos with pins 0-9
servos = [PWM(Pin(i)) for i in list(range(5)) + list(range(16, 20))]

# Set duty cycle
max_duty = 65535
min_duty = 0
half_duty = int((max_duty - min_duty) / 2)

# Vending machine state variables
queue = ""
confirmed = False
paid = False
cost = 1000
balance = 0

# Function to read keys from keypad and add them to a queue, press # to finish reading keys
def read_key():
    global confirmed, cost, queue
    
    if confirmed == False:
        key = keypad.get_key()
        if key in "123456789":
            queue += key
        elif key == "#":
            if len(queue) == 1:
                confirmed = True
                cost = COSTMAP[int(queue)-1]
            else:
                lcd.putstr("Not a valid code. Try again.")
                time.sleep(1)
                queue = ""

# Function to display text on LCD screen based on state of vending machine
def display():
    global queue, confirmed, paid, cost, balance
    
    if len(queue) == 0:
        lcd.putstr("Enter key for candy. Press # when done.")
    
    elif confirmed == False:
        lcd.putstr(queue)
    
    elif paid == False:
        lcd.putstr("Required: " + cost + "\nBalance: " + balance)
    
    else:
        lcd.pustr("Enjoy your snack!")
        time.sleep(5)
        queue = ""
        confirmed = False
        paid = False
        cost = 1000
        balance = 0

# Function to detect inputted coins
def read_coin():
    global balance
    
    val = ir.value()
    if val == 0:
        balance += 1
        time.sleep(0.1)

# Function to dispense queued item after cost is paid
def dispense_item():
    global paid
    
    if balance >= cost:
        paid = True
        if(int(queue)<=5):
            servos[int(queue)-1].turn_cv()
        else:
            servos[int(queue)+9].turn_cv()
        time.sleep(0.4)

# Main loop
while True:
    read_key()
    display()
    read_coin()
    dispense_item()