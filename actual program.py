#import pygame library

import pygame
from pygame import mixer
from sys import exit
import os
import random
import csv
import button




from pygame.constants import JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION
   
#initialise pygame
pygame.init()
mixer.init()

#initialise joystick function
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]




#define screen variables
screenWidth = 800
screenHeight = 600 #screenHeight will be variable 

screen = pygame.display.set_mode((screenWidth,screenWidth))     #create game window
pygame.display.set_caption('Platformer')                        #define window title


#set FPS
clock = pygame.time.Clock()
FPS = 60


#main game variables 
gravity = 0.75
scrollThreshold = 100
rows = 12
maxColumns = 100
tileSize = screenHeight // rows
tileTypes = 15
screenScroll = 0
bgScroll = 0 
lvl = 1 
maxLvls = 2
startGame = False
controlKeys = 6
startIntro = False

#defining player movement variables
moveLeft = False 
moveRight = False
shoot = False

bulletImg = pygame.image.load('Game Files/images/icons/bullet.png')


#define colours
background= 255,0,255
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)

#load music and sounds
pygame.mixer.music.load('Game Files/audio/snd_boss_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0,2000)
jumpFX = pygame.mixer.Sound('Game Files/audio/snd_jump.mp3')
jumpFX.set_volume(0.3)
shootFX = pygame.mixer.Sound('Game Files/audio/snd_rifle_shot.mp3')
shootFX.set_volume(0.3)
hurtFX = pygame.mixer.Sound('Game Files/audio/snd_hurt.mp3')
hurtFX.set_volume(0.3)
reloadFX = pygame.mixer.Sound('Game Files/audio/snd_reload_clip.mp3')
reloadFX.set_volume(0.3)
movingFX = pygame.mixer.Sound('Game Files/audio/snd_step1.mp3')
movingFX.set_volume(0.3)
coinFX = pygame.mixer.Sound('Game Files/audio/snd_collect.mp3')
coinFX.set_volume(0.3)
enemyDeathFX = pygame.mixer.Sound('Game Files/audio/snd_blowup.mp3')
enemyDeathFX.set_volume(0.3)






#button images
startImg = pygame.image.load('Game Files/images/icons/start.png').convert_alpha()
exitImg = pygame.image.load('Game Files/images/icons/exit.png').convert_alpha()
restartImg = pygame.image.load('Game Files/images/icons/restart.png').convert_alpha()

#load control images
downArrow = pygame.image.load('Game Files/images/icons/controls/down.png')
upArrow =  pygame.image.load('Game Files/images/icons/controls/up.png')
leftArrow =  pygame.image.load('Game Files/images/icons/controls/left.png')
rightArrow =  pygame.image.load('Game Files/images/icons/controls/right.png')
rKey =  pygame.image.load('Game Files/images/icons/controls/r.png')
spacebar =  pygame.image.load('Game Files/images/icons/controls/space.png')

#load images 
backgroundImg = pygame.image.load('Game Files/images/background/background.png').convert_alpha()
skyImg = pygame.image.load('Game Files/images/background/parallax-mountain-bg.png').convert_alpha()
mountainImg = pygame.image.load('Game Files/images/background/parallax-mountain-mountains.png').convert_alpha()
mountainFarImg = pygame.image.load('Game Files/images/background/parallax-mountain-montain-far.png').convert_alpha()
mountainTreesImg = pygame.image.load('Game Files/images/background/parallax-mountain-trees.png').convert_alpha()
treesImg = pygame.image.load('Game Files/images/background/parallax-mountain-foreground-trees.png').convert_alpha()
mountainImg = pygame.transform.scale(mountainImg, (int(mountainImg.get_width() *2),int(mountainImg.get_height()*3)))
backgroundImg = pygame.transform.scale(backgroundImg, (int(backgroundImg.get_width() *4),int(backgroundImg.get_height()*3))) 
skyImg = pygame.transform.scale(skyImg, (int(skyImg.get_width() *4),int(skyImg.get_height()*3)))
treesImg = pygame.transform.scale(treesImg, (int(treesImg.get_width() *2),int(treesImg.get_height()*3)))
mountainFarImg = pygame.transform.scale(mountainFarImg, (int(mountainFarImg.get_width() *2),int(mountainFarImg.get_height()*3)))
mountainTreesImg = pygame.transform.scale(mountainTreesImg, (int(mountainTreesImg.get_width() *2),int(mountainTreesImg.get_height()*3)))


#load tileTypes and store in list
imgList = []
for i in range(tileTypes):
    img = pygame.image.load(f'Game Files/images/tileset/{i}.png')
    img = pygame.transform.scale(img, (tileSize,tileSize)) 
    imgList.append(img)

font = pygame.font.SysFont('ArcadeClassic', 30)
def drawText(text,font,textCol,x,y):
    img = font.render(text,True,textCol)
    screen.blit(img,(x,y))

def drawBG():
    screen.fill(background)
    width = skyImg.get_width()
    for x in range(5):
        screen.blit(backgroundImg, ((x*width) - bgScroll * 0.5, screenHeight - backgroundImg.get_height()))
        screen.blit(skyImg,((x*width) - bgScroll *0.5, 0))
        screen.blit(mountainFarImg,((x*width) -bgScroll *0.5,screenHeight - mountainFarImg.get_height() - 100))
        screen.blit(mountainImg, ( (x*width) -bgScroll *0.6, mountainImg.get_height() -440))
        screen.blit(mountainTreesImg, ((x*width) - bgScroll *0.7, mountainTreesImg.get_height() - 405))
        screen.blit(treesImg, ((x*width) -bgScroll*0.8,treesImg.get_height() - 405))

def resetLvl():
    enemyGroup.empty()
    bulletGroup.empty()
    decorationGroup.empty()
    exitGroup.empty()
    coinGroup.empty()

    #create empty tile list
    data = []
    for row in range(rows):
        r = [-1] * maxColumns
        data.append(r)

    return data
    


#create class 
class mainChar(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed, ammo):

        
        pygame.sprite.Sprite.__init__(self)
        self.alive = True 

        self.charType = charType
        
        self.speed = speed
        self.ammo = ammo
        self.fullAmmo = 10
        self.shootCooldown = 0 
        self.health = 100
        self.maxHealth = self.health
        self.direction = 1
        self.vertVel = 0
        self.inAir = True
        self.jump = False
        self.flip = False
        self.reload = False
        self.score = 0

        #ai specific variables
        self.moveCounter = 0 
        self.idling = False
        self.idleCounter = 0 
        self.vision = pygame.Rect(0,0,150,20)

        #list for sprite animation
        self.animationList = []
        self.index = 0 
        self.action = 0 
        self.updateTime = pygame.time.get_ticks()
        
        animationTypes = ['idle','run','jump','defeat']
            
        for animation in animationTypes:
            
            #resets image list 
            tempList = []
            #count number of files in each folder
            frameNum = len(os.listdir(f'Game Files/images/{self.charType}/{animation}'))
            for i in range(frameNum):
                img = pygame.image.load(f'Game Files/images/{self.charType}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()* scale)))
                tempList.append(img)        
            self.animationList.append(tempList)
            


        self.image = self.animationList[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) #instance variable, specific to player
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    #group all methods together to clean up game loop
    
    def update(self):
        self.animationUpdate()
        self.checkAlive()
        if self.shootCooldown > 0:
            self.shootCooldown -= 1
    

    def shoot(self):
        if self.shootCooldown == 0 and self.ammo > 0:
            self.shootCooldown = 30
            bullet = Bullet(self.rect.centerx + (0.6* self.rect.size[0] * self.direction),self.rect.centery + (0.1 * self.rect.size[0]),self.direction)
            bulletGroup.add(bullet)
            self.ammo -= 1
            shootFX.play()
            if self.ammo == 0:
                self.reload = True


    def move(self, moveLeft, moveRight):
        #reset movement variables
        screenScroll = 0 
        movex = 0 
        movey = 0 
        
        #assign movement variables depending on direction
        if moveLeft:
            movex = -self.speed
            self.flip = True
            self.direction = -1
        if moveRight:
            movex = self.speed
            self.flip = False
            self.direction = 1 

        #jump movement 
        if self.jump == True and self.inAir == False:
            self.vertVel = -13
            self.jump = False
            self.inAir = True
        

        #gravity
        self.vertVel += gravity
        if self.vertVel > 10:
            self.vertVel = 10
        movey += self.vertVel

        #collision check
        for tile in world.obstacleList:
            #collision in x direction
            if tile[1].colliderect(self.rect.x + movex, self.rect.y, self.width, self.height):
                movex= 0
                #if AI hits wall, turn around
                if self.charType == 'enemy':
                    self.direction *= -1
                    self.moveCounter = 0 
            #collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + movey, self.width, self.height):
                #check if below ground e.g. jumping
                if self.vertVel < 0:
                    self.vertVel = 0 
                    movey = tile[1].bottom - self.rect.top
                #check if above ground e.g. falling
                elif self.vertVel >= 0:
                    self.vertVel = 0
                    self.inAir = False
                    movey = tile[1].top - self.rect.bottom

        #check if falling off map
        if self.rect.bottom > screenHeight:
            self.health = 0


        #check if going off screen
        if self.charType == 'player':
            if self.rect.left + movex <0 or self.rect.right + movex > screenWidth:
                movex = 0

        #check if collision with exit
        lvlComplete = False
        if pygame.sprite.spritecollide(self, exitGroup, False):
            lvlComplete = True
                

        #update rect position
        self.rect.x += movex 
        self.rect.y += movey

        #update scroll based on player position
        if self.charType == 'player':
            if (self.rect.right > screenWidth - scrollThreshold and bgScroll < (world.lvlLength * tileSize) - screenWidth)\
            or self.rect.left < (scrollThreshold and bgScroll > abs(movex)):
                self.rect.x -= movex
                screenScroll = -movex

        return screenScroll, lvlComplete


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,100) == 1:
                self.actionUpdate(0) #idle
                self.idling = True
                self.idleCounter = 50 
            
            #check if ai is near player
            if self.vision.colliderect(player.rect):
                #stop running and face player
                self.actionUpdate(0) #idle
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        aiMovingRight = True
                    else:
                        aiMovingRight = False
                    aiMovingLeft = not aiMovingRight
                    self.move(aiMovingLeft,aiMovingRight)
                    self.actionUpdate(1) #run
                    self.moveCounter += 1
                    if self.moveCounter > tileSize:
                        self.direction *= -1
                        self.moveCounter *= -1
                        #update ai vision while moving
                        self.vision.center = (self.rect.centerx + 75 * self.direction,self.rect.centery)
                        
                else:
                    self.idleCounter -= 1
                    if self.idleCounter <= 0:
                        self.idling = False
        #scroll
        self.rect.x += screenScroll


    def animationUpdate(self):
        #update animation
        animationTimer = 100
        
        #update image
        self.image = self.animationList[self.action][self.index]

        #check if time has passed since last update
        if pygame.time.get_ticks() - self.updateTime > animationTimer:
            self.updateTime = pygame.time.get_ticks()
            self.index += 1
        #reset index when animation ended
        if self.index >= len(self.animationList[self.action]):
            if self.action == 3:
                self.index = len(self.animationList[self.action]) - 1 
            else:
                self.index = 0 

    def actionUpdate(self,newAction):
      #check if new action is different to previous

        if newAction != self.action:
            self.action = newAction  
            #update animation settings
            self.index = 0 
            self.updateTime = pygame.time.get_ticks()

    def checkAlive(self):
        if self.health <= 0:
            self.health = 0 
            self.speed = 0
            self.alive = False
            self.actionUpdate(3)
    
    
    


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #draws character onto screen 
               
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bulletImg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        #bullet movement
        self.rect.x += (self.direction * self.speed) + screenScroll
        #check for off screen bullet
        if self.rect.right < 0 or self.rect.left > screenWidth:
            self.kill()
        for tile in world.obstacleList:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check character collision
        if pygame.sprite.spritecollide(player,bulletGroup, False):
            if player.alive:
                self.kill()
                player.health -= 10
                hurtFX.play()
        for enemy in enemyGroup:
            if pygame.sprite.spritecollide(enemy,bulletGroup, False):
                if enemy.alive:
                    self.kill()
                    enemy.health -= 25   
                    if enemy.health == 0:    
                        enemyDeathFX.play()
                        player.score += 10
                        if player.health <= 90:
                            player.health += 10       
        
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Game Files/images/icons/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*scale), int(self.image.get_height()* scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))

    def update(self):
        #check if player has collected coin
        if pygame.sprite.collide_rect(self, player):
            player.score += 10
            #delete coin after collision
            self.kill()
            coinFX.play()
        self.rect.x += screenScroll

