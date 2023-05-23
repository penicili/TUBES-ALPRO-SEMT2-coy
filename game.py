import pygame
from sys import exit
from random import randint

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
            obstacleRect.x -= 8
            if obstacleRect.bottom == 300:
                screen.blit(obstacleSurface1,obstacleRect)
            else:
                screen.blit(obstacleSurface2,obstacleRect)

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
pygame.display.set_caption('Jumper')
    # Membuat objek clock untuk mengatur framerate
clock = pygame.time.Clock()
    # Membuat Font
gameFont = pygame.font.Font('font/Pixeltype.ttf', 50)
    # Game over state
gameActive = True
    # Waktu utk score
startTime = 0
    # Menambahkan surface (membuat gambar)
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSuface = pygame.image.load('graphics/ground.png').convert()
    # Teks
# scoreSurf = gameFont.render('My game', False, (64,64,64)).convert()
# scoreRect = scoreSurf.get_rect(center=(400,50))
score = 0
GameOverText = gameFont.render('Game Over', False, (64,64,64)).convert()
gameOverRect = GameOverText.get_rect(center = (400,150))
RestartText = gameFont.render('Press R to restart', False, (64,64,64)).convert()
RestartRect = RestartText.get_rect(center=  (400,300))
    # Obstacle
obstacleSurface1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
obstacleSurface2 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
obstacleRectList = []


    # Surface player dan hitboxnya
playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
playerWalk = [playerWalk1,playerWalk2]
playerIndex = 0
playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
playerSurface = playerWalk[playerIndex]
playerRect = playerSurface.get_rect(midbottom=(80,300))
    # Gravitasi
playerGravity = 0
    # Timers
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1400)
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
                    obstacleRectList.append(obstacleSurface1.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstacleRectList.append(obstacleSurface2.get_rect(midbottom=(randint(900,1100),210)))
                    


        if not gameActive:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
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
        # screen.blit(obstacleSurface1,obstacleRect1)
        obstacleRectList = obstacleMovement(obstacleRectList)
            # Player
        playerGravity += 1
        playerRect.y += playerGravity
        if playerRect.bottom > 300: playerRect.bottom = 300
        playerAnimation()
        screen.blit(playerSurface,playerRect)

        # Game over
        # if obstacleRect1.colliderect(playerRect):
        #     gameActive = False
        gameActive = collisions(playerRect,obstacleRectList)
# Game over State
    else:
        gameOverScore = gameFont.render(f'Score: {score}', False, (64, 64, 64)).convert()
        gameOverSRect = gameOverScore.get_rect(center=(400,200))
        playerRect.midbottom= (80,300)
        obstacleRectList.clear()
        playerGravity = 0
        screen.fill((94,129,162))
        screen.blit(GameOverText,gameOverRect)
        screen.blit(gameOverScore,gameOverSRect)
        screen.blit(RestartText,RestartRect)





    # Me-refresh tampilan pada window
    pygame.display.update()
    # Mengatur framerate 60 fps
    clock.tick(60)