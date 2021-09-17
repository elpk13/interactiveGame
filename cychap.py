#The purpose of this file is to host the choose your chapter screen that follows the choose your 
#eventually a difficulty setting will be integrated here or on the settings page. 

#import necessary systems
import pygame
import os

#drawings of characters will be initialized here


#inits
pygame.init()


#set the parameters for the pygame window
height = 900 # Set the dimensions of the screen, by which
width = 1200  # everything will be scaled later.
screen = pygame.display.set_mode((width,height))

# Select and size background image
background = pygame.image.load(os.path.join('Assets',"winter_forest_background.jpg")) # Image credit:
background = pygame.transform.scale(background,(width,height)) # Linnaea Mallette,
                                                               # publicdomainpictures.net

#Set up the indicators used to make choices - will use a three indicator style like settings menu 
# - but temporarily only need one indicator because starting with two wolves
indicator = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator = pygame.transform.scale(indicator,(int(height/12),int(height/12)))
positionslist = [(int(width/4 - 50),int(height/2 + 100)),(int(2*width/4 - 50),int(height/2 + 100)), 
    (int(3*width/4 - 50),int(height/2 + 100))]
position = 0

# Blit background, then buttons, then indicator, and update screen.
def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(indicator,positionslist[position])
    pygame.display.update()

drawscreen()

runningcychap = True
while runningcychap:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningcychap = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and position < 2:
                position += 1
            elif event.key == pygame.K_LEFT and position > 0:
                position -= 1
            drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if position == 0:
                    #chapter1
                    pass
                elif position == 1:
                    #chapter2
                    pass
                elif position == 2:
                    #chapter3
                    pass

