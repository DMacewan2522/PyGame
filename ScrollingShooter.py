import pygame, sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyGame Assignment")

class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, xposition, yposition, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Player_Idle.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
        self.rect = self.image.get_rect()
        self.rect.center = (xposition, yposition)

playerModel = PlayerCharacter(200, 200, 3)


run = True
while run:

    screen.blit(playerModel.image, playerModel.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()