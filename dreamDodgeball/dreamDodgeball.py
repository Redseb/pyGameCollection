import pygame
import random
import os

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

class Biedronka():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 20
        self.rectShape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = random.randint(-10,10) / 100 #random vertical velocity
        self.vy = random.randint(-10,10) / 100 #random horizontal velocity
        self.sprite = pygame.image.load(os.path.join('./images/enemy.png'))

        # self.shape = pygame.Circle(self.x, self.y, self.width, self.height)

    def draw(self):
        #populate with sprite
        screen.blit(self.sprite, (self.x, self.y))
    def move(self):
        self.x = self.x + self.vx
        self.y  = self.y + self.vy
        self.rectShape = pygame.Rect(self.x, self.y, self.width, self.height)

    def collision(self, player):
        if self.rectShape.colliderect(player):
            return True
        else:
            return False

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = self.width
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = 0
        self.vy = 0
        self.sprite = pygame.image.load(os.path.join('./images/player.png'))
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
    def move(self, vx, vy):
        self.x = self.x + vx
        self.y = self.y + vy
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

#setting up game
biedronki = []
for i in range(20):
    biedronki.append(Biedronka(300, 300))

player = Player(300, 550)

gameState = "menu"
inGameBackground = pygame.image.load(os.path.join('./images/background.png'))
points = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.vy = -0.3
            elif event.key == pygame.K_DOWN:
                player.vy = 0.3
            elif event.key == pygame.K_RIGHT:
                player.vx = 0.3
            elif event.key == pygame.K_LEFT:
                player.vx = -0.3
            elif event.key == pygame.K_SPACE and gameState != "ingame":
                gameState = "ingame"
                points = 0
                biedronki = []
                for i in range(20):
                    biedronki.append(Biedronka(300, 300))

                player = Player(300, 550)
            else:
                player.vx = 0
                player.vy = 0
        else:
            player.vx = 0
            player.vy = 0
    screen.blit(inGameBackground, (0,0))

    if gameState == "menu":
        logo = pygame.image.load(os.path.join('./images/title1.png'))
        screen.blit(logo, (0,0))
    elif gameState == "ingame":
        points += 1
        for biedronka in biedronki:
            biedronka.move()
            biedronka.draw()
            if biedronka.collision(player.shape):
                gameState = "end"
        for biedronka in biedronki:
            if biedronka.x < 0 or biedronka.x + biedronka.width > width:
                biedronka.vx = -biedronka.vx
            if biedronka.y < 0 or biedronka.y + biedronka.height > height:
                biedronka.vy = - biedronka.vy
        if player.x < 0:
            player.x = 0
        elif player.x + player.width > width:
            player.x = width - player.width
        if player.y < 0:
            player.y = 0
        if player.y + player.height > height:
            player.y = height - player.height
        
        player.draw()
        player.move(player.vx, player.vy)
    elif gameState == "end":
        gameOver = pygame.image.load(os.path.join('./images/failure.png'))
        screen.blit(gameOver, (0,0))
        write("Points: " + str(points), 0, 100, 30)
    pygame.display.update()


