import pygame
from sys import exit

# Menginisiasi pygame 
pygame.init()

# Membuat window
screen = pygame.display.set_mode((800,450))
pygame.display.set_caption('Jumper')
# Membuat objek clock untuk mengatur framerate
clock = pygame.time.Clock()

# Test
skySurface = pygame.image.load('Graphics_placeholder\sky_placeholder.png')

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
    # Me-refresh tampilan pada window
    pygame.display.update()
    # Mengatur framerate 60 fps
    clock.tick(60)