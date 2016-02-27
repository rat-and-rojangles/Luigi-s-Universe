import pygame, os, sys
from pygame.locals import *
from TextOption import *
from AnimatedImage import *
import Game,GameTutorial

SCREEN_SIZE = (1280, 720) #resolution of the game

global FPS
global clock
global time_spent

WHITE=(255,255,255)
GRAY=(127,127,127)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

YELLOW=(255,255,0)

LIGHT_RED=(255,127,127)
LIGHT_GREEN=(127,255,127)
LIGHT_BLUE=(0,127,255)

FPS=30

default_character="Luigi"

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

def levelName(oddstr):
    return oddstr[2:-4].replace("+"," ")

def titleScreen(screen,CHARACTER):
    #print CHARACTER
    
    #pygame.mixer.music.load('music/resurrection_state.wav')
    pygame.mixer.music.load('music/awakening_of_the_earth_spirits2.wav')
    pygame.mixer.music.play(-1)
    rawBG=pygame.image.load("menu/titleBG.jpg")
    bgImg= pygame.transform.scale(rawBG, (1024,600))
    bgRect=bgImg.get_rect()
    bgRect.center=(512,300)

    clock = pygame.time.Clock()

    movie = pygame.movie.Movie('video/visualizerfast1.mpg')
    #movie = pygame.movie.Movie("video/pacman.mpg")
    movie_screen=pygame.Surface(movie.get_size()).convert()
    #movieRect=movie_screen.get_rect()
    movieRect=Rect(bgRect.center[0],bgRect.center[1],1142,718)
    movieRect.center=bgRect.center
    movie.set_display(movie_screen)
    movie.play()
    
    
    #one third of the way from the top
    #titleLogoImage=pygame.image.load("menu/titleLogo.png").convert_alpha()
    titleLogoImage=pygame.image.load("menu/luigiverse2.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,bgRect.height/3)
    

    #options 
    #options=(TextOption("Play Game","level1"),TextOption("Level Select","levelselect"),TextOption("Character Select","characterselect"),TextOption("Tutorial","tutorial"),TextOption("Credits","credits"),TextOption("QUIT","quit"))
    options=(TextOption("Play Game","level1"),TextOption("Level Select","levelselect"),TextOption("Character Select","characterselect"),TextOption("Tutorial","tutorial"),TextOption("QUIT","quit"))
    options[len(options)-1].setSelectedColor(RED)

    #alignment of menu options
    verticalspace=bgRect.height-titleLogoRect.bottom
    heightOfOptions=0
    for op in options:
        heightOfOptions=heightOfOptions+op.rect.height+5

    currentY=int((verticalspace-heightOfOptions)/2+titleLogoRect.bottom)

    for op in options:
        op.rect.top=currentY
        currentY=currentY+op.rect.height+5

    selectedIndex=0
    screen.blit(bgImg,bgRect)

    fireR=AnimatedImage("menu/greenfireSmall")
    fireL=AnimatedImage("menu/greenfireSmall")

    
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #control selection
            if event.type == KEYDOWN and event.key == K_UP:
                TextOption.cursorSound.play()
                if selectedIndex==0:
                    selectedIndex=len(options)-1
                else:
                    selectedIndex-=1
            if event.type == KEYDOWN and event.key == K_DOWN:
                TextOption.cursorSound.play()
                if selectedIndex==len(options)-1:
                    selectedIndex=0
                else:
                    selectedIndex+=1
            if event.type == KEYDOWN and event.key == K_RETURN:
                TextOption.selectSound.play()
                if options[selectedIndex].action=="level1":
                    pygame.mixer.music.stop()
                    Game.initiateLevel(screen,"level/01Luigi+Bros.txt",CHARACTER)
                elif options[selectedIndex].action=="levelselect":
                    levelSelect(screen,CHARACTER)
                elif options[selectedIndex].action=="characterselect":
                    characterSelect(screen,CHARACTER)
                elif options[selectedIndex].action=="tutorial":
                    pygame.mixer.music.load("music/resurrection_state.wav")
                    pygame.mixer.music.play(-1)
                    GameTutorial.playGame(screen,CHARACTER,"Welcome to Luigi's Universe. \nHit the ? blocks for more information.")
                elif options[selectedIndex].action=="quit":
                    pygame.quit()
                    sys.exit()


        tpt=tps(clock,FPS)

        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        if not movie.get_busy():
            movie.rewind()
            movie.play()

        screen.blit(pygame.transform.scale(movie_screen, (movieRect.width,movieRect.height)),movieRect)
        
        
        fireR.rect.center=(0,options[selectedIndex].rect.center[1]-18)
        fireL.rect.center=(0,options[selectedIndex].rect.center[1]-18)

        fireR.rect.left=options[selectedIndex].rect.right+15
        fireL.rect.right=options[selectedIndex].rect.left-15

        fireR.draw(screen)
        fireL.draw(screen)

        screen.blit(titleLogoImage,titleLogoRect)
        for op in options:
            op.draw(screen)


        pygame.display.flip()


def levelSelect(screen, CHARACTER):
    pygame.mixer.music.load('music/beans.wav')
    pygame.mixer.music.play(-1)
    rawBG=pygame.image.load("menu/levelSelectBG.png")
    bgImg= pygame.transform.scale(rawBG, (1024,600))
    bgRect=bgImg.get_rect()
    bgRect.center=(512,300)
    
    
    #one sixth of the way from the top
    titleLogoImage=pygame.image.load("menu/levelSelectLogo.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,bgRect.height/6)
    

    options=[]
    levels = os.listdir( "level" )
    levels.sort()
    for txtFile in levels:
        if ".txt" in txtFile:
            #options.append(TextOption(txtFile,"level/"+txtFile))
            options.append(TextOption(levelName(txtFile),"level/"+txtFile))
    options.append(TextOption("BACK","titlescreen"))

    options[len(options)-1].setSelectedColor(LIGHT_BLUE)
    options[len(options)-1].setUnselectedColor(GRAY)


    #alignment of menu options
    verticalspace=bgRect.height-titleLogoRect.bottom
    heightOfOptions=0
    for op in options:
        heightOfOptions=heightOfOptions+op.rect.height+5

    currentY=int((verticalspace-heightOfOptions)/2+titleLogoRect.bottom)

    for op in options:
        op.rect.top=currentY
        currentY=currentY+op.rect.height+5

    selectedIndex=0

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #control selection
            if event.type == KEYDOWN and event.key == K_UP:
                TextOption.cursorSound.play()
                if selectedIndex==0:
                    selectedIndex=len(options)-1
                else:
                    selectedIndex-=1
            if event.type == KEYDOWN and event.key == K_DOWN:
                TextOption.cursorSound.play()
                if selectedIndex==len(options)-1:
                    selectedIndex=0
                else:
                    selectedIndex+=1
            if event.type == KEYDOWN and event.key == K_RETURN:
                TextOption.selectSound.play()
                if options[selectedIndex].action=="titlescreen":
                   titleScreen(screen,CHARACTER)
                else:
                    pygame.mixer.music.stop()
                    Game.initiateLevel(screen,options[selectedIndex].action, CHARACTER)


        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        screen.blit(bgImg,bgRect)
        screen.blit(titleLogoImage,titleLogoRect)
        for op in options:
            op.draw(screen)

        pygame.display.flip()

def characterSelect(screen, CHARACTER):
    #pygame.mixer.music.load('music/resurrection_state.wav')
    pygame.mixer.music.load('music/dancefloor.wav')
    pygame.mixer.music.play(-1)
    rawBG=pygame.image.load("menu/tech.png")
    bgImg= pygame.transform.scale(rawBG, (1024,600))
    bgRect=bgImg.get_rect()
    bgRect.center=(512,300)

    clock = pygame.time.Clock()

    #one third of the way from the top
    titleLogoImage=pygame.image.load("menu/characterSelectLogo.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,bgRect.height/6)
    
    
    fireIndex=0
    selectedIndex=0
    count=0

    options=[]
    characters = os.listdir( "characters" )
    characters.sort()
    for folder in characters:
        if "." not in folder:
            options.append(TextOption(folder,"characters/"+folder+"/run_right"))
            if folder==CHARACTER:
                fireIndex=count
                selectedIndex=count
            count+=1
    #options.append(TextOption("BACK","titlescreen"))
    options.append(TextOption("OK","titlescreen"))

    #options[len(options)-1].setSelectedColor(LIGHT_BLUE)
    options[len(options)-1].setSelectedColor(YELLOW)
    options[len(options)-1].setUnselectedColor(GRAY)

    #alignment of menu options
    verticalspace=bgRect.height-titleLogoRect.bottom
    heightOfOptions=0
    for op in options:
        heightOfOptions=heightOfOptions+op.rect.height+5

    currentY=int((verticalspace-heightOfOptions)/2+titleLogoRect.bottom)

    for op in options:
        op.rect.top=currentY
        currentY=currentY+op.rect.height+5
        op.rect.right-=128

    
    screen.blit(bgImg,bgRect)

    

    characterPreview=AnimatedImage("characters/"+CHARACTER+"/run_right")
    fireL=AnimatedImage("menu/greenfireSmall")

    
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #control selection
            if event.type == KEYDOWN and event.key == K_UP:
                TextOption.cursorSound.play()
                if selectedIndex==0:
                    selectedIndex=len(options)-1
                else:
                    selectedIndex-=1
            if event.type == KEYDOWN and event.key == K_DOWN:
                TextOption.cursorSound.play()
                if selectedIndex==len(options)-1:
                    selectedIndex=0
                else:
                    selectedIndex+=1
            if event.type == KEYDOWN and event.key == K_RETURN:
                TextOption.selectSound.play()
                if options[selectedIndex].action=="titlescreen":
                   titleScreen(screen,CHARACTER)
                else:
                    characterPreview=AnimatedImage(options[selectedIndex].action)
                    fireIndex=selectedIndex
                    CHARACTER=options[selectedIndex].text


        tpt=tps(clock,FPS)

        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        screen.blit(bgImg,bgRect)

        fireL.rect.center=(0,options[fireIndex].rect.center[1]-18)
        fireL.rect.right=options[fireIndex].rect.left-15
        fireL.draw(screen)

        
        
        characterPreview.rect.center=(768,300)
        characterPreview.draw(screen)

        screen.blit(titleLogoImage,titleLogoRect)
        for op in options:
            op.draw(screen)


        pygame.display.flip()



def runGame():
    pygame.init()
    pygame.display.set_caption("Luigi's Universe")
    pygame.display.set_icon(pygame.image.load("gamefiles/luigiFlame.png"))
    screen = pygame.display.set_mode((1024, 600)) #windowed

    titleScreen(screen, default_character)



