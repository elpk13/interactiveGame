# Imports and initializations
import pygame
import random
import os
import math
import dialog
from elements import *
from worldgeneration import *
from gamethods import *

pygame.init()

# Put all code in function - character and graphics will be sent to it, rather
# than loaded again.  Sending screen allows it to run on same screen.
def hunt(screen,worldx, worldy, background, nightbackground, character, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphics, printGraphicsSmall, animalTypes, animalGraphics,world):

    globinfo = readglobals() # We will soon add screen, etc. to function arguments
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']

    # I didn't use these in chap1.
    halfwidth = window_width/2
    halfheight = window_height/2
    upperx = worldx - halfwidth
    uppery = worldy - halfheight
    width = window_width
    height = window_height

    hoofprint = 0
    pos_hoofprint_visited = {}

    # Load animal print images and locate 50 of each throghout the map.
    rabbitImage = printGraphics['rabbit'] # Images come from sent dictionaries
    rabbitPrints = []

    rabbitFace = animalGraphics['rabbit'][0] # Static for now.
    #for i in range(50):
    #    rabbitPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
    #rabbitPrints.sort(key=lambda x : x[1])
    rabbitA = (random.randint(halfwidth,upperx-100),random.randint(halfheight,uppery-100))
    print(f"rabbitA:{rabbitA}")


# Populate the world with arbitrary obstacles of assorted types and sizes.
# Use the world passed to function for now - but remove prints, and consider
# using a smaller one?
    world.prints = []

    caught = 0
    count = 0
# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
    def posokh(x,y): # Change name so I can use posok() inside it.
        if not posok(x,y,world.obstacles):
            return False
        if not posinworld(x,y,worldx,worldy,window_width,window_height):
            return False
        if(abs(x-rabbitA[0]) < (rabbitFace.get_width()/5) and abs(y-rabbitA[1]) < (rabbitFace.get_height()/5)):
            #global caught
            #caught = 1
            global count
            count +=1
            print(f"x:{x},y{y}")
            print(f"colx: {x-rabbitA[0]}, coly: {y-rabbitA[1]}")
            #print(rabbitFace.get_width()/5, rabbitFace.get_height()/5)
            print(f"collide no {count}" )
            #print(caught)
            return True
        else:
            return (x,y)

# The drawScreen method depends on a world object which does not yet contain a
# RabbitPath, so this has been added in lieu.
    def drawRabbitPath():
        for rx,ry in zip(rabbitpath_x, rabbitpath_y):
            screen.blit(rabbitImage, (int(rx-playerx+width/2-rabbitImage.get_width()/2), int(ry-playery+height/2-rabbitImage.get_height()/2)) )
        screen.blit(rabbitFace,(int(rabbitA[0]-playerx+width/2-rabbitFace.get_width()/2),int(rabbitA[1]-playery+height/2-rabbitFace.get_height()/2)))
        # Place over everything in drawScreen - consider putting RabbitPath in the World object,
        pygame.display.update() # to add to drawScreen method in correct place.

# Pick random point where player starts.  Assume dimensions of map are greater
# than screen, else an error will occur.  Move the player to an acceptable
# position before starting.
    playerx = random.randint(width/2,worldx-width/2)
    playery = random.randint(height/2,worldy-height/2)
    while not posok(playerx,playery,world.obstacles):
        playerx = random.randint(width/2,worldx-width/2)
        playery = random.randint(height/2,worldy-height/2)


    speed = 10 # pixels by which player moves in a frame
    frametime = 100 # milliseconds of each frame

    runninggame = True
    timelapsed = 0 # frames, ticks, tenths of a second

    currentmode, currentframe = 0, 0
