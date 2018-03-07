from gtts import gTTS
import os
from tesserocr import PyTessBaseAPI
import multiprocessing as mp
from Reader import Reader
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Defaults import SetDefaults

class StartEvent(object):
    def __init__(self):
        self.image = "image/image.png"
        self.text = "text/textfile.txt"
        self.running = True
        self.fileDealer = SetDefaults()
        
    def camera_module(self):
        #if(os.path.exists(self.image)):
        #    os.remove(self.image)
        pass
        '''
            Run camera module here to take the picture and save it for processing
        '''    
    def convert_image_to_text(self):
        os.system("sh imageToText.sh")
        #fileOPen = open(self.text, "w")
        #with PyTessBaseAPI() as api:
            #api.SetImageFile(self.image)
            #text = api.GetUTF8Text()
            #for line in str(text):
                #try:
                    #fileOPen.write(line)
                #except:
                    #print("Invalid character. Cannot convert")
        
    def convert_text_to_mp3(self):
        fileList = os.listdir("readdocs")
        numOfFiles = len(fileList)
        if(numOfFiles > 5):
            for file in fileList:
                os.remove("readdocs/"+file)        
        text = ""
        file = open(self.text)
        try:
            for line in file:
                try:
                    text = str(text+line)
                except:
                    print("Invalid characters left out")
        except:
            print("Invalid characters left out, outer loop")
        tts = gTTS(text, lang='en', slow=False)
        now = datetime.datetime.now()
        s = str(now)
        s = s.replace(" ", "")        
        self.mp3file = "readdocs/"+s+".mp3"
        tts.save(self.mp3file)
        file.close()     
    
    def reader(self):
        print("starting reading file")
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
        newfile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}], "title": self.mp3file[9:]})
        newfile.SetContentFile(self.mp3file)
        newfile.Upload()
            
    def go(self):
        self.camera_module()
        self.convert_image_to_text()
        self.convert_text_to_mp3()
        self.reader()
        self.save_file_to_cloud()
        self.running = False
        self.fileDealer.fileWriter("buttons/play")
        print("again in start event")
