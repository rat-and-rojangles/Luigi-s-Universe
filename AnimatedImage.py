import pygame, os

#AnimatedScreen takes a folder path filled with multiple frames of an animation.
class AnimatedImage(object):
    def __init__(self, folder):
        self.frame=0
        self.images = []
        for x in os.listdir( folder ):
            self.images.append(pygame.image.load(folder+"/"+x).convert_alpha())
        self.rect=self.images[0].get_rect()

    def draw(self, screen):
        self.frame+=1
        if self.frame==len(self.images):
            self.frame=0

        screen.blit(self.images[self.frame],self.rect)


    def draw_frame(self, frame, screen):
        screen.blit(self.images[frame],self.rect)