class World():
    def __init__(self):
        self.obstacleList = []

    def processData(self,data):
        self.lvlLength = len(data[0])
        #iterate through each value in game data files
        for y, row in enumerate(data):
            for x,tile in enumerate(row):
                if tile >= 0 :
                    img = imgList[tile]
                    imgRect = img.get_rect()
                    imgRect.x = x * tileSize
                    imgRect.y = y * tileSize
                    tileData = (img, imgRect)
                    if tile >= 0 and tile <=8:
                        self.obstacleList.append(tileData)
                    elif tile >= 9 and tile <= 10: #creates decorations
                        decoration = Decorations(img, x *tileSize, y*tileSize)
                        decorationGroup.add(decoration)
                    elif tile == 11: #creates player
                        player = mainChar('player', x*tileSize,y*tileSize,2,5,10)
                        HealthBar = healthBar(10, 10, player.health, player.health)
                    elif tile == 12: #creates enemies
                        enemy = mainChar('enemy', x*tileSize, y*tileSize, 2,2,10)
                        enemyGroup.add(enemy)
                    elif tile == 13: #creates coin
                        coin = Coin(x*tileSize,y*tileSize,2)
                        coinGroup.add(coin)
                    elif tile == 14: #exit flag
                        Exitflag = exitflag(img, x*tileSize,y*tileSize)
                        exitGroup.add(Exitflag)

        return  player, HealthBar

    def draw(self):
        for tile in self.obstacleList:
            tile[1][0] += screenScroll
            screen.blit(tile[0], tile[1])

