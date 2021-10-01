# Imports and initializations
import pygame
import random
import os
import math

pygame.init()

#set the parameters for the pygame window
height = 900 # Set the dimensions of the screen, which determines how
width = 1200 # much of the world is shown.
screen = pygame.display.set_mode((width,height))
halfheight = height/2
halfwidth = width/2

# World size determined by dimensions of background image.
background = pygame.image.load(os.path.join('Assets_poc',"map_background.jpg"))
worldx = background.get_width()
worldy = background.get_height()
uppery = worldy - halfheight
upperx = worldx - halfwidth
print(uppery)
print(upperx)
# Load all player-related images.  For multiple characters, consider making this
# a large tree function in its own script.
# Player images go into four lists:  a list of right-moving frames, left-moving,
# up-moving, and down-moving.  Each can be any length.  First frame should be
# a balanced look for player.
playerr1 = pygame.image.load(os.path.join('Assets_poc',"animation_1.png"))
playerr2 = pygame.image.load(os.path.join('Assets_poc',"animation_2.png"))
playerr3 = pygame.image.load(os.path.join('Assets_poc',"animation_3.png"))
pframers = [playerr1,playerr2,playerr3]
playerl1 = pygame.transform.flip(playerr1,True,False)
playerl2 = pygame.transform.flip(playerr2,True,False)
playerl3 = pygame.transform.flip(playerr3,True,False)
pframels = [playerl1,playerl2,playerl3]
playeru1 = pygame.image.load(os.path.join('Assets_poc',"animation_1.png"))
playeru2 = pygame.image.load(os.path.join('Assets_poc',"animation_2.png"))
playeru3 = pygame.image.load(os.path.join('Assets_poc',"animation_3.png"))
pframeus = [playeru1,playeru2,playeru3]
playerd1 = pygame.image.load(os.path.join('Assets_poc',"animation_1.png"))
playerd2 = pygame.image.load(os.path.join('Assets_poc',"animation_2.png"))
playerd3 = pygame.image.load(os.path.join('Assets_poc',"animation_3.png"))
pframeds = [playerd1,playerd2,playerd3]
# The current frame in any list is stored in the list current frames.
# Currentmode refers to which direction the player is depicted facing.
framelists = [pframers,pframels,pframeus,pframeds]
currentframes = [0,0,0,0]
currentmode = 0
hoofprint = 0 

bisonImage = pygame.image.load(os.path.join('Assets_poc',"temp_bison_print.png"))
bisonImage = pygame.transform.scale(bisonImage,(int(height/15),int(height/15)))
bisonPrints = []
for i in range(50):
    bisonPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
def takey(top):
    return top[1]
bisonPrints.sort(key=takey)

# Populate the world with identical obstacles
obstacleimage = pygame.image.load(os.path.join('Assets_poc',"temporary_tree.png"))
obstacles = []
for i in range(100):
    obstacles.append((random.randint(0,worldx),random.randint(0,worldy)))
def takey(tup): # Sort list of obstacles so that they blit from top to bottom.
    return tup[1]
obstacles.sort(key=takey)

# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
def posok(x,y):
    for ob in obstacles:
        if abs(x-ob[0]) < obstacleimage.get_width()/2 and abs(y-ob[1]) < obstacleimage.get_height()/2:
            return False
    for bis in bisonPrints:
        if abs(x-bis[0]) < bisonImage.get_width()/2 and abs(y-bis[1]) < bisonImage.get_height()/2:
            return False
    if(x<halfwidth or x>upperx):
        return False
    elif(y<halfheight or y>uppery):
        return False
    else:
        return True

def printCol(x,y):
    for bis in bisonPrints:
        if abs(x-bis[0]) < bisonImage.get_width()/2 and abs(y-bis[1]) < bisonImage.get_height()/2:
            return True
        else:
            return False

# The familiar drawscreen method places the relevant part of the background
# over the screen, then superlays obstacles, then places the relevant frame
# of the player.
def drawscreen():
    screen.blit(background,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    for obstacle in obstacles:
        screen.blit(obstacleimage, (int(obstacle[0]-playerx+width/2-obstacleimage.get_width()/2),int(obstacle[1]-playery+height/2-obstacleimage.get_height()/2)))
    for bison in bisonPrints:
        screen.blit(bisonImage, (int(bison[0]-playerx+width/2-bisonImage.get_width()/20),int(bison[1]-playery+height/2-bisonImage.get_height()/20)))
    playerimage = framelists[currentmode][currentframes[currentmode]]
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

drawscreen()

runninggame = True

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
    # Newpos variables currently indicate only the direction of motion as a
    # vector of variable magnitude.
    dist = ((newposx-playerx)**2 + (newposy-playery)**2) ** 0.5
    if dist > 0:
        newposx = playerx + (newposx - playerx)*speed/dist
        newposy = playery + (newposy - playery)*speed/dist
    # Newpos variables now indicate the desired position of the player in the
    # next frame.
    if posok(newposx,newposy):
        if newposx > playerx:   # When choosing the direction to face the
            currentmode = 0     # player, left and right are prioritized for
        elif newposx < playerx: # diagonals, as in the Champion Island game.
            currentmode = 1
        elif newposy > playery:
            currentmode = 2
        elif newposy < playery:
            currentmode = 3
        playerx,playery = newposx,newposy # Player position changes;
        # Newpos variables now reflect current position.
        if dist > 0: # If player moves, update animation frame in list.
            if currentframes[currentmode] != len(framelists[currentmode]) - 1:
                currentframes[currentmode] += 1
            else:
                currentframes[currentmode] = 0
        else:
            currentframes = [0,0,0,0] # If player doesn't move, return to
    elif printCol(newposx,newposy):
        currentFrames = [0,0,0,0]
        import hunt
        drawscreen()
    else:                             # stationary player.
        currentframes = [0,0,0,0] # If player cannot move, return to stationary.

    pygame.time.delay(frametime)
    drawscreen()
