import pygame, sys
    #Initialize PyGame
pygame.init()

#Set screen height and width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#Set game screen to assigned height and width
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyGame Assignment")

#Game Framerate
clock = pygame.time.Clock()
FrameRate = 60

#Input variables
moveLeft = False
moveRight = False

#Set background colour and function to add background to the game screen
backGround = (100, 130, 100)
def createBackground():
    screen.fill(backGround)

#Player Class
class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, movespeed):
        self.movespeed = movespeed
        self.movedirection = 1
        self.directionChange = False
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Gunner_Idle.gif')  #Assign the player's sprite an image
        #Change image size according to game size
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    #Function to place player onto the screen
    def createPlayer(self):
        screen.blit(pygame.transform.flip(self.image, self.directionChange, False),  self.rect)
    #Function that handles player movements
    def playerMovement(self, moveLeft, moveRight):
        twox = 0
        twoy = 0
        if moveLeft:
            twox = -self.movespeed
            self.directionChange = True
            self.direction = -1
        if moveRight:
            twox = self.movespeed
            self.directionChange = False
            self.direction = 1
        self.rect.x += twox
        self.rect.y += twoy

#Create player
playerModel = PlayerCharacter(200, 200, 3, 5)

#Game Loop
run = True
while run:
    #Game Initializations
    clock.tick(FrameRate)
    createBackground()
    playerModel.createPlayer()
    playerModel.playerMovement(moveLeft, moveRight)

    #Check for the game ending in order to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Player Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #Stop Movements
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

    #Keep game display updated with new information
    pygame.display.update()

pygame.quit()