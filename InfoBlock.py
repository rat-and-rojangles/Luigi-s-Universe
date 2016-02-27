import pygame
from pygame.locals import *

WHITE=(255,255,255)
BLACK=(0,0,0)

class InfoBlock(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("world/blocks/questionBlock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.solid=True
        self.lethal=False
        self.type="block"
        self.hasInfo=True
        self.infoText=text

        #self.font=pygame.font.Font('gamefiles/OCRAEXT.TTF',24)
        self.font=pygame.font.Font('gamefiles/OCRAEXT.TTF',18)
        """self.textImage=self.font.render(self.infoText, True, WHITE)
        self.shadow=self.font.render(self.infoText, True, BLACK)"""

        self.textImage=self.renderText(WHITE)
        self.shadow=self.renderText(BLACK)
        
        self.textRect=self.textImage.get_rect()
        self.fullTextImage=self.combineShadow()
        self.textRect=self.fullTextImage.get_rect()
        
        self.textRect.center=(512,0)
        self.textRect.bottom=590
        
    
        self.bumping=False
        self.bumpDisp=0
        self.bumpDirection=-3

    def renderText(self, color):
        lines = self.infoText.splitlines()
        #first we need to find image size...
        width = height = 0
        for l in lines:
            width = max(width, self.font.size(l)[0])
            height += self.font.get_linesize()
        #create 8bit image for non-aa text..
        img = pygame.Surface((width, height),SRCALPHA).convert_alpha()
        #render each line
        height = 0
        for l in lines:
            t = self.font.render(l, True, color).convert_alpha()
            img.blit(t, (0, height))
            height += self.font.get_linesize()
        return img

    def combineShadow(self):
        img = pygame.Surface((self.textRect.width, self.textRect.height),SRCALPHA).convert_alpha()
        img.blit(self.shadow,(self.textRect[0],self.textRect[1]+2))
        img.blit(self.shadow,(self.textRect[0],self.textRect[1]-2))
        img.blit(self.shadow,(self.textRect[0]+2,self.textRect[1]))
        img.blit(self.shadow,(self.textRect[0]-2,self.textRect[1]))
        img.blit(self.textImage,self.textRect)
        #img.set_alpha(127)
        return img#.convert_alpha()
        
        
    """def drawMessage(self, screen):
        #draws shadow first
        screen.blit(self.shadow,(self.textRect[0],self.textRect[1]+2))
        screen.blit(self.shadow,(self.textRect[0],self.textRect[1]-2))
        screen.blit(self.shadow,(self.textRect[0]+2,self.textRect[1]))
        screen.blit(self.shadow,(self.textRect[0]-2,self.textRect[1]))

        screen.blit(self.textImage,self.textRect)"""

    def drawMessage(self, screen):
        screen.blit(self.fullTextImage,self.textRect)

