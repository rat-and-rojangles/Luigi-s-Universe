#index of characters
#1,2,3: blocks
#L,R: enemy ports (also generates cosmetic pipes)
#l,r: exit pipes
#P: player start
#f: instant win flag

import pygame
from pygame.locals import *
from Block import *
from Pipe import *
from Crashman import *
from Enemy import *
from AnimatedScreen import *

def stripTrailingSpaces(strung):
    if strung.endswith(" "):
        return stripTrailingSpaces(strung[:-1])
    else:
        return strung


class Level(object):
    #static list of keywords
    KEYWORDS = ["block","splashscreen","music","bg","gametype","maxwidth","elemental","enemymax","spawndelay","nextlevel","video"]
    DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
    
    '''Read a map and create a levelFile'''
    def __init__(self, open_level, character):
        self.levelLines = []
        self.world = []
        self.all_sprite = pygame.sprite.Group()
        self.enemy_ports=[]
        self.levelPath=open_level
        self.levelFile = open(self.levelPath, "r")
        self.blockStyles=[]
        self.elemental=False
        self.hasVideo=False
        self.enemy_max=1
        self.spawn_delay=3
        self.character=character

        #default
        self.nextLevelPath=self.levelPath

        self.create_level()
        self.get_size()
        self.generateWorldRect()

        

        

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
            if len(h.split())>=1 and h.split()[0] in Level.KEYWORDS:
                if h.split()[0]=="block":
                    self.blockStyles.append(h.split()[1])
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
                elif h.split()[0]=="video":
                    self.hasVideo=True
                    self.videoPath=h.split()[1]
                    self.videoInit()

        if self.elemental:
            self.elementalOverlay=AnimatedScreen(elementalPath,self.bgRect)

    def create_level(self):
        for l in self.levelFile:
            newStr=l
            if newStr.endswith("\n"):
                newStr=newStr[:-1]
            self.levelLines.append(stripTrailingSpaces(newStr))

        self.readHeaders()

        x=0
        y=0
        #an enemy port tells the game where to spawn enemies
        for row in self.levelLines:
            for col in row:
                if col in Level.DIGITS:
                    obstacle = Block(x, y, self.blockStyles[int(col)])
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col == "f":
                    obstacle = Block(x, y, "world/flag.png")
                    obstacle.type="flag"
                    obstacle.solid=False
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                if col == "P":
                    self.crashman = Crashman(x,y,self,self.character)
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

    """def generateWorldRect(self):
        self.world_rect=Rect(0, 0, self.width, self.height)
        self.leftBoundary=Rect(-self.width-20,0, self.width, self.height)
        self.rightBoundary=Rect(self.width+20, 0, self.width, self.height)
        self.bottomBoundary=Rect(0, self.height+5, self.width, self.height)"""

    def generateWorldRect(self):
        self.world_rect=Rect(0, 0, self.width, self.height)
        self.leftBoundary=Rect(-self.width-self.crashman.rect.width/2+1,0, self.width, self.height)
        self.rightBoundary=Rect(self.width+self.crashman.rect.width/2-1, 0, self.width, self.height)
        self.bottomBoundary=Rect(0, self.height+5, self.width, self.height)

    def drawBG(self, screen):
        if self.hasVideo:
            newsurf=pygame.Surface((1024,600))
            newsurf.blit(pygame.transform.scale(self.movie_screen, (self.movieRect.width,self.movieRect.height)),self.movieRect)
            self.bgImg=newsurf
            
        screen.blit(self.bgImg, self.bgRect)

    def reset(self):
        self.__init__(self.levelPath,self.character)

    def videoInit(self):
        self.movie = pygame.movie.Movie(self.videoPath)
        self.movie_screen=pygame.Surface(self.movie.get_size()).convert()
        self.movieRect=Rect(512,300,1142,718)
        self.movieRect.center=(512,300)
        self.movie.set_display(self.movie_screen)
        self.movie.play()

    def drawVideo(self):
        screen.blit(pygame.transform.scale(self.movie_screen, (self.movieRect.width,self.movieRect.height)),self.movieRect)


