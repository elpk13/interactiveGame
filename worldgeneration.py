from classes import *
import pygame
import random
import os
import math
import dialog
import bisect

# This script contains two functions:  getWorldGraphics, which loads all the
# images that appear in the world from their files and sends them in dictionaries.
# Running this function only once allows the image loading to only occur once,
# good for keeping world generation fast.  Keeping all image loading in this
# function also makes it a one-stop place to check filenames, though menu images
# are not a part of it.

# The second function, generateWorld, produces an object of the class World,
# which has as attributes lists of every object to appear in the world.
# This function has two primary parts:  the first, a set of sub-functions that
# initialize objects of our own classes (e.g., plantTree), the second, a set of
# subfunctions that produces lists of these to be sent to the world object.

# Argument names in subfunctions generally match those in the parent function.

def getWorldGraphics(window_height,worldx=0,worldy=0,bgname="Map_Background.png"):
    # worldx = worldy = 0 causes them to be determined by the dimensions of the background image.
    def getBackground(bgname,worldx=0,worldy=0):
        background = pygame.image.load(os.path.join('Assets',"Map_Background.png"))
        nightbackground = pygame.image.load(os.path.join('Assets',"Map_Background_Night.png"))
        if worldx + worldy > 0:
            background = pygame.transform.scale(background,(worldx,worldy))
            nightbackground = pygame.transform.scale(nightbackground,(worldx,worldy))
        return background, nightbackground

    background, nightbackground = getBackground(bgname,worldx,worldy)
    worldx = background.get_width()
    worldy = background.get_height()

    def getCharacter(height): # Returns list of framelists for four animations and name.
        # Identity of the character determined from settings file edited by choice screen,
        # not passed to function.
        settingsfile = open("settings.txt","r") # Retrieve current status of settings
        currentsettings = settingsfile.readlines() # from settings file.
        charid = int(currentsettings[2][0])
        settingsfile.close() # Choose character and name.
        charactername = ['Aspen','Khewa','Mani','Nico','Sparrow','Timber'][charid]

        pframers = [] # Form list of animations.  One for right-walking, one for
        pframels = [] # left-walking, one up, one down.
        pframeus = [] # Each starts with standing and loops from the third frame.
        pframeds = []
        for f in range(1,9):
            frame = pygame.image.load(os.path.join('Animations','Wolves',charactername,charactername + '_Walking_Right000' + str(f) + '.png'))
            frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
            pframers.append(frame)
            frame = pygame.transform.flip(frame,True,False)
            pframels.append(frame)
            frame = pygame.image.load(os.path.join('Animations','Wolves',charactername,charactername + '_Walking_Forward000' + str(f) + '.png'))
            frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
            pframeus.append(frame)
            frame = pygame.image.load(os.path.join('Animations','Wolves',charactername,charactername + '_walking_Away000' + str(f) + '.png'))
            frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(7*frame.get_height())),int(height/7)))
            pframeds.append(frame)

        if charactername == "Mani":
            charactername = "Máni"  # Accent mark not in filename.

        return Wolf(charactername,[pframers,pframels,pframeus,pframeds])

    character = getCharacter(window_height)

    def getStreamGraphics():
        streamAppearancesByAim = { } # The 'aim' of a stream roughly refers to the
        streamNightAppearancesByAim = { } # direction south of the west-axis in
        appearances = [] # which it flows.  Rivers flow south-west, always.
        nightappearances = []
        streamDimensionsByAim = { } # 's' refers to source.
        for aim in ['30','45','60','30s','45s','60s','30-45','45-60','60-30','30-60','60-45','45-30']:
            for i in range(1,4):  # Change length of stream animations here.
                appearances.append(pygame.image.load(os.path.join('Animations','Streams',aim+'000'+str(i)+'.png')))
                nightappearances.append(pygame.image.load(os.path.join('Animations','Streams',aim+'000'+str(i)+'_Night.png')))
            streamAppearancesByAim[aim] = appearances
            streamNightAppearancesByAim[aim] = nightappearances
            width, height = appearances[0].get_width(), appearances[0].get_height()
            streamDimensionsByAim[aim] = (width,height)
            appearances = []
            nightappearances = []
        return streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim

    streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim = getStreamGraphics()

    def getStreamCurveCoefficients(): # The coefficients of curves in stream bends
        def fg(t,w,i,e): # need only be calculated once.  This method is explained in a side document.
            def r(d): # Cool, a fourth-order nested function!
                return int(d)*math.pi/180 # Converts degree-strings to radians.
            f = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(e))-2*t)/t**3 , (3*t-3*w/math.cos(r(e))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , w/math.cos(r(e)) )
            g = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(i))-2*t)/t**3 , (3*t-3*w/math.cos(r(i))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , 0 )
            return f, g
        streamCurveCoefficients = { }
        for aim in ['30-45','30-60','45-30','45-60','60-30','60-45']:
            streamCurveCoefficients[aim] = fg(300,50,aim[:2],aim[-2:])
        return streamCurveCoefficients

    streamCurveCoefficients = getStreamCurveCoefficients()

    def getTreeGraphics():
        treeGraphics = { } # Dictionary of framelists (one for each season) by type.
        treeNightGraphics = { }
        treeGreenness = { } # Dictionary of whether a tree is evergreen (same image in winter)
        for type in ['White_Oak']: # List all non-evergreen trees here.
            summerdays = []
            summernits = []
            autumndays = []
            autumnnits = []
            winterdays = []
            winternits = []
            for i in range(1,8):
                summerdays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Summer000'+str(i)+'.png')))
                summernits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Summer000'+str(i)+'_Night.png')))
                autumndays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Autumn000'+str(i)+'.png')))
                autumnnits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Autumn000'+str(i)+'_Night.png')))
                winterdays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Winter000'+str(i)+'.png')))
                winternits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Winter000'+str(i)+'_Night.png')))
            treeGraphics[type] = (summerdays,autumndays,winterdays)
            treeNightGraphics[type] = (summernits,autumnnits,winternits)
            treeGreenness[type] = False
        for type in ['Spruce']: # List all evergreen trees here.
            days = []
            nits = []
            for i in range(1,8):
                days.append(pygame.image.load(os.path.join('Animations','Trees',type+'000'+str(i)+'.png')))
                nits.append(pygame.image.load(os.path.join('Animations','Trees',type+'000'+str(i)+'_Night.png')))
            treeGraphics[type] = days
            treeNightGraphics[type] = nits
            treeGreenness[type] = True
        return treeGraphics, treeNightGraphics, treeGreenness

    treeGraphics, treeNightGraphics, treeGreenness = getTreeGraphics()

    def getPrintGraphics(height): # Height is the height of the world, by which prints are scaled.
        printGraphics = { } # Prints, large and identifiable for dialogs
        printGraphicsSmall = { } # Blitted images in the world
        animalTypes = { } # Types by animal - 0 for prey, 1 for mutual, 2 for predator
        for animal in ['bison']: # List predators here - bear, moose
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 2
        for animal in []: # List neither predator nor prey here - raccoons, foxes
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 1
        for animal in ['deer','rabbit']: # List prey here
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 0
        return printGraphics, printGraphicsSmall, animalTypes

    printGraphics, printGraphicsSmall, animalTypes = getPrintGraphics(window_height)

    return worldx, worldy, background, nightbackground, character, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphics, printGraphicsSmall, animalTypes

