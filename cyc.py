#The purpose of this file is to host the choose your character screen that follows the main menu
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
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator,(int(height/12),int(height/12)))
positions1list = [(int(3*width/4),int(height/3)),(int(7*width/12),int(7*height/12)),
    (int(7*width/12),int(3*height/4))]
position1 = 0

# Blit background, then buttons, then indicator, and update screen.
def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(indicator,positionslist[position])
    pygame.display.update()

drawscreen()

runningcyc = True

while runningcyc:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningcyc = False
