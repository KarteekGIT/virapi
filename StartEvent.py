from gtts import gTTS
import os
from Reader import Reader
class StartEvent(object):
    def __init__(self):
        pass
    def camera_module(self):
        image = "image/image.jpg"
        if(os.path.exists(image)):
            os.remove(image)
        '''
            Run camera module here to take the picture and save it for processing
        '''    
    def image_filters(self):
        '''
            code for image filtering
        '''
    def convert_image_to_text(self):
        '''
            Code to convert image to mp3 file
        '''
    def convert_text_to_mp3(self):
        text = ""
        file = open('text/textfile.txt')
        for line in file:
            text = text+line
        tts = gTTS(text, lang='en', slow=True)
        self.mp3file = "readdocs/file.mp3"
        tts.save(self.mp3file)
        file.close()     
    def signal_filters(self):
        '''
            code for signal filtering
        '''
    def cloud_saving_and_reader_threads(self):
        read = Reader(self.mp3file)
        read.reading()
        
if __name__=='__main__':
    start = StartEvent()
    start.convert_text_to_mp3()
    start.cloud_saving_and_reader_threads()