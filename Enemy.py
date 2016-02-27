import pygame, random, copy, os
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    """class for player and collision"""
    def __init__(self, x, y, direction, level):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contact = False
        self.jumping = False

        #self.character="characters/darkman"
        self.character="characters/spiny"
        
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

        self.STUNDURATION=3
        self.stuntimer=0

        self.direction = direction #left or right
        self.image = pygame.image.load(self.character+"/idle_right.png").convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.frame = 0

        self.level=level

        self.HSPEED=3

        self.solid=True
        self.lethal=True
        
        self.type="enemy"
        self.stunned=False
        self.falling=False
        self.alive=True

        #determines when mario kicks this creature
        self.freshkick=False


    def checkScreenWarp(self):
        if self.rect.colliderect( self.level.leftBoundary ):
            self.rect.right=self.level.world_rect.right
        elif self.rect.colliderect( self.level.rightBoundary ):
            self.rect.left=self.level.world_rect.left

    def checkFallout(self):
        if self.rect.top>self.level.bottomBoundary.top:
            self.alive=False

    def update(self,tpt):
        if self.stunned:
            self.stuntimer-=tpt
            if self.stuntimer<=0:
                self.stunned=False
                self.lethal=True
                self.image=pygame.transform.flip(self.image,False,True)
                self.rect.center=self.realcenter
            elif self.stuntimer<=1:
                x=random.randint(-5,5)
                y=random.randint(-5,5)
                self.rect.center=(self.realcenter[0]+x, self.realcenter[1]+y)
            
        elif self.falling:
            self.updateFalling()
        elif self.alive and not self.stunned:
            self.updateAlive()

    def updateAlive(self):
        if self.direction == "right":
            self.image = self.idle_right

        if self.direction == "left":
            self.image = self.idle_left

        if self.direction == "left":
            self.movx = -self.HSPEED
            if self.contact:
                self.frame += 1
                if self.frame == len(self.run_left): self.frame = 0

                self.image = self.run_left[self.frame]
            else:
                self.image = self.image = self.jump_left

        if self.direction == "right":
            self.movx = +self.HSPEED
            if self.contact:
                self.frame += 1
                if self.frame == len(self.run_right): self.frame = 0
                self.image = self.run_right[self.frame]
            else:
                self.image = self.image = self.jump_right

        self.rect.right += self.movx

        self.collide(self.movx, 0)


        if not self.contact:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy


        self.contact = False
        self.collide(0, self.movy)
        self.checkScreenWarp()
        self.checkFallout()

    def updateFalling(self):
        self.rect.y+=8
        if not self.rect.colliderect(self.level.world_rect):
            self.alive=False

    def collide(self, movx, movy):
        self.contact = False
        #for o in self.level.all_sprite:
        
        for o in self.level.world:
            bottombump=None
            
            if self.rect.colliderect(o) and o.solid==True and o!=self:
                if movx > 0:
                    self.rect.right = o.rect.left
                    self.direction = "left"
                if movx < 0:
                    self.rect.left = o.rect.right
                    self.direction = "right"
                if movy > 0 and o.type!="enemy": #doesn"t stand on other enemies
                    bottombump = o.rect.top
                    self.movy = 0
                    self.contact = True

                    if o.type=="block" and o.bumping:
                        self.stunned=True
                        self.lethal=False
                        self.image=pygame.transform.flip(self.image,False,True)
                        self.stuntimer=self.STUNDURATION
                        self.realcenter=(self.rect.center[0],self.rect.center[1]-6)

                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0

            #departing through the pipe
            if self.rect.colliderect(o) and o.type=="pipe":
                if self.direction=="left" and o.direction=="right":
                    if self.rect.right<o.rect.right:
                        self.alive=False
                elif self.direction=="right" and o.direction=="left":
                    if self.rect.left>o.rect.left:
                        self.alive=False

            #last thing to happen
            if bottombump:
                self.rect.bottom=bottombump


