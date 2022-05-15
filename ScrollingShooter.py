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
FrameRate = 90

#Game Variables
gameGravity = 0.75

#Input variables
moveLeft = False
moveRight = False

#Set background colour and function to add background to the game screen
BGColour = (100, 130, 100)
REDColour = (255, 0, 0)
def createBackground():
    screen.fill(BGColour)
    pygame.draw.line(screen, REDColour, (0, 500), (SCREEN_WIDTH, 500))

#Player Class
class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, movespeed):
        self.playerIsAlive = True
        self.movespeed = movespeed
        self.movedirection = 1
        self.isJumping = False
        self.isAirborne = True
        self.yVelocity = 0
        self.directionChange = False
        self.animationList = []
        self.animationIndex = 0
        self.currentPlayerAction = 0
        self.timeTracker = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        #Idle Animation
        holding_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/PlayerIdle/Player_Idle_{i}.png')  #Assign the player's sprite an image based on animation playing
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale)))) #Change image size
            holding_list.append(img)
        self.animationList.append(holding_list)
        #Running Animation
        holding_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/PlayerRun/Player_Run_{i}.png')  #Assign the player's sprite an image based on animation playing
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale)))) #Change image size
            holding_list.append(img)
        self.animationList.append(holding_list)
        #Jumping Animation
        holding_list= []
        for i in range(4):
            img = pygame.image.load(f'assets/PlayerJump/Player_Jump_{i}.png')  # Assign the player's sprite an image based on animation playing
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))  # Change image size
            holding_list.append(img)
        self.animationList.append(holding_list)
        self.image = self.animationList[self.currentPlayerAction][self.animationIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #Function to place player onto the screen
    def createPlayer(self):
        screen.blit(pygame.transform.flip(self.image, self.directionChange, False),  self.rect)

    #Function that handles player animations on a timer
    def handleAnimations(self):
        #Timer for animation reset
        animationTimer = 100
        self.image = self.animationList[self.currentPlayerAction][self.animationIndex]
        if pygame.time.get_ticks() - self.timeTracker > animationTimer:
            self.animationIndex += 1        #Increase the list index by one each pass of the loop
            self.timeTracker = pygame.time.get_ticks()      #Reset timeTracker each pass of the loop
        if self.animationIndex >= len(self.animationList[self.currentPlayerAction]):      #Once the index reaches the length of the list...
            self.animationIndex = 0     #Reset the animation index to reset the animation

    #Change player action based on game state eg. running
    def definePlayerAction(self, newAction):        #Tells animation code which animation should be played when
        if newAction != self.currentPlayerAction:
            self.currentPlayerAction = newAction
            self.animationIndex = 0
            self.timeTracker = pygame.time.get_ticks()

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
        if self.isJumping == True and self.isAirborne == False:
            self.yVelocity = -11                #Detects when the player is jumping and changes yVelocity when it does so
            self.isJumping = False
            self.isAirborne = True
        #Gravity
        self.yVelocity += gameGravity
        twoy += self.yVelocity                  #Changes twoy coordinate based on yVelocity
        if self.rect.bottom + twoy > 500:
            twoy = 500 - self.rect.bottom
            self.isAirborne = False

        #Update position of player rectangle
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

    if playerModel.playerIsAlive:
        if playerModel.isAirborne:
            playerModel.definePlayerAction(2)   #Player is moving
        elif moveLeft or moveRight:
            playerModel.definePlayerAction(1)   #Player is moving
        else:
            playerModel.definePlayerAction(0)   #Player is idle

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
            if event.key == pygame.K_w and playerModel.playerIsAlive:
                playerModel.isJumping = True
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