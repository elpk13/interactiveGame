#The purpose of this file is to host the choose your character screen that follows the main menu
#eventually a difficulty setting will be integrated here or on the settings page.

#import necessary systems
import pygame
import os

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

# Set up the wolves' portrait images.
topleft = pygame.image.load(os.path.join('Assets',"Aspen_Headshot.png"))
topcent = pygame.image.load(os.path.join('Assets',"Khewa_Headshot.png"))
toprite = pygame.image.load(os.path.join('Assets',"Mani_Headshot.png"))
basleft = pygame.image.load(os.path.join('Assets',"Nico_Headshot.png"))
bascent = pygame.image.load(os.path.join('Assets',"Sparrow_Headshot.png"))
basrite = pygame.image.load(os.path.join('Assets',"Timber_Headshot.png"))
# Scale to uniform height without distorting.
topleft = pygame.transform.scale(topleft,(int(height/3),int(height*topleft.get_height()/(3*topleft.get_width()))))
topcent = pygame.transform.scale(topcent,(int(height/3),int(height*topcent.get_height()/(3*topcent.get_width()))))
toprite = pygame.transform.scale(toprite,(int(height/3),int(height*toprite.get_height()/(3*toprite.get_width()))))
basleft = pygame.transform.scale(basleft,(int(height/3),int(height*basleft.get_height()/(3*basleft.get_width()))))
bascent = pygame.transform.scale(bascent,(int(height/3),int(height*bascent.get_height()/(3*bascent.get_width()))))
basrite = pygame.transform.scale(basrite,(int(height/3),int(height*basrite.get_height()/(3*basrite.get_width()))))

#Set up the indicators used to make choices - will use a three indicator style like settings menu
# - but temporarily only need one indicator because starting with two wolves
indicator1 = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator1 = pygame.transform.scale(indicator1,(int(height/12),int(height/12)))
indicator1rad, ypos1, ypos2 = int(height/24), int(height/2)-int(height)/24, height-int(height/24)
positions1list = [(int(width/6)-indicator1rad,ypos1),(int(width/2)-indicator1rad,ypos1),(int(5*width/6)-indicator1rad,ypos1),
    (int(width/6)-indicator1rad,ypos2),(int(width/2)-indicator1rad,ypos2),(int(5*width/6)-indicator1rad,ypos2)]
position1 = 0

# Blit background, then portraits, then indicator, and update screen.
def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(topleft,(int(width/6-topleft.get_width()/2),int(height/12)))
    screen.blit(topcent,(int(width/2-topcent.get_width()/2),int(height/12)))
    screen.blit(toprite,(int(5*width/6-toprite.get_width()/2),int(height/12)))
    screen.blit(basleft,(int(width/6-basleft.get_width()/2),int(7*height/12)))
    screen.blit(bascent,(int(width/2-bascent.get_width()/2),int(7*height/12)))
    screen.blit(basrite,(int(5*width/6-basrite.get_width()/2),int(7*height/12)))
    screen.blit(indicator1,positions1list[position1])
    pygame.display.update()

drawscreen()

runningcyc = True

while runningcyc:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningcyc = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and position1 % 3 != 2:
                position1 += 1
            elif event.key == pygame.K_LEFT and position1 % 3 != 0:
                position1 -= 1
            elif event.key == pygame.K_UP and position1 > 2:
                position1 -= 3
            elif event.key == pygame.K_DOWN and position1 < 3:
                position1 += 3
            drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                import cychap
                drawscreen()
                #move on to the next screen -> chapter selection
