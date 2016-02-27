import pygame
from pygame.locals import *
import sys, os, math, random
import MainScreen

#from MainScreen import *

from Level import *
from Enemy import *
from HUD import *
from TextOption import *

WHITE=(255,255,255)
GRAY=(127,127,127)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

LIGHT_RED=(255,127,127)
LIGHT_GREEN=(127,255,127)
LIGHT_BLUE=(127,127,255)



DRAWPRIORITY=["crashman","pipe","enemy"]

FPS = 30

pygame.mixer.init()
unpauseSound=pygame.mixer.Sound('sound/unpause.wav')

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    '''Class for center screen on the player'''
    def __init__(self, screen, player, level):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = level.world_rect

    def update(self):
      if self.player.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.player.centerx - 25
      if self.player.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.player.centerx + 25
      if self.player.centery > self.rect.centery + 25:
          self.rect.centery = self.player.centery - 25
      if self.player.centery < self.rect.centery - 25:
          self.rect.centery = self.player.centery + 25
      self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                if s.type=="block" and s.bumping:
                    surf.blit(s.image, (RelRect(s, self).x,RelRect(s, self).y+s.bumpDisp))
                    if s.bumpDisp==0 and s.bumpDirection>0:
                        s.bumping=False
                        s.bumpDisp=0
                        s.bumpDirection=-3
                    elif s.bumpDisp==-12:
                        s.bumpDirection=3
                        s.bumpDisp=-9
                    else:
                        s.bumpDisp+=s.bumpDirection
                else:
                    surf.blit(s.image, RelRect(s, self))

    #crashman is always on top. pipes are next priority, then enemies
    def draw_sprites_prio(self, surf, sprites, crashman):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                if s.type not in DRAWPRIORITY:
                    if s.type=="block" and s.bumping:
                        surf.blit(s.image, (RelRect(s, self).x,RelRect(s, self).y+s.bumpDisp))
                        if s.bumpDisp==0 and s.bumpDirection>0:
                            s.bumping=False
                            s.bumpDisp=0
                            s.bumpDirection=-3
                        elif s.bumpDisp==-12:
                            s.bumpDirection=3
                            s.bumpDisp=-9
                        else:
                            s.bumpDisp+=s.bumpDirection
                    else:
                        surf.blit(s.image, RelRect(s, self))
        for s in sprites:
            if s.rect.colliderect(self.rect):
                if s.type=="enemy":
                    surf.blit(s.image, RelRect(s, self))
        for s in sprites:
            if s.rect.colliderect(self.rect):
                if s.type=="pipe":
                    surf.blit(s.image, RelRect(s, self))

        surf.blit(crashman.image,RelRect(crashman,self))

#message with stransparent bg
def messageScreenOverlay(screen, message):
    fontObj=pygame.font.Font('gamefiles/OCRAEXT.TTF', 32)
    textSurfaceObj=fontObj.render(message, False, WHITE)
    textShadow=fontObj.render(message, False, BLACK)
    textRectObj=textSurfaceObj.get_rect()
    textRectObj.center=screen.get_rect().center


    screen.blit(textShadow,(textRectObj[0],textRectObj[1]+2))
    screen.blit(textShadow,(textRectObj[0],textRectObj[1]-2))
    screen.blit(textShadow,(textRectObj[0]+2,textRectObj[1]))
    screen.blit(textShadow,(textRectObj[0]-2,textRectObj[1]))
    screen.blit(textSurfaceObj,textRectObj)
    
    pygame.display.update()
    waitForKey()

def drawRenderedMessage(screen, messageImg, messageShadow, rect):
    screen.blit(messageShadow,(rect[0],rect[1]+2))
    screen.blit(messageShadow,(rect[0],rect[1]-2))
    screen.blit(messageShadow,(rect[0]+2,rect[1]))
    screen.blit(messageShadow,(rect[0]-2,rect[1]))
    screen.blit(messageImg,rect)
    
    pygame.display.update()

def waitForKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

