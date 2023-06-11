import pygame
from sys import exit
from random import randint, choice
import math

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range (pygame.joystick.get_count())]

joyStatus = False
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.playerWalk = [playerWalk1,playerWalk2]
        self.playerIndex = 0
        self.playerJump  = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jumpSound = pygame.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.7)

    def playerInput(self):
        keys =pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jumpSound.play()
        if joyStatus == True:
            aabs= pygame.joystick.Joystick(0).get_button(0)
            if aabs and self.rect.bottom >= 300:
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

    # Game Status
gameStatus = 'Menu'

    # Waktu utk score
startTime = 0

    # Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacleGroup = pygame.sprite.Group()


clickSound = pygame.mixer.Sound('audio/8bitClick.mp3')


    # Surfaces
skySurface = pygame.image.load('Lv1_Graphics/parallax-mountain-bg.png')
skySurface = pygame.transform.scale(skySurface, (int(skySurface.get_width())*3, int(skySurface.get_height())*3)).convert_alpha()
MountainSurface = pygame.image.load('Lv1_Graphics/mountains_cut.png')
MountainSurface = pygame.transform.scale(MountainSurface,(int(MountainSurface.get_width())*4, int(MountainSurface.get_height())*4)).convert_alpha()
groundSuface = pygame.image.load('Lv1_Graphics/ground.png').convert()
citySurface = pygame.image.load('Lv1_Graphics/city_cut.png')
citySurface = pygame.transform.scale(citySurface, (int(citySurface.get_width())*4, int(citySurface.get_height()*4))).convert_alpha()
skyDay = pygame.image.load('graphics/Sky.png').convert()
logo = pygame.image.load('graphics/still guy run.png').convert_alpha()
logoRect = logo.get_rect(center= (400,120))





MountainWidth = MountainSurface.get_width()
bgWidth = groundSuface.get_width()
cityWidth = citySurface.get_width()

tiles = math.ceil(800/MountainWidth) + 1
tilesGround = math.ceil(800/bgWidth) + 1
tilesCity = math.ceil(800/cityWidth) + 1

scroll = 0
groundScroll = 0
cityScroll = 0

score = 0

bgm = pygame.mixer.Sound('audio/music.wav')
bgm.play(loops= -1)

GameOverText = gameFont.render('Game Over', False, (64,64,64)).convert()
gameOverRect = GameOverText.get_rect(center = (400,50))

RestartText = gameFont.render('Restart', False, (100,100,100)).convert()
RestartRect = RestartText.get_rect(center=  (400,253))
startText = gameFont.render('Normal', False, (100,100,100)).convert()
startRect = startText.get_rect(center=  (300,255))
startText1 = gameFont.render('Normal +', False, (100,100,100)).convert()
startRect1 = startText1.get_rect(center=  (500,255))





buttonimg = pygame.image.load('graphics/buttoncoy.png').convert_alpha()
# buttonimg = pygame.transform.scale(buttonimg, (int (buttonimg.get_width()* 5), int(buttonimg.get_height())* 5))
# restartButtonRect = buttonimg.get_rect(center = (400, 255))
restartButton = Button(400, 255, buttonimg, 3)
startButton = Button (300, 255, buttonimg, 3)
startButton2 = Button (500, 255, buttonimg, 3)


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


        if gameStatus == 'Running':
            if event.type == obstacleTimer:               
                obstacleGroup.add(Obstacle(choice(['fly','snail','snail','snail','snail'])))
            if event.type == pygame.JOYDEVICEADDED:
                joyStatus == True
                clickSound.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gameStatus = 'Menu'
                clickSound.play()

        if gameStatus == 'Over':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    clickSound.play()
                    gameStatus = "Running"
                    startTime = pygame.time.get_ticks()
            if joyStatus:
                if pygame.joystick.Joystick(0).get_button(7):
                    clickSound.play()
                    gameStatus = 'Running'
                    startTime = pygame.time.get_ticks()

        


# Game running State
    if gameStatus != 'Running2':
        screen.blit(skySurface,(0,0))
        for i in range (0, tiles):
            screen.blit(MountainSurface, ((i * MountainWidth + scroll ), 130))
        for i in range (0, tiles):
            screen.blit(citySurface,((i* cityWidth + cityScroll), 170))
        for i in range (-1, 2):
            screen.blit(groundSuface, ((i * bgWidth + groundScroll ), 300))
        if abs(scroll) > MountainWidth:
            scroll = 0
        if abs(groundScroll) > bgWidth:
            groundScroll = 0
        if abs (cityScroll) >  cityWidth:
            cityScroll = 0

    if gameStatus == 'Running2':
        screen.blit(skySurface,(0,0))
        for i in range (0, tiles):
            screen.blit(MountainSurface, ((i * MountainWidth + scroll ), 130))
        for i in range (0, tiles):
            screen.blit(citySurface,((i* cityWidth + cityScroll), 170))
        for i in range (-1, 2):
            screen.blit(groundSuface, ((i * bgWidth + groundScroll ), 300))
        if abs(scroll) > MountainWidth:
            scroll = 0
        if abs(groundScroll) > bgWidth:
            groundScroll = 0
        if abs (cityScroll) >  cityWidth:
            cityScroll = 0
        
        

    # scroll bg
    scroll -= 1
    groundScroll -= 6
    cityScroll -= 4

    # Player
    player.draw(screen)
    player.update()
    if gameStatus == 'Menu':
        screen.blit(logo,logoRect)
        if startButton.draw(screen):
            gameStatus = "Running"
            startTime = pygame.time.get_ticks()  
        if startButton2.draw(screen):
            gameStatus = 'Running2' 
        screen.blit(startText,startRect)
        screen.blit(startText1,startRect1)
        

    if gameStatus == 'Running':
    # Score
        score = displayScore()
        # Obstacle
        obstacleGroup.draw(screen)
        obstacleGroup.update()

        # Game over
        gameOver = not collisionSprite()
        if gameOver:
            gameStatus = 'Over'


# Game over State
    if gameStatus == 'Over':
        gameOverScore = gameFont.render(f'Score: {score}', False, (64, 64, 64)).convert()
        gameOverSRect = gameOverScore.get_rect(center=(400,150))
        screen.fill((108, 198, 240))
        screen.blit(GameOverText,gameOverRect)
        screen.blit(gameOverScore,gameOverSRect)
        if restartButton.draw(screen):
            gameStatus = 'Running'
            startTime = pygame.time.get_ticks()
        screen.blit(RestartText,RestartRect)

    pygame.display.update()
    clock.tick(60)