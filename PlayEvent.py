import threading
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class PlayEvent(object):
    def __init__(self):
        self.folderid = None    
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.liveThreads = []
        self.drive = GoogleDrive(gauth)
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()                            
        for file in file_list:
            if(file['title'] == "vira"):
                folderid = file['id']
                break
        file_list2 = self.drive.ListFile({'q': "'%s' in parents  and trashed=false" % folderid}).GetList()
        self.cursor = list(file_list2)
           
    def download(self, id, title):
        if(os.path.exists('buffer/'+title)):
            return 'buffer/'+title
        file = self.drive.CreateFile({'id' : id})
        file.GetContentFile('buffer/'+title)
        return 'buffer/'+title
