import pygame
from sys import exit

# Scoreboard
def displayScore():
    playTime = int((pygame.time.get_ticks() - startTime)/200)
    scoreSurf = gameFont.render(f'{playTime}',False,(64,64,64))
    scoreRect= scoreSurf.get_rect(center= (400,50))
    screen.blit(scoreSurf,scoreRect)
# Menginisiasi pygame 
pygame.init()

# BGM
pygame.mixer.music.load('audio/bgm.mp3')
pygame.mixer.music.play()

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
GameOverText = gameFont.render('Game Over', False, (64,64,64)).convert()
gameOverRect = GameOverText.get_rect(center = (400,200))
    # Obstacle surface dan hitbox
obstacleSurface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
obstacleRect = obstacleSurface.get_rect(midbottom=(800,300))


    # Surface player dan hitboxnya
playerSurface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
playerRect = playerSurface.get_rect(midbottom=(80,300))

    # Gravitasi
playerGravity = 0

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
        if not gameActive:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    gameActive = True
                    obstacleRect.left = 800
                    startTime = pygame.time.get_ticks()
        
                
    if gameActive:
        # Menempatkan surface pada display
        screen.blit(skySurface,(0,0))
        screen.blit(groundSuface,(0,300))
        # pygame.draw.rect(screen, '#c0e8ec', scoreRect)
        # pygame.draw.rect(screen, '#c0e8ec', scoreRect,10)
        # screen.blit(scoreSurf,scoreRect)
        displayScore()
            # Obstacle
        obstacleRect.x -= 8
        if obstacleRect.right <= 0: obstacleRect.left = 800
        screen.blit(obstacleSurface,obstacleRect)
            # Player
        playerGravity += 1
        playerRect.y += playerGravity
        if playerRect.bottom > 300: playerRect.bottom = 300
        screen.blit(playerSurface,playerRect)

        # Game over
        if obstacleRect.colliderect(playerRect):
            gameActive = False
            pygame.mixer.pause()
    else:
        screen.fill('Yellow')
        screen.blit(GameOverText,gameOverRect)




    # Me-refresh tampilan pada window
    pygame.display.update()
    # Mengatur framerate 60 fps
    clock.tick(60)