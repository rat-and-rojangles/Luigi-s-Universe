import pygame
from pygame.locals import *

class Pipe(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y, imagepath, direction):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.solid=False
        self.lethal=False
        self.direction=direction

        self.type="pipe"
        
        

        
