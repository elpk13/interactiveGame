import pygame
import os

pygame.init()

#goals 
#    sound on/off



#the following lines set up the display window
height = 900 # Set the dimensions of the screen, by which
width = 1200  # everything will be scaled later.
screen = pygame.display.set_mode((width,height))

background = pygame.image.load(os.path.join('Assets',"winter_forest_background.jpg")) # Image credit:
background = pygame.transform.scale(background,(width,height)) # Linnaea Mallette,
                                                               # publicdomainpictures.net
# Select and scale an indicator to show what is selected
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator1,(int(height/12),int(height/12)))

# Positions for indicator:  to the right of any of the three buttons
positionslist1 = [(int(3*width/4),int(height/3)),(int(7*width/12),int(7*height/12)),
    (int(7*width/12),int(3*height/4))]
position1 = 0 # Current position, indicated by place in positionslist

def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(indicator1,positionslist1[position1])
    pygame.display.update()

drawscreen()

runsettings = True

while runsettings:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningmenu = False