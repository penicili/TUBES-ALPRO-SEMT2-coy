import pygame
from sys import exit
from random import randint




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.playerWalk = [playerWalk1,playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

    def playerInput(self):
        keys =pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def applyGravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def playerAnimation(self):
        if self.rect.bottom <= 300: 
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex > len(self.playerWalk):
                self.playerIndex = 0
                self.image = self.playerWalk[int(self.playerIndex)]
                
    def update(self):
        self.playerInput()
        self.applyGravity()



# Scoreboard
def displayScore():
    playTime = int((pygame.time.get_ticks() - startTime)/1000)
    scoreSurf = gameFont.render(f'Score: {playTime}',False,(64,64,64))
    scoreRect= scoreSurf.get_rect(center= (400,50))
    screen.blit(scoreSurf,scoreRect)
    return playTime


# Obstacle Movement
def obstacleMovement(obstacleList):
    if obstacleList:
        for obstacleRect in obstacleList:
            obstacleRect.x -= 5.5
            if obstacleRect.bottom == 300:
                screen.blit(snailSurf,obstacleRect)
            else:
                screen.blit(flySurf,obstacleRect)

        obstacleList = [obstacle for obstacle in obstacleList if obstacle.x > -100]
        return obstacleList
    else: return []


# Collision
def collisions(player, obsRects):
    if obsRects:
        for obsRect in obsRects:
            if player.colliderect(obsRect):
                return False
    return True


# Player Animation
def playerAnimation():
    global playerSurface, playerIndex
    if playerRect.bottom < 300:
        #Lompat ketika di atas
        playerSurface = playerJump
    else:
        #Jalan ketika di ground
        playerIndex += 0.1
        if playerIndex >= len(playerWalk): playerIndex = 0
        playerSurface = playerWalk[int(playerIndex)]


# Menginisiasi pygame 
pygame.init()


    # Membuat window
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Hell nah dude')


    # Membuat objek clock untuk mengatur framerate
clock = pygame.time.Clock()


    # Membuat Font
gameFont = pygame.font.Font('font/Pixeltype.ttf', 50)


    # Game over state
gameActive = True


    # Waktu utk score
startTime = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

    # Menambahkan surface (membuat gambar)
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSuface = pygame.image.load('graphics/ground.png').convert()


    # Teks
# scoreSurf = gameFont.render('My game', False, (64,64,64)).convert()
# scoreRect = scoreSurf.get_rect(center=(400,50))
score = 0
GameOverText = gameFont.render('Game Over', False, (64,64,64)).convert()
gameOverRect = GameOverText.get_rect(center = (400,50))
RestartText = gameFont.render('Restart', False, (64,64,64)).convert()
RestartRect = RestartText.get_rect(center=  (400,225))
restartButton = pygame.image.load('Graphics_placeholder/button_pixelated.png').convert_alpha()
restartButton = pygame.transform.scale(restartButton, (int(restartButton.get_width() * 0.5), int(restartButton.get_height() * 0.5)))
restartRect = restartButton.get_rect(center= (400,225))


    # Obstacle
snailFrame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrames = [snailFrame1,snailFrame2]
snailFrameIndex = 0
snailSurf = snailFrames[snailFrameIndex]

flyFrame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
flyFrame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
flyFrames = [flyFrame1, flyFrame2]
flyFrameIndex = 0
flySurf = flyFrames[flyFrameIndex]

obstacleRectList = []


    # Surface player dan hitboxnya
playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
playerWalk = [playerWalk1,playerWalk2]
playerIndex = 0
playerSurface = playerWalk[playerIndex]
playerRect = playerSurface.get_rect(midbottom=(80,300))


    # Gravitasi
playerGravity = 0


    # Timers
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1400)

snailAnimaTimer = pygame.USEREVENT +2
pygame.time.set_timer(snailAnimaTimer,500)

flyAnimaTimer = pygame.USEREVENT +3
pygame.time.set_timer(flyAnimaTimer,250)

# game loop
while True:
# Event loop, mengecek segala input player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Menutup / menghancurkan window
            pygame.quit()
            exit()
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and playerRect.bottom >= 300: 
                    playerGravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerRect.collidepoint((event.pos)) and playerRect.bottom >= 300:
                    playerGravity = -20
            if event.type == obstacleTimer:
                if randint(0,2):
                    obstacleRectList.append(snailSurf.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstacleRectList.append(flySurf.get_rect(midbottom=(randint(900,1100),210)))
            if event.type == snailAnimaTimer:
                if snailFrameIndex == 0 : snailFrameIndex =1
                else: snailFrameIndex = 0
                snailSurf = snailFrames[snailFrameIndex]
            if event.type == flyAnimaTimer:
                if flyFrameIndex == 0 : flyFrameIndex = 1
                else: flyFrameIndex = 0
                flySurf = flyFrames[flyFrameIndex]


        if not gameActive:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    gameActive = True
                    startTime = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and restartRect.collidepoint(event.pos):
                    gameActive = True
                    startTime = pygame.time.get_ticks()
        

# Game running State          
    if gameActive:
        # Menempatkan surface pada display
        screen.blit(skySurface,(0,0))
        screen.blit(groundSuface,(0,300))
        # pygame.draw.rect(screen, '#c0e8ec', scoreRect)
        # pygame.draw.rect(screen, '#c0e8ec', scoreRect,10)
        # screen.blit(scoreSurf,scoreRect)
        score = displayScore()
            # Obstacle
        # obstacleRect1.x -= 8
        # if obstacleRect1.right <= 0: obstacleRect1.left = 800
        # screen.blit(snailFrame1,obstacleRect1)
        obstacleRectList = obstacleMovement(obstacleRectList)
            # Player
        playerGravity += 1
        playerRect.y += playerGravity
        if playerRect.bottom > 300: playerRect.bottom = 300
        playerAnimation()
        screen.blit(playerSurface,playerRect)
        player.draw(screen)
        player.update()
        # Game over
        # if obstacleRect1.colliderect(playerRect):
        #     gameActive = False
        gameActive = collisions(playerRect,obstacleRectList)


# Game over State
    else:
        gameOverScore = gameFont.render(f'Score: {score}', False, (64, 64, 64)).convert()
        gameOverSRect = gameOverScore.get_rect(center=(400,150))
        playerRect.midbottom= (80,300)
        obstacleRectList.clear()
        playerGravity = 0
        screen.fill((108, 198, 240))
        screen.blit(GameOverText,gameOverRect)
        screen.blit(gameOverScore,gameOverSRect)
        screen.blit(restartButton,restartRect)
        screen.blit(RestartText,RestartRect)





    # Me-refresh tampilan pada window
    pygame.display.update()
    # Mengatur framerate 60 fps
    clock.tick(60)