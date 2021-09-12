import pygame
import os

WIDTH, HEIGHT = 900, 500 # I can't figure out how to publish to GitHub through Atom, but I can edit the code and add
                         # to the repository directly by going to github.com
                         #deletethiscommentwhenyoureadit
                         #percentsignsmakebettercomments
                         #donemessingwithyourcodenow
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
WHITE = (255,255,255)
FPS = 60
WOLF_GREY_IMAGE = pygame.image.load(os.path.join('Assets', "greyWolf.png"))

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(WOLF_GREY_IMAGE, (450,250))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()
