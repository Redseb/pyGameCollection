import pygame
import os
import random

pygame.init()

#Create game window
height = 600
width = 600
screen = pygame.display.set_mode((width,height))

def write(text, x, y, size):
    textFont = pygame.font.SysFont("Arial", size)
    rend = textFont.render(text, 1, (255, 100, 100))
    x = (width - rend.get_rect().width) / 2
    y = (height - rend.get_rect().height) / 2
    screen.blit(rend, (x, y))

class Obstacle():
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y_top = 0
        self.height_top = random.randint(150,250)
        self.middle = 200 #space inbetween top and bottom obstacle
        self.y_bottom = self.height_top + self.middle
        self.height_bottom = height - self.y_bottom
        # self.color = (48,98,48) #Gameboy darkest color
        self.color = (28, 78, 28)
        self.sprite_top = pygame.image.load(os.path.join('./images/caveTop.png'))
        self.sprite_bottom = pygame.image.load(os.path.join('./images/caveBottom.png'))
        self.shape_top = pygame.Rect(self.x, self.y_top, self.width, self.height_top)
        self.shape_bottom = pygame.Rect(self.x, self.y_bottom, self.width, self.height_bottom)


    def draw(self):
        # pygame.draw.rect(screen, self.color, self.shape_top, 0)
        screen.blit(self.sprite_top, (self.x, self.y_top), (0, 0, self.width, self.height_top))
        screen.blit(self.sprite_bottom, (self.x, self.y_bottom))
        # pygame.draw.rect(screen, self.color, self.shape_bottom, 0)

    def move(self, v):
        self.x = self.x - v
        self.shape_top = pygame.Rect(self.x, self.y_top, self.width, self.height_top)
        self.shape_bottom = pygame.Rect(self.x, self.y_bottom, self.width, self.height_bottom)
    def collision(self, player):
        if self.shape_top.colliderect(player) or self.shape_bottom.colliderect(player):
            return True
        else:
            return False

class Plane():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 50
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = pygame.image.load(os.path.join('./images/plane.png'))
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
    def move(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)        

obstacles = []
for i in range(21):
    obstacles.append(Obstacle(i * width/20, width/20))
player = Plane(250, 275)
dy = 0


gameState = "menu"
caveSpeed = 0.25
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -0.20
            elif event.key == pygame.K_DOWN:
                dy = 0.20
            elif event.key == pygame.K_SPACE:
                if gameState != "ingame":
                    player = Plane(250, 275)
                    dy = 0
                    points = 0
                    gameState = "ingame"
    screen.fill((139, 172, 15)) #Clear screen
    if gameState == "menu":
        logo = pygame.image.load(os.path.join('./images/logo.png'))
        screen.blit(logo, (0,0))
    elif gameState == "ingame":
        for obstacle in obstacles:
            obstacle.move(caveSpeed)
            obstacle.draw()
            if obstacle.collision(player.shape):
                gameState = "end"
        for obstacle in obstacles:
            if obstacle.x <=-obstacle.width:
                obstacles.remove(obstacle)
                obstacles.append((Obstacle(width,width/20)))
                if dy != 0: #Only increase points when the player is moving up or down
                    points = points + 10
                if points < 1000:
                    caveSpeed = 0.25
                elif points < 2000:
                    caveSpeed = 0.30
                elif points < 4000:
                    caveSpeed = 0.40
                elif points < 6000:
                    caveSpeed = 0.60
        player.draw()
        player.move(dy)
    elif gameState == "end":
        gameOver = pygame.image.load(os.path.join('./images/gameOver.png'))
        screen.blit(gameOver, (0,0))
    pygame.display.update()