#path function to determine the path on which to blit the rabbit prints
#takes an acceptable radius and angle, using these two things
#determines the path of the footprints that the player will
#have to follow to get to the animal
    rabbitPath = []
    rad = []

    def findPath(rabbitPath, rad): # I had to pass it - even as global, it kept coming
                              # up undefined somehow.
        newx = []
        newy = []
        # sort the location of the rabbit relative to the player.
        #initial iteration, will need to be done in a loop using rabbitPath
        #so that way it varies the path for each increment.

        rabbitPath.append(playerx)
        rabbitPath.append(playery)
        ind = 0
        rabRad = 10000
        rad.append(5)
        radInd = 0

        #loop through the distance from the player blit through the rabbit's location
        #stop when the rabbit's location is within the radius that the player can move within
        while rabRad > 400:
            #
            if(rabbitA[0] > rabbitPath[-2] and rabbitA[1] >= rabbitPath[-1]):
                yLen = rabbitA[1] - rabbitPath[-1]
                xLen = rabbitA[0] - rabbitPath[-2]
                oppAdj = xLen / yLen
                loc = 1
                xc = 1
                yc = 1
                print("one")
            elif(rabbitA[0] < rabbitPath[-2] and rabbitA[1] <= rabbitPath[-1]):
                yLen = rabbitPath[-1] - rabbitA[1]
                xLen = rabbitPath[-2] - rabbitA[0]
                oppAdj = yLen / xLen
                loc = 2
                xc = -1
                yc = -1
                print("two")
            elif(rabbitA[0] < rabbitPath[-2] and rabbitA[1] >= rabbitPath[-1]):
                yLen = rabbitA[1] - rabbitPath[-1]
                xLen = rabbitPath[-2] - rabbitA[0]
                oppAdj = xLen / yLen
                loc = 2
                xc = -1
                yc = 1
                print("three")
            elif(rabbitA[0] > rabbitPath[-2] and rabbitA[1] <= rabbitPath[-1]):
                yLen = rabbitPath[-1] - rabbitA[1]
                xLen = rabbitA[0] - rabbitPath[-2]
                oppAdj = yLen / xLen
                loc = 1
                xc = 1
                yc = -1
                print("four")
            rabRadSq = (xLen**2) + (yLen**2) # calculate norm^2 from current pos to rabbit
            if math.sqrt(rabRadSq) > rabRad:
                rabbitPath.pop()
                rabbitPath.pop()
                rad.append(random.randint(75, 400)) #choose new random radius for next point
                ind -= 2
                print('.',end='')
                continue
            rabRad = math.sqrt(rabRadSq) # calculate norm from current pos to rabbit
            print("rabRad:", end='')
            print(rabRad)
            theta = math.atan(oppAdj) # calculate current angle to rabbit
            angle = random.randint(0, int(theta * 1000)) / 1000 # choose new random angle between 0 and that angle
            rabbitPath.append(rad[-1] * math.cos(angle) * xc + rabbitPath[ind]) # choose new random point x
            rabbitPath.append(rad[-1] * math.sin(angle) * yc + rabbitPath[ind+1]) # choose new random point y
            ind += 2
            radInd += 1
            rad.append(random.randint(75, 400)) #choose new random radius for next point
            print(f"radInd{radInd}")
            #print(rabRad, xc, yc, loc)

    #footprint array calculations here
        newx, newy = [x for i,x in enumerate(rabbitPath) if i % 2 == 0],[x for i,x in enumerate(rabbitPath) if i % 2 == 1]

        return newx, newy, rabbitPath, rad # Pass back out of the function at end for globality

    rabbitpath_x, rabbitpath_y, rabbitPath, rad = findPath(rabbitPath, rad) # Pass into function when called.

    health = 100 # For now.
    ybaselist = getYbaselist(world.objectsofheight)                                             # Always daytime during the hunt?
    drawScreen(screen,window_width,window_height,character,playerx,playery,world,ybaselist,timelapsed,False,health,currentmode,currentframe)
    drawRabbitPath()


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
        if pressed[pygame.K_SPACE]:
            speed = 40
        else:
            speed = 10
        if caught == 1:
            runninggame = False
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

        obj = posokh(newposx,newposy) # returns a (x,y) coordinate if a collision occurred, else None
        if obj:
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
                if currentframe != len(character.framelists[currentmode]) - 1:
                    currentframe += 1
                else:
                    currentframe = 2 # Reset to third frame to loop
            else:
                currentframe = 0 # If player doesn't move, return to
        else:                             # stationary player.
            currentframe = 0 # If player cannot move, return to stationary.
        pygame.time.delay(frametime)
        #timelapsed += 1   # Not advance time/animations during hunt?

        drawScreen(screen,window_width,window_height,character,playerx,playery,world,ybaselist,timelapsed,False,health,currentmode,currentframe)
        drawRabbitPath()

############################# End of hunt function

globinfo = readglobals() # We will soon add screen, etc. to function arguments
window_width = globinfo['window_width']
window_height = globinfo['window_height']
screen = makescreen() # instead of including them here.

worldx, worldy, background, nightbackground, character, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphics, printGraphicsSmall, animalTypes, animalGraphics = getWorldGraphics(globinfo['window_height'])
testworld = generateWorld(worldx,worldy,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphicsSmall)

hunt(screen, worldx, worldy, background, nightbackground, character, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphics, printGraphicsSmall, animalTypes, animalGraphics, testworld)
