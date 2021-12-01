import pygame
import os

def get_menu_graphics(window_width,window_height):

    menuGraphics = { }

    # Load background, crop to same aspect ratio as window, and scale to size
    # of window.
    background = pygame.image.load(os.path.join('Assets','winter_forest_background.jpg')) # Image credit:
    bgw, bgh = background.get_width(), background.get_height() # Linnaea Mallette, publicdomainpictures.net
    if window_width / bgw > window_height > bgh:
        background = background.subsurface(int((bgw - bgh*window_width/window_height)/2),0,int(bgh*window_width/window_height),bgh)
    else:
        background = background.subsurface(0,int((bgh-bgw*window_height/window_width)/2),bgw,int(bgw*window_height/window_width))
    background = pygame.transform.scale(background,(window_width,window_height))
    menuGraphics['background'] = background

    # Load buttons and scale to appropriate portions of window.
    playbutton = pygame.image.load(os.path.join('Assets',"play_button.jpg"))
    playbutton = pygame.transform.scale(playbutton,(int(window_width/2),int(window_height/4)))
    settingsbutton = pygame.image.load(os.path.join('Assets',"settings_button.jpg"))
    settingsbutton = pygame.transform.scale(settingsbutton,(int(window_width/6),int(window_height/12)))
    aboutbutton = pygame.image.load(os.path.join('Assets',"about_button.jpg"))
    aboutbutton = pygame.transform.scale(aboutbutton,(int(window_width/6),int(window_height/12)))
    menuGraphics['about'] = aboutbutton
    menuGraphics['play'] = playbutton
    menuGraphics['settings'] = settingsbutton

    soundlabel = pygame.image.load(os.path.join('Assets',"sound_effects_label.png"))
    soundlabel = pygame.transform.scale(soundlabel,(int(window_width/2),int(window_height/6)))
    narrlabel = pygame.image.load(os.path.join('Assets',"narration_label.png"))
    narrlabel = pygame.transform.scale(narrlabel,(int(window_width/2),int(window_height/6)))
    menuGraphics['sound'] = soundlabel
    menuGraphics['narration'] = narrlabel

    indicator = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
    indicator = pygame.transform.scale(indicator,(int(window_height/12),int(window_height/12)))
    indicator2 = pygame.transform.flip(indicator,True,False)
    menuGraphics['indicator'] = indicator
    menuGraphics['indicator2'] = indicator2

    return menuGraphics
