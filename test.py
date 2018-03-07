from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from playsound import playsound

def tester():
    folderid = None    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()                            
    for file in file_list:
        if(file['title'] == "vira"):
            folderid = file['id']
            break
    file_list2 = drive.ListFile({'q': "'%s' in parents  and trashed=false" % folderid}).GetList()
    file_list2 = list(file_list2)
    print(len(file_list2))
    print(file_list2[1]['id'])
    file = drive.CreateFile({'id' : file_list2[1]['id']})
    file.GetContentFile('download/'+file_list2[1]['title'])

def tester2():
    fileList = os.listdir("download/readdocs")
    numOfFiles = len(fileList)
    print(numOfFiles)
    if(numOfFiles > 10):
        for file in fileList:
            os.remove("download/readdocs"+file)

def tester3():
    playsound("userhints/main.mp3")
                                
if __name__=='__main__':tester3()
