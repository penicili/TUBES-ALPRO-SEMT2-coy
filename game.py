import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.playerWalk = [playerWalk1,playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jumpSound = pygame.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.5)

    def playerInput(self):
        keys =pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jumpSound.play()

    def applyGravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def playerAnimation(self):
        if self.rect.bottom < 300: 
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk): self.playerIndex = 0
            self.image = self.playerWalk [int(self.playerIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.playerAnimation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'snail':
            snailFrame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snailFrame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snailFrame1,snailFrame2]
            y_pos =300
        else:
            flyFrame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            flyFrame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [flyFrame1, flyFrame2]
            y_pos = 210
        self.animationIndex = 0
        self.image = self.frames [self.animationIndex]
        self.rect = self.image.get_rect(midbottom = ((randint(900,1100)),y_pos))

    def obsAnimation(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames): self.animationIndex = 0 
        self.image = self.frames[int(self.animationIndex)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.obsAnimation()
        self.rect.x -= 6
        self.destroy()

class Button():
    def __init__(self, x, y, image, scale):
        self.clickSound = pygame.mixer.Sound('audio/8bitClick.mp3')
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False


    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                self.clickSound.play()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Scoreboard
def displayScore():
    playTime = int((pygame.time.get_ticks() - startTime)/1000)
    scoreSurf = gameFont.render(f'Score: {playTime}',False,(64,64,64))
    scoreRect= scoreSurf.get_rect(center= (400,50))
    screen.blit(scoreSurf,scoreRect)
    return playTime


# Collision
def collisions(player, obsRects):
    if obsRects:
        for obsRect in obsRects:
            if player.colliderect(obsRect):
                return False
    return True


def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    else: return True


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

    # Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

    # Surfaces
obstacleGroup = pygame.sprite.Group()
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSuface = pygame.image.load('graphics/ground.png').convert()

score = 0

bgm = pygame.mixer.Sound('audio/music.wav')
bgm.play(loops= -1)

GameOverText = gameFont.render('Game Over', False, (64,64,64)).convert()
gameOverRect = GameOverText.get_rect(center = (400,50))

RestartText = gameFont.render('Restart', False, (0,0,0)).convert()
RestartText = pygame.transform.scale(RestartText, (int(RestartText.get_width())* 1.2, int(RestartText.get_height())* 1.2))
RestartRect = RestartText.get_rect(center=  (400,253))



gameOverScore = gameFont.render(f'Score: {score}', False, (64, 64, 64)).convert()
gameOverSRect = gameOverScore.get_rect(center=(400,150))

buttonimg = pygame.image.load('graphics/buttonimage.png').convert_alpha()
# buttonimg = pygame.transform.scale(buttonimg, (int (buttonimg.get_width()* 5), int(buttonimg.get_height())* 5))
# restartButtonRect = buttonimg.get_rect(center = (400, 255))
restartButton = Button(400, 255, buttonimg, 5)



    # Timers
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1400)

# Game loop
while True:
# Event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # Close
            pygame.quit()
            exit()
        if gameActive:
            if event.type == obstacleTimer:               
                obstacleGroup.add(Obstacle(choice(['fly','snail','snail','snail','snail'])))


        if not gameActive:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    gameActive = True
                    startTime = pygame.time.get_ticks()

        

# Game running State          
    if gameActive:
        screen.blit(skySurface,(0,0))
        screen.blit(groundSuface,(0,300))
        # Score
        score = displayScore()
        # Player
        player.draw(screen)
        player.update()
        # Obstacle
        obstacleGroup.draw(screen)
        obstacleGroup.update()

        # Game over
        gameActive = collisionSprite()


# Game over State
    else:
        screen.fill((108, 198, 240))
        screen.blit(GameOverText,gameOverRect)
        screen.blit(gameOverScore,gameOverSRect)
        if restartButton.draw(screen):
            gameActive = True
            startTime = pygame.time.get_ticks()
        screen.blit(RestartText,RestartRect)

    pygame.display.update()
    clock.tick(60)