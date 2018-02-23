import threading
import multiprocessing
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Reader import Reader
import os

class PlayEvent(object):
    def __init__(self):
        self.folderid = None    
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()                            
        for file in file_list:
            if(file['title'] == "vira"):
                folderid = file['id']
                break
        file_list2 = self.drive.ListFile({'q': "'%s' in parents  and trashed=false" % folderid}).GetList()
        self.cursor = list(file_list2)
        
    def next_or_prev(self):
        flag = 0;
        liveProcess = []
        mp3file = self.download(self.cursor[flag]['id'],self.cursor[flag]['title'])
        read = Reader(mp3file)
        readProc = multiprocessing.Process(target = read.go_for_play, name="Read object started")
        readProc.start()
        liveProcess.append(readProc)
        while True:
            fileOpen = open('buttons/next', 'r+')
            next = fileOpen.read(5)
            next = next.strip("\n")
            if(next == "True" and flag >= 0):
                print(next)
                flag = flag + 1
                print(flag)
                if(len(liveProcess) > 0):
                    liveProcess.pop().terminate()
                    print("Process terminated")
                fileOpen.seek(0)
                fileOpen.write("False")
                fileOpen.truncate()
                fileOpen.close()        
                mp3file = self.download(self.cursor[flag]['id'],self.cursor[flag]['title'])
                read = Reader(mp3file)
                readProc = multiprocessing.Process(target = read.go_for_play, name="Read object started")
                readProc.start()
                liveProcess.append(readProc)
            fileOpen2 = open('buttons/previous', 'r+')
            prev = fileOpen2.read(5)
            prev = prev.strip("\n")
            #print(prev)
            if(prev == "True" and flag >= 1):
                print(prev)
                flag = flag - 1
                print(flag)
                if(len(liveProcess) > 0):
                    liveProcess.pop().terminate()
                fileOpen2.seek(0)
                fileOpen2.write("False")
                fileOpen2.truncate()
                fileOpen2.close()        
                mp3file = self.download(self.cursor[flag]['id'],self.cursor[flag]['title'])
                read = Reader(mp3file)
                readProc = multiprocessing.Process(target = read.go_for_play, name="Read object started")
                readProc.start()
                liveProcess.append(readProc)
    def go(self):
        nextPrev = threading.Thread(target = self.next_or_prev, name = 'Read obj')
        nextPrev.start()
    
    def download(self, id, title):
        if(os.path.exists('download/'+title)):
            return 'download/'+title
        file = self.drive.CreateFile({'id' : id})
        file.GetContentFile('download/'+title)
        return 'download/'+title
        
        
                    
if __name__=='__main__':
    play = PlayEvent()
    play.go()