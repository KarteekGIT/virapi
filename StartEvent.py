from gtts import gTTS
import os
import multiprocessing as mp
from Reader import Reader
import datetime
from tesserocr import PyTessBaseAPI
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class StartEvent(object):
    def __init__(self):
        self.image = "image/image.png"
        self.text = "text/textfile.txt"
        self.running = True
        
    def camera_module(self):
        #if(os.path.exists(self.image)):
        #    os.remove(self.image)
        pass
        '''
            Run camera module here to take the picture and save it for processing
        '''    
    def image_filters(self):
        pass
        '''
            code for image filtering
        '''
    def convert_image_to_text(self):
        fileOPen = open(self.text, "w")
        with PyTessBaseAPI() as api:
            api.SetImageFile(self.image)
            text = api.GetUTF8Text()
            for line in str(text):
                fileOPen.write(line)
        
    def convert_text_to_mp3(self):
        print("Converting to mp3")
        text = ""
        file = open(self.text)
        for line in file:
            text = text+line
        tts = gTTS(text, lang='en', slow=False)
        now = datetime.datetime.now()
        s = str(now)
        s = s.replace(" ", "")        
        self.mp3file = "readdocs/"+s+".mp3"
        tts.save(self.mp3file)
        file.close()     
        
    def signal_filters(self):
        pass
        '''
            code for signal filtering
        '''
    
    def reader(self):
        print("Sending file to read")
        read = Reader(self.mp3file)
        read.go()
    
    def save_file_to_cloud(self):
        try:
            import httplib
        except:
            import http.client as httplib
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
        except:
            print("no internet connection")
            conn.close()
            return
        folderid = None    
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()                            
        for file1 in file_list:
            #print(file1['title'], type(file1['title']))
            if(file1['title'] == "vira"):
                folderid = file1['id']
                break
        if(folderid):
            print("Folder found")
        else:
            print("creating new folder")
            folder = "vira"
            newfolder_metadata = {'title' : folder, 'mimeType' : 'application/vnd.google-apps.folder'}
            newfolder = drive.CreateFile(newfolder_metadata)
            newfolder.Upload()
            folderid = newfolder['id']
        print("Uploading file to folder")
        newfile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}]})
        newfile.SetContentFile(self.mp3file)
        newfile.Upload()
            
    def execute_start(self):
        while self.running:
            fileOpen = open("buttons/start", "r+")
            start = fileOpen.read(5)
            start = start.strip("\n")
            if(start == "True"):
                fileOpen.seek(0)
                fileOpen.write('False')
                fileOpen.truncate()
                fileOpen.close()
                self.camera_module()
                self.image_filters()
                self.convert_image_to_text()
                self.convert_text_to_mp3()
                self.signal_filters()
                self.reader()
                self.save_file_to_cloud()
                self.running = False
                print("again in start event")
            
    def go(self):
        print("starting")
        execute = mp.Process(target=self.execute_start, name="process for start button")
        execute.start()
        if execute.is_alive():
            execute.join()
            
#if __name__=="__main__":
#    start = StartEvent()
#    start.convert_text_to_mp3()
#    start.save_file_to_cloud()