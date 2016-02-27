import pygame

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)


class TextOption(object):
    pygame.mixer.init()
    cursorSound=pygame.mixer.Sound('sound/cursor.wav')
    selectSound=pygame.mixer.Sound('sound/select.wav')
    pauseSound=pygame.mixer.Sound('sound/brawl_start.wav')
    
    def __init__(self,text,action):
        self.text=text
        self.font=pygame.font.Font('gamefiles/OCRAEXT.TTF',24)
        self.imageUnselected=self.font.render(self.text, True, WHITE)
        self.imageSelected=self.font.render(self.text, True, GREEN)
        self.shadow=self.font.render(self.text, True, BLACK)

        self.rect=self.imageUnselected.get_rect()
        self.rect.center=(512,300)

        self.selected=False

        self.action=action

    def setSelectedColor(self,color):
        self.imageSelected=self.font.render(self.text, True, color)

    def setUnselectedColor(self,color):
        self.imageUnselected=self.font.render(self.text, True, color)

    def draw(self, screen):
        #draws shadow first
        screen.blit(self.shadow,(self.rect[0],self.rect[1]+2))
        screen.blit(self.shadow,(self.rect[0],self.rect[1]-2))
        screen.blit(self.shadow,(self.rect[0]+2,self.rect[1]))
        screen.blit(self.shadow,(self.rect[0]-2,self.rect[1]))
        
        if self.selected:
            screen.blit(self.imageSelected,self.rect)
        else:
            screen.blit(self.imageUnselected,self.rect)


