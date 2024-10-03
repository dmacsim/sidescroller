import pygame
import button
from sys import exit

import csv





pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
screenWidth = 800
screenHeight = int(0.75 * screenWidth)

screen = pygame.display.set_mode((screenWidth,screenWidth)) 
#screen = pygame.display.set_mode((screenWidth + sideMargin, screenHeight + lowerMargin))
pygame.display.set_caption('Level Editor')

#define game variables
rows = 12
maxColumns = 100
tileSize = screenHeight // rows
tileTypes = 15


currentTile = 0 

lvl = 1 


scrollLeft = False
scrollRight = False
scroll = 0 


scrollSpeed = 1

#create tile map
worldData = []
for row in range(rows):
    r = [-1] *maxColumns
    worldData.append(r)

#create ground
for tile in range(0,maxColumns):
    worldData[rows - 1][tile] = 0



#define colours
white = (255,255,255)
black = (0,0,0)
purple = (255,0,255)    

#load images
skyImg = pygame.image.load('Game Files/images/background/parallax-mountain-bg.png').convert_alpha()
mountainImg = pygame.image.load('Game Files/images/background/parallax-mountain-mountains.png').convert_alpha()
mountainFarImg = pygame.image.load('Game Files/images/background/parallax-mountain-montain-far.png').convert_alpha()
mountainTreesImg = pygame.image.load('Game Files/images/background/parallax-mountain-trees.png').convert_alpha()
treesImg = pygame.image.load('Game Files/images/background/parallax-mountain-foreground-trees.png').convert_alpha()
mountainImg = pygame.transform.scale(mountainImg, (int(mountainImg.get_width() *2),int(mountainImg.get_height()*3)))
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

#save and load images
saveImg = pygame.image.load('Game Files/images/icons/save.png')
loadImg = pygame.image.load('Game Files/images/icons/load.png')


def drawBg():
    screen.fill(purple)
    width1 = skyImg.get_width()
    width2 = mountainImg.get_width()
    for i in range(4):
        screen.blit(skyImg,((i*width1) - scroll *0.55,0))
        screen.blit(mountainFarImg,((i*width1) - scroll *0.55, screenHeight - mountainFarImg.get_height()-50))
        screen.blit(mountainImg, ((i*width2) -scroll * 0.6,screenHeight - mountainImg.get_height()))   
        screen.blit(mountainTreesImg, ((i*width2) - scroll *0.7, screenHeight - mountainTreesImg.get_height()))
        screen.blit(treesImg,((i*width1) -scroll *0.8,screenHeight - treesImg.get_height()-50))


def drawGrid():
    for i in range (maxColumns +1):
        pygame.draw.line(screen, white, (i* tileSize - scroll, 0), (i* tileSize -scroll, screenHeight))
    for i in range (rows + 1):
        pygame.draw.line(screen, white,(0,i*tileSize),(screenWidth,i*tileSize))

#drawing world tiles
def drawWorld():
    for y, row in enumerate(worldData):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(imgList[tile], (x*tileSize-scroll,y*tileSize))

font = pygame.font.SysFont('Arcade Classic',36)

def drawText(text,font,textColour, x,y):
    img = font.render(text,True,textColour)
    screen.blit(img,(x,y))

#create buttons
saveButton = button.Button(screenWidth//2 - 350, screenHeight + 70, saveImg,1)
loadButton = button.Button(screenWidth//2 -350 , screenHeight + 10, loadImg,1)



buttonList = []
buttonColumn = 0 
buttonRow = 0 
for i in range(len(imgList)):   
    tileButton = button.Button(100*buttonRow +300, (60*buttonColumn) +610, imgList[i], 1)
    buttonList.append(tileButton)
    buttonColumn += 1
    if buttonColumn == 3:
        buttonRow += 1
        buttonColumn = 0 









run = True
while run:

    clock.tick(FPS)

    drawBg()

    drawGrid()

    drawWorld()


    drawText(f'Level: {lvl}',font, white,63,screenHeight+150)

    if saveButton.draw(screen):
        with open(f'lvlData{lvl}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in worldData:
                writer.writerow(row)
    
    if loadButton.draw(screen):
        #load in level data
        #reset scroll
        scroll = 0 
        with open(f'lvlData{lvl}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x,row in enumerate(reader):
                for y, tile in enumerate(row):
                    worldData[x][y] = int(tile)

    # #select tile
    buttonCount = 0 
    for buttonCount, i in enumerate(buttonList):
        if i.draw(screen):
            currentTile = buttonCount 
    
    #highlight selected tile
    pygame.draw.rect(screen,black,buttonList[currentTile].rect,3)

    #scroll map
    if scrollLeft == True and scroll>0:
        scroll -= 5 *scrollSpeed
    if scrollRight == True and scroll <(maxColumns*tileSize)- screenWidth:
        scroll += 5 *scrollSpeed
 

    #add new tiles to screen with mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0]+scroll)// tileSize
    y = (pos[1]) // tileSize

    #check that coords are within tile area
    if pos[0] < screenWidth and pos[1] < screenHeight:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if worldData[y][x] != currentTile:
                worldData[y][x]= currentTile
        if pygame.mouse.get_pressed()[2] ==1:
            worldData[y][x] = -1


  



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                scrollLeft = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                scrollRight = True
            if event.key == pygame.K_LSHIFT:
                scrollSpeed = 5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                lvl += 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and lvl>0:
                lvl -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                scrollLeft = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                scrollRight = False
            if event.key == pygame.K_LSHIFT:
                scrollSpeed = 1
    
    pygame.display.update()
pygame.quit()