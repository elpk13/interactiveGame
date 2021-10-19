# Imports and initializations
import pygame
import random
import os
import math
from elements import *

pygame.init()

#set the parameters for the pygame window
height = 900 # Set the dimensions of the screen, which determines how
width = 1200 # much of the world is shown.
screen = pygame.display.set_mode((width,height))
halfheight = height/2
halfwidth = width/2

# World size determined by dimensions of background image.
background = pygame.image.load(os.path.join('Assets',"map_background.jpg"))
worldx = background.get_width()
worldy = background.get_height()
uppery = worldy - halfheight
upperx = worldx - halfwidth
#print(uppery)
#print(upperx)

# Load all player-related images.
# Player images go into four lists:  a list of right-moving frames, left-moving,
# up-moving, and down-moving.  Each can be any length.  First frame should be
# a balanced look for player, looping begins at third.
settingsfile = open("settings.txt","r") # Retrieve current status of settings
currentsettings = settingsfile.readlines() # from settings file.
charid = int(currentsettings[2][0])
settingsfile.close()
charactername = ['Aspen','Khewa','Mani','Nico','Sparrow','Timber'][charid]

# Load character graphics.  Commented lines can be uncommented when files are
# ready.  Currently, only playable character is Mani.
pframers = []
pframels = []
pframeus = []
pframeds = []
for f in range(1,9):
    charactername = 'Nico'
    frame = pygame.image.load(os.path.join('Animations',charactername + '_Walking_Right000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
    pframers.append(frame)
    frame = pygame.transform.flip(frame,True,False)
    pframels.append(frame)
    frame = pygame.image.load(os.path.join('Animations',charactername + '_Walking_Forward000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
    pframeus.append(frame)
    frame = pygame.image.load(os.path.join('Animations',charactername + '_walking_Away000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(7*frame.get_height())),int(height/7)))
    pframeds.append(frame)

# The current frame in any list is stored in the list current frames.
# Currentmode refers to which direction the player is depicted facing.
framelists = [pframers,pframels,pframeus,pframeds]
currentframe = 0
currentmode = 0

if charactername == "Mani":
    charactername = "Máni"  # Don't change until files are loaded.

hoofprint = 0
pos_hoofprint_visited = {}

bisonImage = pygame.image.load(os.path.join('Assets_poc',"temp_bison_print.png"))
bisonImage = pygame.transform.scale(bisonImage,(int(height/15),int(height/15)))
bisonPrints = []
for i in range(50):
    bisonPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
bisonPrints.sort(key=lambda x : x[1])

rabbitImage = pygame.image.load(os.path.join('Assets_poc',"rabbit print.png"))
rabbitImage = pygame.transform.scale(rabbitImage,(int(height/10),int(height/10)))
rabbitPrints = []
for i in range(50):
    rabbitPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
rabbitPrints.sort(key=lambda x : x[1])

deerImage = pygame.image.load(os.path.join('Assets_poc',"deer print.png"))
deerImage = pygame.transform.scale(deerImage,(int(height/15),int(height/10)))
deerPrints = []
for i in range(50):
    deerPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
deerPrints.sort(key=lambda x : x[1])

# Populate the world with arbitrary obstacles of assorted types and sizes.
obstacleImages = [pygame.image.load(os.path.join('Assets',"pine_tree.png")),
pygame.image.load(os.path.join('Assets',"oak_tree.png"))]
obstacleLocations = []
obstacleTypes = []
for i in range(100):
    obstacleLocations.append((random.randint(0,worldx),random.randint(0,worldy)))
    obstacleTypes.append(random.randint(0,len(obstacleImages)-1))
def takey(tup): # Sort list of obstacles so that they blit from top to bottom.
    return tup[1]
obstacleLocations.sort(key=takey)

# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
def posok(x,y):
    for ob in range(len(obstacleLocations)):
        if abs(x-obstacleLocations[ob][0]) < obstacleImages[obstacleTypes[ob]].get_width()/2 and abs(y-obstacleLocations[ob][1]) < obstacleImages[obstacleTypes[ob]].get_height()/2:
            return False
    for bis in bisonPrints:
        if abs(x-bis[0]) < bisonImage.get_width()/2 and abs(y-bis[1]) < bisonImage.get_height()/2:
            if bis not in pos_hoofprint_visited:
                pos_hoofprint_visited[bis] = True
            return bis
    if(x<halfwidth or x>upperx):
        return False
    elif(y<halfheight or y>uppery):
        return False
    else:
        return (x,y)

def printCol(x,y):
    for bis in bisonPrints:
        if abs(x-bis[0]) < bisonImage.get_width()/2 and abs(y-bis[1]) < bisonImage.get_height()/2:
            return True
        else:
            return False

def isNight(frames):
    if (frames % 600) > 300:
        return True
    return False

# The familiar drawscreen method places the relevant part of the background
# over the screen, then superlays obstacles, then places the relevant frame
# of the player.
def drawscreen():
    screen.blit(background,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    if isNight(timelapsed):
        for ob in range(len(obstacleLocations)):
            screen.blit(obstacleNightImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleNightImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleNightImages[obstacleTypes[ob]].get_height()/2)))
    else:
        for ob in range(len(obstacleLocations)):
            screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
    for bison in bisonPrints:
        screen.blit(bisonImage, (int(bison[0]-playerx+width/2-bisonImage.get_width()/20),int(bison[1]-playery+height/2-bisonImage.get_height()/20)))
    for rabbit in rabbitPrints:
        screen.blit(rabbitImage, (int(rabbit[0]-playerx+width/2-rabbitImage.get_width()/20),int(rabbit[1]-playery+height/2-rabbitImage.get_height()/20)))
    for deer in deerPrints:
        screen.blit(deerImage, (int(deer[0]-playerx+width/2-deerImage.get_width()/20),int(deer[1]-playery+height/2-deerImage.get_height()/20)))
    for ob in range(len(obstacleLocations)):
        screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
    playerimage = framelists[currentmode][currentframe]
    screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
    pygame.display.update()

# Pick random point where player starts.  Assume dimensions of map are greater
# than screen, else an error will occur.  Move the player to an acceptable
# position before starting.
playerx = random.randint(width/2,worldx-width/2)
playery = random.randint(height/2,worldy-height/2)
while not posok(playerx,playery):
    playerx = random.randint(width/2,worldx-width/2)
    playery = random.randint(height/2,worldy-height/2)

speed = 10 # pixels by which player moves in a frame
frametime = 100 # milliseconds of each frame

runninggame = True
timelapsed = 0 # frames, ticks, tenths of a second

drawscreen()

while runninggame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runninggame = False
    pressed = pygame.key.get_pressed() # This method of movement checking
    newposx = playerx                  # considers all keys which may be
    newposy = playery                  # pressed at the end of a tick/frame.
    if pressed[pygame.K_RIGHT]:
        newposx += 1
    if pressed[pygame.K_LEFT]:
        newposx -= 1
    if pressed[pygame.K_UP]:
        newposy -= 1
    if pressed[pygame.K_DOWN]:
        newposy += 1
    if pressed[pygame.K_RETURN]:
        speed = 40
    else:
        speed = 10
    # Newpos variables currently indicate only the direction of motion as a
    # vector of variable magnitude.
    dist = ((newposx-playerx)**2 + (newposy-playery)**2) ** 0.5
    if dist > 0:
        newposx = playerx + (newposx - playerx)*speed/dist
        newposy = playery + (newposy - playery)*speed/dist
    # Newpos variables now indicate the desired position of the player in the
    # next frame.
    global resp
    resp = 3

    obj = posok(newposx,newposy) # returns a (x,y) coordinate if a collision occurred, else None
    if obj:
        if newposx > playerx:   # When choosing the direction to face the
            currentmode = 0     # player, left and right are prioritized for
        elif newposx < playerx: # diagonals, as in the Champion Island game.
            currentmode = 1
        elif newposy > playery:
            currentmode = 2
        elif newposy < playery:
            currentmode = 3
        if obj in pos_hoofprint_visited and pos_hoofprint_visited[obj] == True:
            currentframe = 0
            import dialog
            resp = dialog.dialog(width,height,"What would you like to do about the print that was found",['Howl for the pack - Group Hunt','Hunt alone','Run Away','Ignore'],bisonImage)
            pos_hoofprint_visited[obj] = False
        playerx,playery = newposx,newposy # Player position changes;
        # Newpos variables now reflect current position.
        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to
        if resp == 0:
            #group hunt
            drawscreen()
        elif resp == 1:
            import cyc
            drawscreen()
        elif resp == 2:
            #remove tracks
            drawscreen()
        elif resp == 3:
            #ignore
            drawscreen()
    else:                             # stationary player.
        currentframe = 0 # If player cannot move, return to stationary.

    pygame.time.delay(frametime)
    timelapsed += 1
    if timelapsed % 600 == 0:
        background = pygame.image.load(os.path.join('Assets','map_background.jpg'))
    elif timelapsed % 300 == 0:  # 'Light' refers to the dark version, because the function
        background = pygame.image.load(os.path.join('Assets','map_background_light.jpg'))
    drawscreen()                 # that made it lightens images by a scalar > 1.
