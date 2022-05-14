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
        self.animationList = []
        self.animationIndex = 0
        self.timeTracker = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        for i in range(4):
            img = pygame.image.load(f'assets/Player_Idle_{i}.png')  #Assign the player's sprite an image
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale)))) #Change image size
            self.animationList.append(img)
        self.image = self.animationList[self.animationIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #Function to place player onto the screen
    def createPlayer(self):
        screen.blit(pygame.transform.flip(self.image, self.directionChange, False),  self.rect)

    #Function that handles player animations on a timer
    def handleAnimations(self):
        #Timer for animation reset
        animationTimer = 300
        self.image = self.animationList[self.animationIndex]
        if pygame.time.get_ticks() - self.timeTracker > animationTimer:
            self.animationIndex += 1        #Increase the list index by one each pass of the loop
            self.timeTracker = pygame.time.get_ticks()      #Reset timeTracker each pass of the loop
        if self.animationIndex >= len(self.animationList):      #Once the index reaches the length of the list...
            self.animationIndex = 0     #Reset the animation index to reset the animation

    #Function that handles player movements
    def playerMovement(self, moveLeft, moveRight):
        twox = 0
        twoy = 0
        if moveLeft:
            twox = -self.movespeed
            self.directionChange = True
            self.direction = -1
        if moveRight:                           #Detects when the player is moving left to notify the game on when to flip the sprite
            twox = self.movespeed
            self.directionChange = False
            self.direction = 1
        self.rect.x += twox
        self.rect.y += twoy




#Create player
playerModel = PlayerCharacter(200, 200, 2, 5)




#Game Loop
run = True
while run:
    #Game Initializations
    clock.tick(FrameRate)
    createBackground()
    playerModel.handleAnimations()
    playerModel.createPlayer()
    playerModel.playerMovement(moveLeft, moveRight)

    #Check for the game ending in order to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Player Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:     #Move left
                moveLeft = True
            if event.key == pygame.K_d:     #Move right
                moveRight = True
            if event.key == pygame.K_ESCAPE:    #Close the game
                run = False
        #Stop Movements
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:     #Stop left movement
                moveLeft = False
            if event.key == pygame.K_d:     #Stop right movement
                moveRight = False

    #Keep game display updated with new information
    pygame.display.update()

pygame.quit()