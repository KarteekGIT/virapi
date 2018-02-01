import multiprocessing
from time import sleep
from StartEvent import StartEvent
from Defaults import SetDefaults

lock = multiprocessing.Lock()
def main():
    SetDefaults()
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
        while True:
            fileOpen = open('buttons/sensor', 'r+')
            sensor = fileOpen.read(5)
            sensor = sensor.strip("\n")
            if(sensor == 'True'):
                print("inside sensor")
                fileOpen.seek(0)
                fileOpen.write('False')
                fileOpen.truncate()
                fileOpen.close()
                lock.acquire(block=True)
                
                start = StartEvent()
                start.go()

                lock.release()
                print('Done, exiting and releasing sensor lock')
                SetDefaults()
    
def process_for_playOrStop():
        while True:
            filePlay = open('buttons/play', 'r+')
            play = filePlay.read(5)
            play = play.strip('\n')
            if(play == 'True'):
                filePlay.seek(0)
                filePlay.write('False')
                filePlay.truncate()
                filePlay.close()
                lock.acquire(block=True)
                print('Play button is pressed, running program')
                sleep(10)
                '''
                    The thread to be executed when play button is pressed
                '''
                lock.release()
                print('Done, Exiting and releasing play lock')
                SetDefaults()
            
if __name__ == '__main__':main()