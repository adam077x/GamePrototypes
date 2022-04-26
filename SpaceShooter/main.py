import pygame
import sys
import random

SPACESHIP_IMAGE = pygame.image.load("spaceship.png")

class ScoreCounter():
    def __init__(self):
        self.score = 0

    def inc(self):
        self.score += 1

    def getScore(self):
        return self.score

scoreCounter = ScoreCounter()

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.transform.rotate(SPACESHIP_IMAGE, 180)
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))

    def update(self, dt):
        self.y += dt / 2

        for bullet in bullets:
            if pygame.Rect(self.x, self.y, 64, 64).colliderect(bullet.rect):
                scoreCounter.inc()
                print(scoreCounter.getScore())
                pygame.display.set_caption("SCORE: " + str(scoreCounter.getScore()))
                bullets.remove(bullet)
                enemies.remove(self)
        
        if self.y > 480:
            enemies.remove(self)

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

enemies = []
bullets = []
stars = []

class Star:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = random.randint(1, 3)

    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

    def update(self, dt):
        self.y += (dt * self.radius) / 5

        if self.y > 480:
            stars.remove(self)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 16, 16)

    def update(self, dt):
        self.rect.update(self.x, self.y, 16, 16)
        self.y -= dt

        if self.y < 0:
            bullets.remove(self)

    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 4)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.sprite = pygame.transform.scale(SPACESHIP_IMAGE, (64, 64))

    def update(self, dt):
        self.x += self.velX * dt
        self.y += self.velY * dt

        for enemy in enemies:
            if pygame.Rect(enemy.x, enemy.y, 64, 64).colliderect(pygame.Rect(self.x, self.y, 64, 64)):
                scoreCounter.score = 0
                pygame.display.set_caption("SCORE: " + str(scoreCounter.getScore()))
                self.x = 640/2
                bullets.clear()
                enemies.clear()

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def keydown(self, event):
        if event.key == pygame.K_a:
            self.velX = -1
        elif event.key == pygame.K_d:
            self.velX = 1
        
        if event.key == pygame.K_w:
            self.velY = -1
        elif event.key == pygame.K_s:
            self.velY = 1

        if event.key == pygame.K_SPACE:
            bullets.append(Bullet(self.x+32, self.y))
    
    def keyup(self, event):
        if event.key == pygame.K_a:
            self.velX = 0
        elif event.key == pygame.K_d:
            self.velX = 0
        
        if event.key == pygame.K_w:
            self.velY = 0
        elif event.key == pygame.K_s:
            self.velY = 0

pygame.init()

player = Player(320, 350)

(width, height) = (640, 480)

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

t = 1000
t2 = 100

pygame.display.set_caption(f"SCORE: {0}".format(scoreCounter.score))

running = True
while running:
    dt = clock.tick()

    t -= dt
    if t < 0:
        t = 1000
        enemies.append(Enemy(random.randint(0, 640), -100))

    t2 -= dt
    if t2 < 0:
        t2 = 50
        stars.append(Star(random.randint(0, 640), 0, random.randint(1, 8)))
    
    screen.fill((0, 0, 0))

    player.update(dt)
    player.render(screen)

    for star in stars:
        star.update(dt)
        star.render(screen)

    for enemy in enemies:
        enemy.update(dt)
        enemy.render(screen)

    for bullet in bullets:
        bullet.update(dt)
        bullet.render(screen)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            player.keydown(event)
        elif event.type == pygame.KEYUP:
            player.keyup(event)
