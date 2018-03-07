import RPi.GPIO as GPIO
import time
from Defaults import SetDefaults

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

fileDealer = SetDefaults()
while True:
    input_state18 = GPIO.input(18)
    input_state17 = GPIO.input(17)

    if input_state18 == False:
        print('Start Pressed')
        fileDealer.fileTrue("buttons/start")
        time.sleep(1.0)
    
    if input_state17 == False:
        print('Play Pressed')
        fileDealer.fileTrue("buttons/next")
        time.sleep(1.0)
