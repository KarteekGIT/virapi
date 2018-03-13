from gtts import gTTS
import os
import multiprocessing as mp
from Reader import Reader
import datetime
import pygame
import pygame.camera
from pygame.locals import *
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
        try:
            pygame.camera.init()
            camList = pygame.camera.list_cameras()
            for cams in camList:
                print(cams)
                
            if camList:
                print("In camlist")
                cam = pygame.camera.Camera(camList[0], (640, 480))
                cam.start()
                #cam.set_controls(hflip=False, vflip=False, brightness=10)
                img = cam.get_image()
                print(type(img))
                pygame.image.save(img, self.image)

            cam.stop()
        except:
            print("Cannot take picture")
        
    def convert_image_to_text(self):
        try:
            os.system("sh imageToText.sh")
        except:
            print("Cannot convert image to text")

    def convert_text_to_mp3(self):
        try:
            fileList = os.listdir("readdocs")
            numOfFiles = len(fileList)
            if(numOfFiles > 5):
                for file in fileList:
                    os.remove("readdocs/"+file)
            text = ""
            file = open(self.text, 'r+', encoding="utf-8")
            for line in file:
                text = str(text+line)
                #print("Invalid characters left out")
            #print("Invalid characters left out, outer loop")
            tts = gTTS(text, lang='en', slow=False)
            now = datetime.datetime.now()
            s = str(now)
            s = s.replace(" ", "")
            self.mp3file = "readdocs/"+s+".mp3"
            tts.save(self.mp3file)
            file.close()
            print("No text in text file")
        except:
            print("Unable to convert the file.")

    def reader(self):
        try:
            print("starting reading file")
            read = Reader(self.mp3file)
            read.go()
        except:
            print("No text to read")

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
        try:
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
        except:
            print("No file to upload")

    def go(self):
        try:
            self.camera_module()
            self.convert_image_to_text()
            self.convert_text_to_mp3()
            self.reader()
            self.save_file_to_cloud()
            self.running = False
            self.fileDealer.fileWriter("buttons/play")
            print("Again in start event")
        except:
            print("Unable to read from image")
