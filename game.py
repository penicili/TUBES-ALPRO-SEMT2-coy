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
testText = pygame.font.Font('font/Pixeltype.ttf', 50)

# Menambahkan surface (membuat gambar)
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSuface = pygame.image.load('graphics/ground.png').convert()
testTextSurf = testText.render('My game', False, 'red').convert()
    # Obstacle
obstacleSurface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
obstacleXpos = 600
    # Player
playerSurface = pygame.image.load('graphics/Player/player_stand.png')



# game loop
while True:
    # Event loop, mengecek segala input player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Menutup / menghancurkan window
            pygame.quit()
            exit()
    
    # Menempatkan surface pada display
    screen.blit(skySurface,(0,0))
    screen.blit(groundSuface,(0,300))
    screen.blit(testTextSurf,(300,50))
    # Membuat animasi untuk obstacle
    if obstacleXpos > -30:
        obstacleXpos -= 4
    else:
        obstacleXpos = 800
    screen.blit(obstacleSurface,(obstacleXpos,250))

    # Me-refresh tampilan pada window
    pygame.display.update()

    # Mengatur framerate 60 fps
    clock.tick(60)