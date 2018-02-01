from gtts import gTTS
import os
import multiprocessing as mp
from Reader import Reader
import datetime
class StartEvent(object):
    def __init__(self):
        self.image = "image/image.jpg"
        self.text = "text/textfile.txt"
        
    def camera_module(self):
        #if(os.path.exists(self.image)):
        #    os.remove(self.image)
        #if(os.path.exists(self.text)):
        #    os.remove(self.text)
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
        pass
        '''
            Code to convert image to mp3 file
        '''
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
        pass
        ''''
        code that saves file to cloud
        
        '''
        
    def execute_start(self):
        while True:
            fileOpen = open("buttons/start", "r+")
            start = fileOpen.read(5)
            start = start.strip("\n")
            if(start == "True"):
                self.camera_module()
                self.image_filters()
                self.convert_image_to_text()
                self.convert_text_to_mp3()
                self.signal_filters()
                self.reader()

                fileOpen.seek(0)
                fileOpen.write('False')
                fileOpen.truncate()
                fileOpen.close()
                print("again in start event")
            
    def go(self):
        print("starting")
        execute = mp.Process(target=self.execute_start, name="process for start button")
        execute.start()
        if execute.is_alive():
            execute.join()
            
if __name__=="__main__":
    start = StartEvent()
    start.go()