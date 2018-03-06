import multiprocessing
from StartEvent import StartEvent
from Defaults import SetDefaults
from PlayEvent import PlayEvent
from Reader import Reader

fileDealer = SetDefaults()
lock = multiprocessing.Lock()
condition = multiprocessing.Condition()
def main():
    process_running = []
    
    sensor_process = multiprocessing.Process(target=process_for_sensor, name='Process Waiting For Sensor')
    play_or_stop_process = multiprocessing.Process(target=process_for_playOrStop, name='Process Waiting For Play or Stop button')
    
    sensor_process.start()
    play_or_stop_process.start()
        
    process_running.append(sensor_process)
    process_running.append(play_or_stop_process)
    
    for proc in process_running:
        if(proc.is_alive()):
            proc.join()
def process_for_sensor():
    condition.acquire()    
    while True:
        play = fileDealer.fileReader("buttons/play")
        if(play == "True"):
            condition.wait()
        sensor = fileDealer.fileReader("buttons/start")
        if(sensor == "True"):
            fileDealer.fileWriter("buttons/start")
            lock.acquire(block=True)
            print("inside sensor")
            start = StartEvent()
            start.go()
            print("Done, exiting and releasing sensor lock")
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
            print("Play button is pressed, running program")
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
if __name__ == '__main__':main()
