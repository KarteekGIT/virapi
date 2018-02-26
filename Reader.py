import threading as mp
import pygame
from Defaults import SetDefaults
import os
from PlayEvent import PlayEvent
class Reader(object):
    def __init__(self, filename):
        self.filename = filename
        self.flag = False
        self.run = True
        self.reader = None
        self.playing = None
        self.nextPrev = None
        self.rwind = None
        self.volume = None
        self.playAgainEvent = False
        self.running_process=[]
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)
        self.fileDealer = SetDefaults()        
        
    def reading(self):
        print("Reader started")
        pygame.mixer.music.play()
        try:
            while self.run:
                if(self.playAgainEvent):
                    self.playAgainEvent = False
                    pygame.mixer.music.play()
                end = self.fileDealer.fileReader("buttons/start")
                if(end == "True"):
                    self.fileDealer.fileWriter("buttons/start")
                    self.run = False
                    self.quit()
            print("Reading Exiting")
        except:
            SetDefaults()
            print("exception occured Reading Exiting")
    def play_or_stop(self):
        try:
            while self.run:
                stop = self.fileDealer.fileReader("buttons/stop")
                play = self.fileDealer.fileReader("buttons/play")            
                if(stop == "True"):
                    self.flag = True
                if(play == "True"):
                    print("play")
                    print("Write False to play")
                    self.fileDealer.fileWriter("buttons/play")
                    pygame.mixer.music.unpause()

                if(self.flag):
                    if(stop == "True"):
                        print("stop")
                        self.flag = False
                        print("Write False to stop")
                        self.fileDealer.fileWriter("buttons/stop")
                        pygame.mixer.music.pause()
            print("PlayorStop Exiting")
        except:
            SetDefaults()
            print("exception occured PlayorStop Exiting")

    def rewind(self):
        try:
            while self.run:
                rewind = self.fileDealer.fileReader("buttons/previous")
                if(rewind == "True"):
                    print("rewind")
                    self.fileDealer.fileWriter("buttons/previous")
                    pygame.mixer.music.rewind()
        except:
            SetDefaults()
            print("Exiting")
            
    def volume_up_down(self):
        '''
            Code to control volume
            
        '''
        
    def next_or_prev(self):
        self.nextOrPrevflag = 0;
        nextStatus = self.nextOrPrevflag
        prevStatus = nextStatus
        fileDownload = PlayEvent()
        self.mp3file = self.mp3file = fileDownload.download(fileDownload.cursor[self.nextOrPrevflag+1]['id'],fileDownload.cursor[self.nextOrPrevflag+1]['title'])
        pygame.mixer.music.queue(self.mp3file)
        try:
            while self.run:
                if(nextStatus < self.nextOrPrevflag):
                    print("flag next: "+str(self.nextOrPrevflag))
                    print("next stat1: "+str(nextStatus))
                    nextStatus = self.nextOrPrevflag
                    prevStatus = nextStatus
                    print("next stat2: "+str(nextStatus))
                    self.mp3file = fileDownload.download(fileDownload.cursor[nextStatus]['id'],fileDownload.cursor[nextStatus]['title'])
                    self.playNewFile(self.mp3file)
                    if(len(fileDownload.cursor) > 1):
                        pygame.mixer.music.queue(fileDownload.download(fileDownload.cursor[nextStatus+1]['id'],fileDownload.cursor[nextStatus+1]['title']))
                if(prevStatus > self.nextOrPrevflag):
                    print("flag prev :"+str(self.nextOrPrevflag))
                    print("prev stat: "+str(prevStatus))
                    prevStatus = self.nextOrPrevflag
                    nextStatus = prevStatus
                    print("prev stat: "+str(prevStatus))
                    self.mp3file = fileDownload.download(fileDownload.cursor[prevStatus]['id'],fileDownload.cursor[prevStatus]['title'])
                    self.playNewFile(self.mp3file)
                    if(prevStatus > 0):
                        pygame.mixer.music.queue(fileDownload.download(fileDownload.cursor[prevStatus-1]['id'],fileDownload.cursor[prevStatus-1]['title']))                                
                fileList = os.listdir("buffer")
                numOfFiles = len(fileList)
                if(numOfFiles > 5):
                    for file in fileList:
                        os.remove("buffer/"+file)
                next = self.fileDealer.fileReader("buttons/next")
                if(next == "True" and self.nextOrPrevflag >= 0):
                    if(self.nextOrPrevflag < len(fileDownload.cursor)):
                        self.nextOrPrevflag = self.nextOrPrevflag + 1
                    self.fileDealer.fileWriter("buttons/next")
                prev = self.fileDealer.fileReader("buttons/previous")
                if(prev == "True" and self.nextOrPrevflag >= 1):
                    self.nextOrPrevflag = self.nextOrPrevflag - 1
                    self.fileDealer.fileWriter("buttons/previous")        
            print("Exciting nextPevious")
        except:
            SetDefaults()
            print("Exception occured exiting nextprevious")
                    
    def quit(self):
        pygame.mixer.music.stop()
        
    def playNewFile(self, filename):
        self.filename = filename
        pygame.mixer.music.load(self.filename)
        self.playAgainEvent = True
        SetDefaults()        
                
    def go(self):
        print("Ready for reading")
        self.reader = mp.Thread(target=self.reading, name="reading process")
        self.playing = mp.Thread(target=self.play_or_stop, name="process waiting for play")
        self.rwind = mp.Thread(target=self.rewind, name="process waiting for rewind")        
        self.reader.start()
        self.playing.start()
        self.rwind.start()
        self.joiner([self.reader, self.playing, self.rwind])
        print("Process for play stop rewind started")
                
    def go_for_play(self):
        self.reader = mp.Thread(target=self.reading, name="reading process")
        self.playing = mp.Thread(target=self.play_or_stop, name="process waiting for play")
        self.nextPrev = mp.Thread(target=self.next_or_prev, name="Process for next or previous")
        self.reader.start()
        self.playing.start()
        self.nextPrev.start()
        self.joiner([self.reader, self.playing, self.nextPrev])
        print("Process for play stop nextprev started")
        
    def joiner(self, processList = []):
        for proc in processList:
            self.running_process.append(self.playing)
        for proc in self.running_process:
            if proc.is_alive():
                proc.join()