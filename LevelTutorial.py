#FORMAT FOR levelFile HEADERS

#splashscreen path
#maximum length of levelFile
#bg image

#music

#block1 image
#block2 image
#block3 image
#gametype and victorycount
""" """
#index of characters
#1,2,3: blocks
#L,R: enemy ports (also generates cosmetic pipes)
#l,r: exit pipes
#P: player start

import pygame, string
from pygame.locals import *
from Block import *
from Pipe import *
from CrashmanTutorial import *
from Enemy import *
from AnimatedScreen import *
from InfoBlock import *

def stripTrailingSpaces(strung):
    if strung.endswith(" "):
        return stripTrailingSpaces(strung[:-1])
    else:
        return strung


class LevelTutorial(object):
    #static list of keywords
    KEYWORDS = ["message","splashscreen","music","bg","gametype","maxwidth","elemental","enemymax","spawndelay","nextlevel"]
    DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
    
    '''Read a map and create a levelFile'''
    def __init__(self, open_level, character, initialText):
        self.levelLines = []
        self.world = []
        self.all_sprite = pygame.sprite.Group()
        self.enemy_ports=[]
        self.levelPath=open_level
        self.levelFile = open(self.levelPath, "r")
        self.messages=[]
        self.elemental=False
        self.enemy_max=1
        self.spawn_delay=3
        self.character=character
        self.create_level()
        self.get_size()
        self.generateWorldRect()



        self.nextLevelPath=self.levelPath

        self.currentInfoBlock=InfoBlock(-100,-100,initialText)

    def readHeaders(self):
        #makes a list of header lines
        current=""
        headers=[]
        while current!="HEADER END":
            current=self.levelLines.pop(0)
            headers.append(current)

        elementalPath=""

        #carries out the action of each header
        for h in headers:
            if len(h.split())>=1 and h.split()[0] in LevelTutorial.KEYWORDS:
                if h.split()[0]=="message":
                    newstr=string.replace(h[8:], "@", "\n")
                    #self.messages.append(h[8:])
                    self.messages.append(newstr)
                elif h.split()[0]=="splashscreen":
                    self.splashscreenImg= pygame.transform.scale(pygame.image.load(h.split()[1]), (1024,600))
                elif h.split()[0]=="music":
                    self.musicPath=h.split()[1]
                elif h.split()[0]=="bg":
                    self.bgPath=h.split()[1]
                    self.bgInit()
                elif h.split()[0]=="gametype":
                    self.objectiveType=h.split()[1]
                    self.objectiveMax=int(h.split()[2])
                elif h.split()[0]=="elemental":
                    self.elemental=True
                    elementalPath=h.split()[1]
                elif h.split()[0]=="enemymax":
                    self.enemy_max=int(h.split()[1])
                elif h.split()[0]=="spawndelay":
                    self.spawn_delay=float(h.split()[1])
                elif h.split()[0]=="nextlevel":
                    self.nextLevelPath=h.split()[1]

        if self.elemental:
            self.elementalOverlay=AnimatedScreen(elementalPath,self.bgRect)

    def create_level(self):
        for l in self.levelFile:
            newStr=l
            if newStr.endswith("\n"):
                newStr=newStr[:-1]
            self.levelLines.append(stripTrailingSpaces(newStr))

        self.readHeaders()
        #print self.messages

        x=0
        y=0
        #an enemy port tells the game where to spawn enemies
        for row in self.levelLines:
            for col in row:
                if col == "X":
                    obstacle = Block(x, y, "world/blocks/cinder.png")
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col == "C":
                    obstacle = Block(x, y, "level/tutorial/sign.png")
                    obstacle.solid=False
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col in LevelTutorial.DIGITS:
                    obstacle = InfoBlock(x, y, self.messages[int(col)])
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col == "P":
                    self.crashman = CrashmanTutorial(x,y,self,self.character)
                    self.all_sprite.add(self.crashman)
                if col == "L":
                    pep = Pipe(x, y-75, "world/pipes/leftpipe.png","left")
                    self.world.append(pep)
                    self.all_sprite.add(self.world)
                    self.enemy_ports.append( (x,y, "left") )
                if col == "R":
                    pep = Pipe(x-125, y-75, "world/pipes/rightpipe.png","right")
                    self.world.append(pep)
                    self.all_sprite.add(self.world)
                    self.enemy_ports.append( (x,y, "right") )
                if col == "l":
                    pep = Pipe(x+25, y-75, "world/pipes/leftpipe.png","left")
                    self.world.append(pep)
                    self.all_sprite.add(self.world)
                if col == "r":
                    pep = Pipe(x-125, y-75, "world/pipes/rightpipe.png","right")
                    self.world.append(pep)
                    self.all_sprite.add(self.world)

                x += 25
            y += 25
            x = 0

    def bgInit(self):
        rawBG=pygame.image.load(self.bgPath)
        self.bgImg= pygame.transform.scale(rawBG, (1024,600))
        self.bgRect= self.bgImg.get_rect()
        self.bgRect.center=(512,300)


    def get_size(self):
        lines = self.levelLines

        self.width=len(max(lines, key=len))*25
        self.height = (len(lines))*25
        return (self.width, self.height)

    def generateWorldRect(self):
        self.world_rect=Rect(0, 0, self.width, self.height)
        self.leftBoundary=Rect(-self.width-self.crashman.rect.width/2+1,0, self.width, self.height)
        self.rightBoundary=Rect(self.width+self.crashman.rect.width/2-1, 0, self.width, self.height)
        self.bottomBoundary=Rect(0, self.height+5, self.width, self.height)

    def drawBG(self, screen):
        screen.blit(self.bgImg, self.bgRect)

    def reset(self):
        self.__init__(self.levelPath)

    def drawInfo(self,screen):
        self.currentInfoBlock.drawMessage(screen)


