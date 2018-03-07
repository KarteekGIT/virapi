import multiprocessing
from StartEvent import StartEvent
from Defaults import SetDefaults
from PlayEvent import PlayEvent
from Reader import Reader
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
fileDealer = SetDefaults()
lock = multiprocessing.Lock()
condition = multiprocessing.Condition()

def main():
    print("Please place document on the reader pad and press start. Or please press play to read from your cloud")
    process_running = []

    sensor_process = multiprocessing.Process(target=process_for_sensor, name='Process Waiting For Sensor')
    play_or_stop_process = multiprocessing.Process(target=process_for_playOrStop, name='Process Waiting For Play or Stop button')
    push_button_process = multiprocessing.Process(target=process_for_pushbuttons, name='Process push buttons')
    push_button_process.daemon = True
    
    sensor_process.start()
    play_or_stop_process.start()
    push_button_process.start()

    process_running.append(sensor_process)
    process_running.append(play_or_stop_process)
    process_running.append(process_for_pushbuttons)

    for proc in process_running:
        if(proc.is_alive()):
            proc.join()

def process_for_sensor():
    condition.acquire()
    while True:
        play = fileDealer.fileReader("buttons/next")
        if(play == "True"):
            condition.wait()
        sensor = fileDealer.fileReader("buttons/start")
        if(sensor == "True"):
            fileDealer.fileWriter("buttons/start")
            lock.acquire(block=True)
            print("Parsing document. It may take 7 to 10 minutes.")
            start = StartEvent()
            start.go()
            print("Done reading document")
            SetDefaults()
            condition.notify()
            lock.release()
    condition.release()


def process_for_playOrStop():
    condition.acquire()
    while True:
        start = fileDealer.fileReader("buttons/start")
        if(start == "True"):
            condition.wait()
        play = fileDealer.fileReader("buttons/next")
        if(play == "True"):
            fileDealer.fileWriter("buttons/next")
            print("Retrieving file from the cloud.")
            lock.acquire(block=True)
            firstDownload = PlayEvent()
            firstFile = firstDownload.download(firstDownload.cursor[0]["id"], firstDownload.cursor[0]["title"])
            playFirst = Reader(firstFile)
            playFirst.go_for_play()
            print('Done, Exiting and releasing play lock')
            SetDefaults()
            condition.notify()
            lock.release()
    condition.release()

def process_for_pushbuttons():
    while True:
        input_state18 = GPIO.input(18)
        input_state17 = GPIO.input(17)
        input_state2 = GPIO.input(2)
        input_state3 = GPIO.input(3)
        input_state4 = GPIO.input(4)
        input_state27 = GPIO.input(27)
        input_state22 = GPIO.input(22)
    
        if(input_state18) == False:
            print('Start Pressed')
            fileDealer.fileTrue("buttons/start")
            time.sleep(0.8)

        if(input_state17) == False:
            print('Next Pressed')
            fileDealer.fileTrue("buttons/next")
            time.sleep(0.8)

        if(input_state2) == False:
            print('Play Pressed')
            fileDealer.fileTrue("buttons/play")
            time.sleep(0.8)
        
        if(input_state22) == False:
            print('Stop Pressed')
            fileDealer.fileTrue("buttons/stop")
            time.sleep(0.8)
        
        if(input_state3) == False:
            print('Previous Pressed')
            fileDealer.fileTrue("buttons/previous")
            time.sleep(0.8)

        if(input_state4) == False:
            print('Volumeup Pressed')
            fileDealer.fileTrue("buttons/volumeup")
            time.sleep(0.8)

        if(input_state27) == False:
            print('Volumedown Pressed')
            fileDealer.fileTrue("buttons/volumedown")
            time.sleep(0.8)

if __name__ == '__main__':main()