class Decorations(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))

    def update(self):
        self.rect.x += screenScroll

class exitflag(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))
    def update(self):
        self.rect.x += screenScroll

class healthBar():
    def __init__(self,x,y,health,maxHealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxHealth = maxHealth
    
    def draw(self,health):
        #update with new health 
        self.health = health
        ratio = self.health / self.maxHealth
        pygame.draw.rect(screen,black,(self.x - 2,self.y - 2,154,24 ))
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        
class screenFade():
    def __init__(self,direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fadeCounter = 0
    
    def fade(self):
        fadeComplete = False
        self.fadeCounter += self.speed
        if self.direction == 1: #whole screen fade
            pygame.draw.rect(screen, self.colour, (0 -self.fadeCounter,0, screenWidth //2, screenHeight))
            pygame.draw.rect(screen, self.colour, (screenWidth //2 + self.fadeCounter,0, screenWidth , screenHeight))
            pygame.draw.rect(screen, self.colour, (0 ,0 -self.fadeCounter, screenWidth , screenHeight//2))
            pygame.draw.rect(screen, self.colour, (0 ,screenHeight//2+ self.fadeCounter, screenWidth , screenHeight))
        if self.direction == 2: #vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0,0,screenWidth, 0 +self.fadeCounter))
        if self.fadeCounter >= screenWidth:
            fadeComplete = True
        
        return fadeComplete

#create screen fades
introFade = screenFade(1, black,4)
deathFade = screenFade(2, background, 4 )

#create buttons
startButton = button.Button(screenWidth // 2 -50 , screenHeight // 2 , startImg, 1)
exitButton = button.Button(screenWidth // 2 -50 , screenHeight // 2 +100, exitImg, 1)
restartButton = button.Button(screenWidth // 2 -100, screenHeight // 2, restartImg, 2)
exitButton2 = button.Button(screenWidth // 2 -50, screenHeight // 2 +200, exitImg, 1)


#create sprite groups
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
coinGroup = pygame.sprite.Group()
decorationGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()



#reload text 
reloadX = 400
reloadY = 400

reloadText = pygame.image.load('Game files/images/icons/reload.png')
reloadTextRect = reloadText.get_rect()
reloadTextRect.center = (reloadX,reloadY)


#load images for controls


#empty tile list 
worldData = []
for row in range(rows):
    r = [-1] *maxColumns
    worldData.append(r)

#load level data and game world
with open(f'lvlData{lvl}.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            worldData[x][y] = int(tile)

world = World()
player, HealthBar = world.processData(worldData)

#main game loop
gameLoop = True
while gameLoop:                             
    
    clock.tick(FPS)

    

    if startGame == False:
        #draw menu 
        screen.fill(background)
        #add buttons
        if startButton.draw(screen):
            startGame = True
            startIntro = True
        if exitButton.draw(screen):
            pygame.quit()


    else:
        
        #update background
        drawBG()
        world.draw()
        HealthBar.draw(player.health)

        #ammo counter
        drawText('Ammo: ', font, white, 10 , 35 )
        for x in range(player.ammo):
            screen.blit(bulletImg, (80+(x*10),30))
        drawText(f'Score: {player.score}',font, white, 700,10)

        

        coinGroup.update()
        coinGroup.draw(screen)
        for enemy in enemyGroup:
            enemy.ai()
            enemy.update()
            enemy.draw()

        
        player.update()
        player.draw()


        #update and draw groups
        bulletGroup.update()
        bulletGroup.draw(screen)
        decorationGroup.update()
        decorationGroup.draw(screen)
        exitGroup.update()
        exitGroup.draw(screen)


        #controls
        drawText('Controls:', font, white, 0, screenHeight +10)
        drawText('Jump', font, white, 100, screenHeight+70)
        drawText('Left Run', font, white, 175, screenHeight+70)
        drawText('Right Run', font, white, 275, screenHeight+70)
        drawText('Reload', font, white, 400, screenHeight+70)
        drawText('Shoot', font, white, 100, screenHeight+170)
        screen.blit(upArrow, (100,screenHeight+10))
        screen.blit(leftArrow, (200, screenHeight+10))
        screen.blit(rightArrow, (300, screenHeight+10))
        screen.blit(rKey, (400, screenHeight+10))
        screen.blit(spacebar, (100,screenHeight+110 ))


        #intro fade 
        if startIntro == True:
            if introFade.fade():
                startIntro = False
                introFade.fadeCounter = 0 

        
        #player actions
        if player.alive:
            if shoot:
                player.shoot()
            if player.reload:
                player.actionUpdate(3) #3: reload
            if player.inAir:
                player.actionUpdate(2) #2: jump 
            if moveLeft or moveRight:
                player.actionUpdate(1) #1: run
            else:
                player.actionUpdate(0) #0: idle 
            screenScroll, lvlComplete,= player.move(moveLeft,moveRight)
            bgScroll -= screenScroll
            #check if player has completed level 
            if lvlComplete == True:
                startIntro = True
                lvl += 1
                bgScroll = 0 
                worldData = resetLvl()
                if lvl <=maxLvls:

                    #load in level data and create world 
                    with open(f'lvlData{lvl}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x,row in enumerate(reader):
                            for y,tile in enumerate(row):
                                worldData[x][y] = int(tile)

                    world = World()
                    player, HealthBar = world.processData(worldData)
                


        else:
            screenScroll = 0 
            if deathFade.fade():
                drawText(f'Final Score:{player.score}', font, white, 350,400)
                if restartButton.draw(screen):
                    deathFade.fadeCounter = 0 
                    startIntro = True
                    bgScroll = 0 
                    worldData = resetLvl()
                    #load in level data and create world 
                    with open(f'lvlData{lvl}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x,row in enumerate(reader):
                            for y,tile in enumerate(row):
                                worldData[x][y] = int(tile)

                    world = World()
                    player, HealthBar = world.processData(worldData)
                elif exitButton2.draw(screen):
                    pygame.quit()
                    exit()
        if player.ammo == 0:
            screen.blit(reloadText,reloadTextRect)
        

        
        
        

    for event in pygame.event.get():        #event handler
        #quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
        #keyboard presses
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moveLeft = True
                movingFX.play()
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moveRight = True
                movingFX.play() 
            if event.key == pygame.K_w or event.key == pygame.K_UP and player.alive:
                player.jump = True 
                jumpFX.play()
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_r:
                player.reload = True
                player.ammo = player.fullAmmo
                reloadFX.play()
                
               
        #keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_SPACE:
                shoot = False 
            if event.key == pygame.K_r:
                player.reload = False
            



    pygame.display.update()

pygame.quit()