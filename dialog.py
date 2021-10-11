import pygame
pygame.init()
import os

def dialog(swidth,sheight,question,options,image=None,width=0.5,height=1/3):
    screen = pygame.display.set_mode((swidth,sheight))
    dialogbg = pygame.image.load(os.path.join("Assets","Dialog_Panel.jpg"))
    dialogbg = pygame.transform.scale(dialogbg,(int(width*swidth),int(height*sheight)))
    paw = pygame.image.load(os.path.join("Assets","indicator_paw.png"))
    paw = pygame.transform.scale(paw,(int(sheight/12),int(sheight/12)))

    runningwidth = int((1-width)*swidth/2)
    runningheight = int(sheight/3 - height*sheight/2)
    buffer = 10
    myfont = pygame.font.SysFont('constantia',24)
    TEXT_COLOR = (239,228,176)
    choice = 0

    def drawscreen(runningwidth,runningheight,buffer,image):
        screen.blit(dialogbg,(runningwidth,runningheight))
        runningwidth += buffer
        runningheight += buffer
        if question != "":
            question_text = myfont.render(question, True, TEXT_COLOR)
            screen.blit(question_text,(int((swidth - question_text.get_width())/2),runningheight))
            runningheight += int(question_text.get_height())
            runningheight += buffer
        if image != None:
            image = pygame.transform.scale(image,(int(0.5*width*swidth-2*buffer),int(sheight/3+height*sheight/2-runningheight-buffer)))
            screen.blit(image,(int(swidth/2 + buffer),runningheight))
        optionpos = []
        for option in options:
            option_text = myfont.render(option, True, TEXT_COLOR)
            screen.blit(option_text,(runningwidth,runningheight))
            runningheight += option_text.get_height()
            runningheight += buffer
            optionpos.append((int(runningwidth + option_text.get_width()/2 + paw.get_width()/2),int(runningheight - option_text.get_height()/2 - paw.get_height()/2)))
        screen.blit(paw,optionpos[choice])
        pygame.display.update()

    drawscreen(runningwidth,runningheight,buffer,image)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return choice
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and choice > 0:
                    choice -= 1
                elif event.key == pygame.K_DOWN and choice < len(options) - 1:
                    choice += 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return choice
                drawscreen(runningwidth,runningheight,buffer,image)
