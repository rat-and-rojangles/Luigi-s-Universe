import pygame, os
from pygame.locals import *

class CrashmanTutorial(pygame.sprite.Sprite):

    """class for player and collision"""
    def __init__(self, x, y, level, character):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contact = False
        self.jumping = True

        self.character="characters/"+character
        

        #crashman images
        self.run_left = []
        for ipath in os.listdir( self.character+"/run_left" ):
            self.run_left.append(pygame.image.load(self.character+"/run_left/"+ipath).convert_alpha())
            
        self.run_right = []
        for ipath in os.listdir( self.character+"/run_right" ):
            self.run_right.append(pygame.image.load(self.character+"/run_right/"+ipath).convert_alpha())

        self.jump_left=pygame.image.load(self.character+"/jump_left.png").convert_alpha()
        self.jump_right=pygame.image.load(self.character+"/jump_right.png").convert_alpha()
        
        self.down_right=pygame.image.load(self.character+"/down_right.png").convert_alpha()
        self.down_left=pygame.image.load(self.character+"/down_left.png").convert_alpha()

        self.idle_right=pygame.image.load(self.character+"/idle_right.png").convert_alpha()
        self.idle_left=pygame.image.load(self.character+"/idle_left.png").convert_alpha()
        
        pygame.mixer.init()
        #Crashman sound constants
        self.jumpingsound=pygame.mixer.Sound("sound/jump.wav")
        self.kicksound=pygame.mixer.Sound("sound/kick.wav")

        #starting image
        self.direction = "right"
        self.image = self.idle_right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.frame = 0

        self.level=level
        self.world=level.world

        self.HSPEED=10
        #self.JUMPSTRENGTH=20
        self.JUMPSTRENGTH=22

        self.type=self.character+""
        self.alive=True
        self.falling=False


    def checkScreenWarp(self):
        if self.rect.colliderect( self.level.leftBoundary ):
            self.rect.right=self.level.world_rect.right
        elif self.rect.colliderect( self.level.rightBoundary ):
            self.rect.left=self.level.world_rect.left
        

    def checkFallout(self):
        if self.rect.top>self.level.bottomBoundary.top:
            self.alive=False
            #self.image=pygame.image.load("world/nothing.png")
    
    def update(self, up, down, left, right):
        if up:
            if self.contact:
                if self.direction == "right":
                    self.image = self.jump_right
                self.jumping = True
                self.movy -= self.JUMPSTRENGTH
                self.jumpingsound.play()
        if down:
            if self.contact and self.direction == "right":
                self.image = self.down_right
            if self.contact and self.direction == "left":
                self.image = self.down_left

        if not down and self.direction == "right":
            self.image = self.idle_right

        if not down and self.direction == "left":
            self.image = self.idle_left

        if left:
            self.direction = "left"
            self.movx = -self.HSPEED
            if self.contact:
                self.frame += 1
                if self.frame == len(self.run_left): self.frame = 0
                self.image = self.run_left[self.frame]
            else:
                self.image = self.image = self.jump_left

        if right:
            self.direction = "right"
            self.movx = +self.HSPEED
            if self.contact:
                self.frame += 1
                if self.frame == len(self.run_right): self.frame = 0
                self.image = self.run_right[self.frame]
            else:
                self.image = self.image = self.jump_right

        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0)

            
        if not self.contact:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.jumping:
            self.movy += 2
            self.rect.top += self.movy
            if self.contact == True:
                self.jumping = False

        self.contact = False
        self.collide(0, self.movy)

        #for the image only
        if not self.contact:
            if self.direction == "right":
                self.image = self.jump_right
            else:
                self.image = self.jump_left


        self.checkScreenWarp()
        self.checkFallout()


    def collide(self, movx, movy):
        self.contact = False
        topbump=None

        #blocks then enemies
        for o in self.world:
            if self.rect.colliderect(o) and (o.solid==True and o.type!="enemy") and o!=self:

                #block interaction
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                if movy < 0:
                    topbump = o.rect.bottom
                    self.movy = 0
                    if o.type=="block":
                        o.bumping=True
                        if o.hasInfo:
                            self.level.currentInfoBlock=o

        

        if topbump:    
            self.rect.top = topbump

        for o in self.world:
            if self.rect.colliderect(o) and o.solid==True and o!=self:
                #dangerous touch
                if o.lethal:
                    self.alive=False
                    self.falling=True

                #mario kick
                if o.type=="enemy" and o.stunned:
                    self.kicksound.play()
                    o.falling=True
                    o.freshkick=True
                    o.stunned=False
                    o.solid=False



    def updateFalling(self):
        if self.rect.colliderect(self.level.world_rect):
            self.rect.y+=8
        else:
            self.falling=False

