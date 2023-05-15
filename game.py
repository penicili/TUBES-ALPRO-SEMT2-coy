import pygame
from sys import exit

# Menginisiasi pygame 
pygame.init()

# Membuat window
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Jumper')
# Membuat objek clock untuk mengatur framerate
clock = pygame.time.Clock()
# Membuat Font
gameFont = pygame.font.Font('font/Pixeltype.ttf', 50)

# Menambahkan surface (membuat gambar)
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSuface = pygame.image.load('graphics/ground.png').convert()
    # Teks
scoreSurf = gameFont.render('My game', False, (64,64,64)).convert()
scoreRect = scoreSurf.get_rect(center=(400,50))
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                playerGravity = -20
        # if event.type == pygame.MOUSEMOTION:
        #     if playerRect.collidepoint((event.pos)): print('collision')
                
    
    # Menempatkan surface pada display
    screen.blit(skySurface,(0,0))
    screen.blit(groundSuface,(0,300))
    pygame.draw.rect(screen, '#c0e8ec', scoreRect)
    pygame.draw.rect(screen, '#c0e8ec', scoreRect,10)
    screen.blit(scoreSurf,scoreRect)
        # Obstacle
    obstacleRect.x -= 4
    if obstacleRect.right <= 0: obstacleRect.left = 800
    screen.blit(obstacleSurface,obstacleRect)

        # Player
    playerGravity += 1
    playerRect.y += playerGravity
    screen.blit(playerSurface,playerRect)



    # Mengecek collision hitbox (rect)
    # if playerRect.colliderect(obstacleRect):
    #     print ('collision')
    
    


    # Me-refresh tampilan pada window
    pygame.display.update()

    # Mengatur framerate 60 fps
    clock.tick(60)