def waitForKeys(keyConstants):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and (event.key in keyConstants):
                return

def waitForKeysDown(keyConstants):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key in keyConstants):
                return

def pauseScreen(screen, level):
    pygame.mixer.music.pause()
    TextOption.pauseSound.play()
    rawBG=pygame.image.load("menu/darkenScreen.png")
    bgImg= pygame.transform.scale(rawBG, (1024,600))
    bgRect=bgImg.get_rect()
    bgRect.center=(512,300)
    screen.blit(bgImg,bgRect)
    pygame.display.flip()
    
    
    #one third of the way from the top
    titleLogoImage=pygame.image.load("menu/pause.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,bgRect.height/3)
    


    options=(TextOption("Resume","resume"),TextOption("Restart Level","restart"),TextOption("Main Menu","mainmenu"),TextOption("QUIT","quit"))
    options[3].setSelectedColor(RED)
    #options[2].setUnselectedColor(GRAY)

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
    screen.blit(titleLogoImage,titleLogoRect)
    while True: #think of condition later
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
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if options[selectedIndex].action=="resume":
                    unpauseSound.play()
                    pygame.mixer.music.unpause()
                    return
            if event.type == KEYDOWN and event.key == K_RETURN:
                TextOption.selectSound.play()
                if options[selectedIndex].action=="resume":
                    unpauseSound.play()
                    pygame.mixer.music.unpause()
                    return
                elif options[selectedIndex].action=="restart":
                    playGame(screen,level)
                elif options[selectedIndex].action=="mainmenu":
                    #import MainScreen
                    print "newChara: "+level.crashman.character
                    MainScreen.titleScreen(screen,level.crashman.character)
                elif options[selectedIndex].action=="quit":
                    pygame.quit()
                    sys.exit()

        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        #screen.blit(bgImg,bgRect)
        #screen.blit(titleLogoImage,titleLogoRect)
        for op in options:
            op.draw(screen)

        pygame.display.flip()



def objectiveProgress(oType,numDefeated,totalTime):
    if oType=="exterminate":
        return numDefeated
    elif oType=="survival":
        return totalTime

def objectiveComplete(oCount,oMax):
    if oCount>=oMax:
        return True
    else:
        return False
    
def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

def win(screen, camera, level, enemy_list, clock, hud, character):
    pygame.mixer.music.load('sound/smb_stage_clear.wav')
    pygame.mixer.music.play(0)

    #one third of the way from the top
    titleLogoImage=pygame.image.load("menu/victory.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,level.bgRect.height/3)

    screen.blit(titleLogoImage,titleLogoRect)
    
    stillFallingEnemies=False
    for e in enemy_list:
        if e.falling==True:
            stillFallingEnemies=True
            
    while stillFallingEnemies==True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key==K_SPACE):
                exitKey = True

        tpt = tps(clock, FPS)
        
            
        for e in enemy_list:
            if e.falling==True:
                e.updateFalling()
            if e.alive==False:
                stillFallingEnemies=False
                #enemy_list.remove(e)

                
        level.drawBG(screen)
        hud.draw(screen)

        
        #draw everything
        camera.draw_sprites_prio(screen, level.all_sprite, level.crashman)

        screen.blit(titleLogoImage,titleLogoRect)

        if level.elemental:
            level.elementalOverlay.draw_frame(level.elementalOverlay.frame,screen)

        hud.draw(screen)

        pygame.display.flip()

    options=(TextOption("Next Level","next"),TextOption("Main Menu","mainmenu"),TextOption("Play Again","restart"),TextOption("QUIT","quit"))
    options[3].setSelectedColor(RED)
    #options[4].setUnselectedColor(GRAY)

    #alignment of menu options
    verticalspace=level.bgRect.height-titleLogoRect.bottom
    heightOfOptions=0
    for op in options:
        heightOfOptions=heightOfOptions+op.rect.height+5

    currentY=int((verticalspace-heightOfOptions)/2+titleLogoRect.bottom)

    for op in options:
        op.rect.top=currentY
        currentY=currentY+op.rect.height+5

    selectedIndex=0
    while True: #think of condition later
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
                if options[selectedIndex].action=="next":
                    pygame.mixer.music.stop()
                    initiateLevel(screen,level.nextLevelPath,character)
                elif options[selectedIndex].action=="mainmenu":
                    #import MainScreen
                    MainScreen.titleScreen(screen,level.crashman.character)
                elif options[selectedIndex].action=="restart":
                    playGame(screen,level)
                elif options[selectedIndex].action=="quit":
                    pygame.quit()
                    sys.exit()

        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        for op in options:
            op.draw(screen)

        pygame.display.flip()

def lose(screen, camera, level, enemy_list, clock, hud):
    pygame.mixer.music.load('sound/gameover.wav')
    pygame.mixer.music.play(0)

    #one third of the way from the top
    titleLogoImage=pygame.image.load("menu/gameover.png").convert_alpha()
    titleLogoRect=titleLogoImage.get_rect()
    titleLogoRect.center=(512,level.bgRect.height/3)

    level.crashman.image=pygame.transform.flip(level.crashman.image,False,True)
    screen.blit(titleLogoImage,titleLogoRect)
    
    while level.crashman.falling==True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key==K_SPACE):
                exitKey = True

        tpt = tps(clock, FPS)
        
        
        level.crashman.updateFalling()
        if not level.crashman.rect.colliderect(camera.rect):
            level.crashman.falling=False
            
                
        level.drawBG(screen)

        #draw everything
        camera.draw_sprites_prio(screen, level.all_sprite, level.crashman)

        screen.blit(titleLogoImage,titleLogoRect)
        

        if level.elemental:
            level.elementalOverlay.draw_frame(level.elementalOverlay.frame,screen)

        hud.draw(screen)

        pygame.display.flip()

    options=(TextOption("Restart","restart"),TextOption("Main Menu","mainmenu"),TextOption("QUIT","quit"))
    options[2].setSelectedColor(RED)

    #alignment of menu options
    verticalspace=level.bgRect.height-titleLogoRect.bottom
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
                if options[selectedIndex].action=="restart":
                    playGame(screen,level)
                elif options[selectedIndex].action=="mainmenu":
                    #import MainScreen
                    MainScreen.titleScreen(screen,level.crashman.character)
                elif options[selectedIndex].action=="quit":
                    pygame.quit()
                    sys.exit()

        for op in options:
            op.selected=False

        options[selectedIndex].selected=True

        #screen.blit(titleLogoImage,titleLogoRect)
        for op in options:
            op.draw(screen)

        pygame.display.flip()

