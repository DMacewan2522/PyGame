import pygame, sys, random         #Initialize Libraries
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
enemySpawnRate = 300

#Input variables
moveLeft = False
moveRight = False
shootGun = False

#Bullet Image
bulletImage = pygame.image.load(f'assets/bullet.png')

#Set background image and function to add ground to game
backGroundImage = pygame.image.load(f'Assets/Background.png')
backGroundImage = pygame.transform.scale(backGroundImage, (int(backGroundImage.get_width() * 2), (int(backGroundImage.get_height() * 2))))
floorPlatform = pygame.image.load(f'Assets/ShooterPlatform.png')
floorPlatform = pygame.transform.scale(floorPlatform, (int(floorPlatform.get_width() / 1.25), (int(floorPlatform.get_height() / 1.25))))
ColourBlack = (0, 0, 0)
def createFloor():
    pygame.draw.line(screen, ColourBlack, (0, 500), (SCREEN_WIDTH, 500))
    screen.blit(floorPlatform, (0, 500))



#Player Class
class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, movespeed):
        self.playerIsAlive = True
        self.health = 100
        self.maximumHealth = self.health
        self.shootCooldown = 0
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
            img = pygame.image.load(f'assets/PlayerIdle/Player_Idle_{i}.png').convert_alpha()  #Assign the player's sprite an image based on animation playing
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale)))) #Change image size
            holding_list.append(img)
        self.animationList.append(holding_list)
        #Running Animation
        holding_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/PlayerRun/Player_Run_{i}.png').convert_alpha()  #Assign the player's sprite an image based on animation playing
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale)))) #Change image size
            holding_list.append(img)
        self.animationList.append(holding_list)
        #Jumping Animation
        holding_list= []
        for i in range(4):
            img = pygame.image.load(f'assets/PlayerJump/Player_Jump_{i}.png').convert_alpha()  # Assign the player's sprite an image based on animation playing
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

    def update(self):
        self.handleAnimations()
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

    def playerShoot(self):
        if self.shootCooldown == 0:
            self.shootCooldown = 20
            bullet = Bullet(playerModel.rect.centerx + (0.9 * playerModel.rect.size[0] * playerModel.movedirection),
                            playerModel.rect.centery - (0.4 * playerModel.rect.size[0]), playerModel.movedirection)
            bulletSpriteGroup.add(bullet)

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
            self.movedirection = -1
        if moveRight:                           #Detects when the player is moving left to notify the game on when to flip the sprite
            twox = self.movespeed
            self.directionChange = False
            self.movedirection = 1
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
        #Border Collision
        if self.rect.left + twox < 0:
            twox = 0  -self.rect.left
        if self.rect.right + twox > SCREEN_WIDTH:
            twox = SCREEN_WIDTH -self.rect.right

        #Update position of player rectangle
        self.rect.x += twox
        self.rect.y += twoy

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.isAlive = True
        self.enemySpeed = 3
        self.yVelocity = 0
        self.image = pygame.image.load(f'Assets/Drone_Fly.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.spawnCooldown = 20
    def update(self):
        self.rect.x += (self.direction * self.enemySpeed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
    def spawnEnemy(self):
        enemySpriteGroup.add(enemy)

enemySpriteGroup = pygame.sprite.Group()

#Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.bulletSpeed = 5
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
        #Move bullet
        self.rect.x += (self.direction * self.bulletSpeed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

bulletSpriteGroup = pygame.sprite.Group()

#Create player
playerModel = PlayerCharacter(200, 200, 2, 5)

enemy = Enemies(100, 100, 0)

#Game Loop
run = True
while run:
    #Game Initializations
    screen.blit(backGroundImage, (0, 0))
    clock.tick(FrameRate)
    createFloor()
    playerModel.createPlayer()
    bulletSpriteGroup.update()
    bulletSpriteGroup.draw(screen)
    enemySpriteGroup.update()
    enemySpriteGroup.draw(screen)
    playerModel.update()

    enemySpawnRate -= 1
    if enemySpawnRate == 0:
        tempRandomXSpawn = random.randint(0, 1)
        if tempRandomXSpawn == 0:
            enemy = Enemies(0, 440, 1)
            enemy.spawnEnemy()
            enemySpawnRate = 300
        elif tempRandomXSpawn == 1:
            enemy = Enemies(800, 440, -1)
            enemy.spawnEnemy()
            enemySpawnRate = 300

    if playerModel.playerIsAlive:
        if shootGun:
            playerModel.playerShoot()
        if playerModel.isAirborne:
            playerModel.definePlayerAction(2)   #Player is jumping
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
            if event.key == pygame.K_w and playerModel.playerIsAlive:       #Player Jumping
                playerModel.isJumping = True
            if event.key == pygame.K_SPACE:
                shootGun = True
            if event.key == pygame.K_ESCAPE:    #Close the game
                run = False
        #Stop Movements
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:     #Stop left movement
                moveLeft = False
            if event.key == pygame.K_d:     #Stop right movement
                moveRight = False
            if event.key == pygame.K_SPACE:
                shootGun = False

    #Keep game display updated with new information
    pygame.display.update()

pygame.quit()