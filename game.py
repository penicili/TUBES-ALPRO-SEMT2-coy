import pygame
from sys import exit

# Menginisiasi pygame 
pygame.init()

# Membuat window
screen = pygame.display.set_mode((800,450))

# game loop
while True:
    # Event loop, mengecek segala input player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Menutup / menghancurkan window
            pygame.quit()
            exit()
            
    # Me-refresh tampilan pada window
    pygame.display.update()