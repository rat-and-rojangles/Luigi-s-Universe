import pygame
from pygame.locals import *

class Block(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y, imagepath):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.solid=True
        self.lethal=False
        self.type="block"
        self.hasInfo=False
        

        self.bumping=False
        self.bumpDisp=0
        self.bumpDirection=-3
