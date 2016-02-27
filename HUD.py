import pygame

class HUD(object):
    def __init__(self):
        self.enemies_defeated=0
        self.time=0
        self.update()

    def timeString(self):
        minutes=str(int(self.time/60))
        if len(minutes)==1:
            minutes="0"+minutes
            
        seconds=str(int(self.time%60))
        if len(seconds)==1:
            seconds="0"+seconds

        return minutes+":"+seconds

    def update(self):
        self.text="Enemies defeated: "+str(self.enemies_defeated)+" Time: "+self.timeString()

        self.font=pygame.font.Font('gamefiles/OCRAEXT.TTF',18)
        self.image=self.font.render(self.text, True, (255,255,255))
        #self.image=self.font.render(self.text, True, (0,255,0),(0,0,127,127)).convert_alpha()

        self.rect=self.image.get_rect()
        self.rect.topleft=(5,5)

        self.shadow=self.font.render(self.text, True, (0,0,0))
    
    def draw(self,screen):
        screen.blit(self.shadow,(self.rect[0],self.rect[1]+2))
        screen.blit(self.shadow,(self.rect[0],self.rect[1]-2))
        screen.blit(self.shadow,(self.rect[0]+2,self.rect[1]))
        screen.blit(self.shadow,(self.rect[0]-2,self.rect[1]))
        screen.blit(self.image,self.rect)
