import pygame
class Reader(object):
    def __init__(self, filename):
        self.filename = filename
    def reading(self):
        #pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("Done")
    def play_or_stop(self):
        '''
            Code to play or stop the reading thread
        '''
    def forward_or_backward(self):
        '''
            Code to forward or backward reading by 10 seconds
        '''