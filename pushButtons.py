import RPi.GPIO as GPIO
import time
from Defaults import SetDefaults

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

fileDealer = SetDefaults()
while True:
    input_state18 = GPIO.input(18)
    input_state17 = GPIO.input(17)
    input_state2 = GPIO.input(2)
    input_state3 = GPIO.input(3)
    input_state4 = GPIO.input(4)
    input_state27 = GPIO.input(27)
    input_state22 = GPIO.input(22)
    
    if input_state18 == False:
        print('Start Pressed')
        fileDealer.fileTrue("buttons/start")
        time.sleep(0.8)

    if input_state17 == False:
        print('Next Pressed')
        fileDealer.fileTrue("buttons/next")
        time.sleep(0.8)

    if input_state2 == False:
        print('Play/Stop Pressed')
        play = fileDealer.fileReader("buttons/play")
        stop = fileDealer.fileReader("buttons/stop")
        if stop == "True":
            fileDealer.fileWrite("buttons/stop")
            fileDealer.fileTrue("buttons/play")
        if play == "True":
            fileDealer.fileWrite("buttons/play")
            fileDealer.fileTrue("buttons/stop")
        time.sleep(0.8)

    if input_state3 == False:
        print('Previous Pressed')
        fileDealer.fileTrue("buttons/previous")
        time.sleep(0.8)

    if input_state4 == False:
        print('Volumeup Pressed')
        fileDealer.fileTrue("buttons/volumeup")
        time.sleep(0.8)

    if input_state27 == False:
        print('Volumedown Pressed')
        fileDealer.fileTrue("buttons/volumedown")
        time.sleep(0.8)

    if input_state22 == False:
        print('Shutdown Pressed')
        #fileDealer.fileTrue("buttons/start")
        time.sleep(0.8)
