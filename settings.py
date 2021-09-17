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
# Select and scale an indicator to show what is selected
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator1,(int(height/14),int(height/14)))

indicator2 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator2 = pygame.transform.scale(indicator2,(int(height/14),int(height/14)))

indicator3 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator3 = pygame.transform.scale(indicator3,(int(height/14),int(height/14)))


# Positions for indicator1 somewhere along the first slider - background sound
# width starts at 300 and ends at 600 
# height will be at 1/3 and 2/3 (first and second slider)
positionslist1 = [(int(width/3-25),int(height/3)),(int(4*width/9),int(height/3)),
    (int(5*width/9),int(height/3)),(int(2*width/3 + 25),int(height/3))]
positionslist2 = [(int(width/3 - 25),int(2*height/3)),(int(4*width/9),int(2*height/3)),
    (int(5*width/9),int(2*height/3)),(int(2*width/3 + 25),int(2*height/3))]
positionslist3 = [(int(7*width/9),int(height/3)),(int(7*width/9),int(2*height/3))]

position1 = 0 # Current position, indicated by place in positionslist
position2 = 0
position3 = 0




def drawscreen():
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, sliderColor, pygame.Rect(400, 300, 450, 50))
    pygame.draw.rect(screen, sliderColor, pygame.Rect(400, 600, 450, 50))
    #far left lines
    pygame.draw.lines(screen, lineColor, True, [(400, 280), (400, 370)], 5)
    pygame.draw.lines(screen, lineColor, True, [(400, 580), (400, 670)], 5)
    #far right lines
    pygame.draw.lines(screen, lineColor, True, [(850, 280), (850, 370)], 5)
    pygame.draw.lines(screen, lineColor, True, [(850, 580), (850, 670)], 5)
    #middle lines
    pygame.draw.lines(screen, lineColor, True, [(559, 280), (559, 370)], 5)
    pygame.draw.lines(screen, lineColor, True, [(559, 580), (559, 670)], 5)
    pygame.draw.lines(screen, lineColor, True, [(691, 280), (691, 370)], 5)
    pygame.draw.lines(screen, lineColor, True, [(691, 580), (691, 670)], 5)
    screen.blit(indicator1,positionslist1[position1])
    screen.blit(indicator2,positionslist2[position2])
    pygame.display.update()


drawscreen()

runsettings = True

while runsettings:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runsettings = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and position3 == 1: # indicator.
                position3 = 0
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
                    if position1 < 3:
                        position1 += 1
                elif position3 == 1:
                    if position2 < 3:
                        position2 += 1
                drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                runsettings = False


