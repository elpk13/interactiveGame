# This script runs the 'about' page that can be accessed from  the main menu.
import pygame

# Open and read file of text to display.
gameinfofile = open("about.txt","r")
gameinfolines = gameinfofile.readlines()

# Choose background colors and text colors.
BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (200,200,200)

# This function does the work of placing the text.  It is a function
# so that the surface on which things must be drawn, screen, can be
# passed to it from main_menu.py.  The argument and the item sent to
# it share the name 'screen'.
def displaygameinfo(screen):

    # Size and place a large mid-screen rectangle.
    height = int(screen.get_height()*0.75)
    width = int(screen.get_width()*0.5)
    left = int(screen.get_width()/4)
    down = int(left/2)
    mainrectangle = pygame.Rect(left,down,width,height)
    pygame.draw.rect(screen,BACKGROUND_COLOR,mainrectangle)

    # Each line of text is to be placed in a new rectangle.
    # Python/pygame does not conveniently handle line breaks.
    newrectangle = mainrectangle
    myfont = pygame.font.SysFont('constantia',24)
    for infoline in gameinfolines:
        if len(infoline) > 0:
            infoline = infoline[:-1] # Remove line break from end of line
        textdisplay = myfont.render(infoline, True, (100,100,100),(0,0,0))
        screen.blit(textdisplay,newrectangle)
        newrectangle = newrectangle.move(0,textdisplay.get_height())

    pygame.display.update()

    aboutscreen = True
    while aboutscreen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and ( event.key == pygame.K_SPACE or event.key == pygame.K_RETURN ):
                aboutscreen = False
            elif event.type == pygame.QUIT:
                aboutscreen = False