def splashscreen(screen,image,rect):
    screen.blit(image,rect)
    pygame.display.flip()
    waitForKeysDown((K_ESCAPE,K_SPACE,K_RETURN))

def initiateLevel(screen,levelPath,character):
    screen_rect = screen.get_rect()
    level = Level(levelPath,character)

    splashscreen(screen,level.splashscreenImg,(0,0,1024,600))
    playGame(screen,level)
    
def playGame(screen,level):
    screen_rect = screen.get_rect()
    
    level.reset()
    world = level.world
    crashman = level.crashman
    pygame.mouse.set_visible(True)

    camera = Camera(screen, crashman.rect, level)
    all_sprite = level.all_sprite

    
    clock = pygame.time.Clock()

    up = down = left = right = False
    x, y = 0, 0


    #randomly selects an enemy port
    enemy_list=[]
    activePortIndex=random.randrange(len(level.enemy_ports))
    activePort=level.enemy_ports[activePortIndex]




    #untilNextSpawn=level.spawn_delay
    untilNextSpawn=0
    totalTime=0
    enemyCount=0

    hud=HUD()


    pygame.mixer.music.load(level.musicPath)
    pygame.mixer.music.play(-1)



    #this is the while true loop
    while crashman.alive and not (objectiveComplete(objectiveProgress(level.objectiveType,hud.enemies_defeated,totalTime),level.objectiveMax) or crashman.foundFlag):
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()



            if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key== K_RETURN):
                #import MainScreen
                if level.hasVideo==True:
                    level.movie.pause()
                up=down=left=right=False
                pauseScreen(screen, level)
                if level.hasVideo==True:
                    level.movie.pause()

            #cheat to end level
            if event.type == KEYDOWN and event.key == K_BACKSPACE:
                crashman.foundFlag=True
                
            #control crashman
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                up=True
            else:
                up=False
                
            if keys[pygame.K_DOWN]:
                down=True
            else:
                down=False
                
            if keys[pygame.K_LEFT]:
                left=True
            else:
                left=False
                
            if keys[pygame.K_RIGHT]:
                right=True
            else:
                right=False

        #sequential spawn order
        """
        if untilNextSpawn<=0 and enemyCount<level.enemy_max:
            print "ENEMY HERE NOW"
            e=Enemy(activePort[0],activePort[1],activePort[2],level)
            enemy_list.append(e)
            level.all_sprite.add(e)
            world.append(e)
            activePortIndex+=1
            if activePortIndex>=len(level.enemy_ports):
                activePortIndex=0
            activePort=level.enemy_ports[activePortIndex]
            untilNextSpawn=level.spawn_delay
            enemyCount+=1"""

        #random spawn order
        if untilNextSpawn<=0 and enemyCount<level.enemy_max:
            print "ENEMY HERE NOW"
            e=Enemy(activePort[0],activePort[1],activePort[2],level)
            enemy_list.append(e)
            level.all_sprite.add(e)
            world.append(e)
            activePortIndex=random.randrange(len(level.enemy_ports))
            activePort=level.enemy_ports[activePortIndex]
            untilNextSpawn=level.spawn_delay
            enemyCount+=1


        #removes dead enemies
        for e in enemy_list:
            if e.alive==False:
                print "ded del thjo"
                enemy_list.remove(e)
                all_sprite.remove(e)
                world.remove(e)
                enemyCount-=1

            if e.freshkick==True:
                hud.enemies_defeated+=1
                hud.update()
                e.freshkick=False


        

        #timer and spawn countdown
        #updates hud time
        tpt = tps(clock, FPS)
        totalTime+=tpt
        if hud.time!=math.floor(totalTime):
            hud.time=math.floor(totalTime)
            hud.update()
        
        if enemyCount<level.enemy_max:
            untilNextSpawn-=tpt
            print str(enemyCount)+": "+str(untilNextSpawn)


        #DRAW ORDER:
        #bg, world, elemental, hud
        #camera.draw_sprites(screen, all_sprite)
        level.drawBG(screen)
        camera.draw_sprites_prio(screen, all_sprite, crashman)

        if level.elemental:
            level.elementalOverlay.draw(screen)

        hud.draw(screen)

        #final updates
        crashman.update(up, down, left, right)
        for e in enemy_list:
            e.update(tpt)
        camera.update()
        pygame.display.flip()


    #################################
    #game complete
    #pygame.display.flip()
    pygame.mixer.music.stop()
    crashman.update(False, False, False, False)
    
    level.drawBG(screen)
    camera.draw_sprites_prio(screen, all_sprite, crashman)

    if level.elemental:
        level.elementalOverlay.draw(screen)

    hud.draw(screen)
    pygame.display.flip()


    if crashman.direction=="right":
        crashman.image=crashman.jump_right
    else:
        crashman.image=crashman.jump_left

    

    """if objectiveComplete(objectiveProgress(level.objectiveType,hud.enemies_defeated,totalTime),level.objectiveMax):
        win(screen, camera, level, enemy_list, clock)
    else:
        lose(screen, camera, level, enemy_list, clock)"""

    if crashman.alive==False:
        lose(screen, camera, level, enemy_list, clock, hud)
    else:
        win(screen, camera, level, enemy_list, clock, hud, crashman.character)
