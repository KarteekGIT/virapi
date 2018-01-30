from pygame import mixer
class Reader(object):
    def __init__(self, filename):
        self.filename = filename
    def reading(self):
        mixer.init()
        mixer.music.load(self.filename)
        mixer.music.play()
        print(self.filename, type(self.filename))
        print("Done")
    def play_or_stop(self):
        '''
            Code to play or stop the reading thread
        '''
    def forward_or_backward(self):
        '''
            Code to forward or backward reading by 10 seconds
        '''