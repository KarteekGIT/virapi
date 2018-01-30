import multiprocessing
from time import sleep

def main():
    lock = multiprocessing.Lock()
    def process_for_sensor():
        while True:
            fileOpen = open('buttons/sensor', 'r+')
            sensor = fileOpen.read(5)
            sensor = sensor.strip("\n")
            if(sensor == 'True'):
                lock.acquire(block=True)
                print('sensor detected, running program')
                sleep(10)
                '''
                    The thread to be executed when document is placed 
                    and detected by the sensor
                '''
                fileOpen.seek(0)
                fileOpen.write('False')
                fileOpen.truncate()
                fileOpen.close()
                print('Done, exiting and releasing sensor lock')
                lock.release()

    def process_for_playOrStop():
        while True:
            filePlay = open('buttons/play', 'r+')
            fileStop = open('buttons/stop', 'r+')
            play = filePlay.read(5)
            play = play.strip('\n')
            if(play == 'True'):
                lock.acquire(block=True)
                print('Play button is pressed, running program')
                sleep(10)
                '''
                    The thread to be executed when play button is pressed
                '''
                filePlay.seek(0)
                fileStop.seek(0)
            
                filePlay.write('False')
                fileStop.write('True')
                
                filePlay.truncate()
                fileStop.truncate()
                
                filePlay.close()
                fileStop.close()
                
                print('Done, Exiting and releasing play lock')
                lock.release()

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
            
if __name__ == '__main__':main()