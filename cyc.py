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
# - but temporarily only need one indicator because starting with two wolves
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator1,(int(height/12),int(height/12)))
positions1list = [(int(width/3 - 50),int(height/2)),(int(2*width/3 - 50),int(height/2))]
position1 = 0

# Blit background, then buttons, then indicator, and update screen.
def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(indicator1,positions1list[position1])
    pygame.display.update()

drawscreen()

runningcyc = True

while runningcyc:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningcyc = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT and position1 == 0:
                position1 = 1
            elif event.key == pygame.K_LEFT and position1 == 1:
                position1 = 0
            drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                import cychap
                drawscreen()
                #move on to the next screen -> chapter selection
            