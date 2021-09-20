import pygame
import os

pygame.init()

#goals
#    sound slider
#    narration slider
#

# need to add selection between top and bottom sound -> how many paws is too many

sliderColor = (204, 204, 255)
lineColor = (0, 0, 0)

#the following lines set up the display window
height = 900 # Set the dimensions of the screen, by which
width = 1200  # everything will be scaled later.
screen = pygame.display.set_mode((width,height))

background = pygame.image.load(os.path.join('Assets',"winter_forest_background.jpg")) # Image credit:
background = pygame.transform.scale(background,(width,height)) # Linnaea Mallette,
                                                               # publicdomainpictures.net
soundlabel = pygame.image.load(os.path.join('Assets',"sound_effects_label.png"))
soundlabel = pygame.transform.scale(soundlabel,(int(width/2),int(height/6)))
narrlabel = pygame.image.load(os.path.join('Assets',"narration_label.png"))
narrlabel = pygame.transform.scale(narrlabel,(int(width/2),int(height/6)))

# Select and scale an indicator to show what is selected
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator1,(int(height/14),int(height/14)))

indicator2 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator2 = pygame.transform.scale(indicator2,(int(height/14),int(height/14)))
indicator2 = pygame.transform.flip(indicator2,True,False)

indicator3 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator3 = pygame.transform.scale(indicator3,(int(height/14),int(height/14)))


# Positions for indicators along sliders - all of which scale horizontally
# with changes to height and width, or changes in indicator size.
positionslist1 = []
positionslist2 = []
for x in range(1,10):
    positionslist1.append((int(width/4+x*width/20 - indicator1.get_width()/2),int(height/2 - indicator1.get_height()/2)))
    positionslist2.append((int(width/4+x*width/20 - indicator1.get_width()/2),int(5*height/6 - indicator1.get_height()/2)))

positionslist3 = [(int(7*width/9),int(height/3)),(int(7*width/9),int(2*height/3))]

position1 = 0 # Current position, indicated by place in positionslist
position2 = 0
position3 = 0




def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(soundlabel,(int(width/4),int(height/3)))
    screen.blit(narrlabel,(int(width/4),int(2*height/3)))
    #pygame.draw.rect(screen, sliderColor, pygame.Rect(400, 300, 450, 50))
    #pygame.draw.rect(screen, sliderColor, pygame.Rect(400, 600, 450, 50))
    #far left lines
    #pygame.draw.lines(screen, lineColor, True, [(400, 280), (400, 370)], 5)
    #pygame.draw.lines(screen, lineColor, True, [(400, 580), (400, 670)], 5)
    #far right lines
    #pygame.draw.lines(screen, lineColor, True, [(850, 280), (850, 370)], 5)
    #pygame.draw.lines(screen, lineColor, True, [(850, 580), (850, 670)], 5)
    #middle lines
    #pygame.draw.lines(screen, lineColor, True, [(559, 280), (559, 370)], 5)
    #pygame.draw.lines(screen, lineColor, True, [(559, 580), (559, 670)], 5)
    #pygame.draw.lines(screen, lineColor, True, [(691, 280), (691, 370)], 5)
    #pygame.draw.lines(screen, lineColor, True, [(691, 580), (691, 670)], 5)
    screen.blit(indicator1,positionslist1[position1])
    screen.blit(indicator2,positionslist2[position2])
    pygame.display.update()

settingsfile = open("settings.txt","r") # Retrieve current status of settings
currentsettings = settingsfile.readlines() # from settings file.
position1 = int(currentsettings[0][0])
position2 = int(currentsettings[1][0])
settingsfile.close()

def updatesettingsfile(): # A function to pass the positions to the settings
    settingsfile = open("settings.txt","w") # status file.
    settingsfile.write(str(position1)+"\n"+str(position2))
    settingsfile.close()

drawscreen()

runsettings = True

while runsettings:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            updatesettingsfile()
            runsettings = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and position3 == 1: # pos 3 reflects
                position3 = 0                               # active indicator
                drawscreen()
            elif event.key == pygame.K_DOWN and position3 == 0:
                position3 = 1
                drawscreen()
            elif event.key == pygame.K_LEFT:
                if position3 == 0:
                    if position1 > 0:
                        position1 -= 1
                elif position3 == 1:
                    if position2 > 0:
                        position2 -= 1
                drawscreen()
            elif event.key == pygame.K_RIGHT:
                if position3 == 0:
                    if position1 < len(positionslist1):
                        position1 += 1
                elif position3 == 1:
                    if position2 < len(positionslist2):
                        position2 += 1
                drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                updatesettingsfile()
                runsettings = False