# Observe that not all the output from the above function is input into that
# below.  The character, the animalTypes dictionary, and the larger print graphics
# are not necessary for the construction of the world.

def generateWorld(worldx,worldy,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, printGraphicsSmall):
    # The first part of this function, concerning sub-functions that initialize
    # user-defined classes.  Updates to classes probably need to be updated here.

    def pourStream(worldx,worldy,streamAppearancesByAim,streamNightAppearancesByAim,streamDimensionsByAim):
        sourcex = random.randint(0,worldx) # Place a random source, pick a direction, and go.
        sourcey = random.randint(0,worldy)
        dir = random.choice(['30','45','60'])
        riverys = {'30':58,'45':71,'60':100} # Vertical height of the river at crossing, by angle.
                                             # Equals width times the secant of the angle.
        aim = dir+'s'
        stream = [StreamSegment(sourcex,sourcey,200,200,True,streamAppearancesByAim[aim],streamNightAppearancesByAim[aim],aim)]
        runningx = sourcex
        runningy = sourcey + 200 - riverys[dir]

        while runningx > 0 and runningy < worldy:
            if random.random() > 0.25: # Half a chance of changing direction with each.
                newdir = random.choice(['30','45','60'])
            else:
                newdir = dir
            if newdir == dir:
                aim = dir
            else:
                aim = '-'.join([dir,newdir])
            segwidth, segheight = streamDimensionsByAim[aim]
            stream.append(StreamSegment(int(runningx-segwidth),runningy,segwidth,segheight,True,streamAppearancesByAim[aim],streamNightAppearancesByAim[aim],aim))
            runningx -= segwidth
            runningy += segheight - riverys[newdir]
            dir = newdir
        return stream # Returns list of segments

    def dry(x,y,streams=[]): # This function checks whether any
        for stream in streams: # streams cover a given point.  Used in later
            for segment in stream: # initialization functions to ensure that
                if segment.covers(x,y,streamCurveCoefficients): # trees, etc.
                    return False                                # not in water.
        return True

    def plantTree(worldx,worldy,type,streams,treeGraphics,treeNightGraphics,treeGreenness):
        while True:
            x = random.randint(0,worldx)
            y = random.randint(0,worldy)
            if dry(x,y,streams):
                appearance = treeGraphics[type]
                if treeGreenness[type]:
                    height = appearance[0].get_height()
                    width = appearance[0].get_width()
                else:
                    height = appearance[0][0].get_height()
                    width = appearance[0][0].get_width()
                return Tree(int(x-width/2),int(y-3*height/4),height,width,True,treeGraphics[type],treeNightGraphics[type],type,treeGreenness[type])

    def stampPrint(worldx,worldy,animal,streams,printGraphicsSmall):
        while True:
            x = random.randint(0,worldx)
            y = random.randint(0,worldy)
            if dry(x,y,streams):
                appearance = printGraphicsSmall[animal]
                return Print(x,y,appearance.get_height(),appearance.get_width(),animal,appearance)

    # The second part of this function concerns the placement of objects
    # initialized in the above code, beginning with streams and continuing
    # through obstacles and decorations.

    mystreams = [] # Pourstream is sufficient; I didn't feel like making a whole subfunction for the multiple streams.
    for s in range(2//random.randint(1,6)): # Maximum 2, but probably just one.
        mystreams.append(pourStream(worldx,worldy,streamAppearancesByAim,streamNightAppearancesByAim,streamDimensionsByAim))

    def forestWorld(worldx,worldy,treeTypes,streams,treeGraphics,treeNightGraphics,treeGreenness):
        treecount = worldx*worldy * random.randint(28,175) // 10000000   # Based on historical forest estimates
        if len(treeTypes) > 7: # If we get so far, forests can be unique # and an arbitrary conversion of pixels
            treeTypes = random.sample(treeTypes,random.randint(5,7))     # to real-life units.
        forest = []
        for t in range(treecount):
            forest.append(plantTree(worldx,worldy,random.choice(treeTypes),streams,treeGraphics,treeNightGraphics,treeGreenness))
        forest.sort(key=lambda x: x.ybase)
        return forest

    myforest = forestWorld(worldx,worldy,list(treeGraphics),mystreams,treeGraphics,treeNightGraphics,treeGreenness)

    def leavePrints(worldx,worldy,printGraphicsSmall,streams):
        count = worldx*worldy // 1000000
        prints = []
        for i in range(count):
            prints.append(stampPrint(worldx,worldy,random.choice(list(printGraphicsSmall)),streams,printGraphicsSmall))
        return prints

    myprints = leavePrints(worldx,worldy,printGraphicsSmall,mystreams)

    return World(worldx,worldy,background,nightbackground,mystreams,myforest, [     ] ,myprints, [         ], [          ])
#    return World(worldx,worldy,background,nightbackground,mystreams,myforest,myrocks,myprints,mydecorations,mysettlements)
# When we iterate through a null list, it can only throw syntax errors.  Try:
# for i in []:
#     tom = turtle.Turtle()
#     tom.throwmeanerror(idareyou)
# in a command prompt; it's fun!
