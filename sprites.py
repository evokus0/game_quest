#kangxi

import pygame

from pygame.sprite import Sprite

from settings import *

class Player(Sprite):
    # sprite for player
    # properties of the class
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLACK)
        '''sets image path to correct location joining image folder to file name then converting to a more efficient format'''
        # self.image = pygame.image.load(os.path.join(img_folder, "Tie.png")).convert()
        '''sets transparent color key to black'''
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.screen_rect = screen.get_rect()
        self.vx = 0
        self.vy = 0
        self.cofric = 0.1
        self.canjump = False
    # stuff it can do....
    def friction(self):
        # print("friction...")
        # if self.vx > -0.5 or self.vx < 0.5:
        #     print("velocity is in range...")
        #     self.vx = 0
        if self.vx > 0.5:
            self.vx -= self.cofric
        elif self.vx < -0.5:
            self.vx += self.cofric
        else:
            self.vx = 0
        if self.vy > 0.5:
            self.vy -= self.cofric
        elif self.vy < -0.5:
            self.vy += self.cofric
        else:
            self.vy = 0
    def gravity(self, value):
        self.vy += value
    def update(self):
        # print(self.vx)
        self.friction()
        if self.rect.bottom < HEIGHT:
            self.gravity(GRAVITY)
        self.rect.x += self.vx
        self.rect.y += self.vy
        # if self.rect.right > WIDTH:
        #     self.rect.x = -50
        #     print("running off screen")
        # if self.rect.top > 500:
        #     self.vy = -5
        # if self.rect.top < 100:
        #     self.vy = 5
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.vy -= 5
        if keystate[pygame.K_a]:
            self.vx -= 5
        if keystate[pygame.K_s]:
            self.vy += 5
        if keystate[pygame.K_d]:
            self.vx += 5
        if keystate[pygame.K_SPACE]:
            self.jump()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            # print("touched the right side...")
        if self.rect.left < 0:
            self.rect.left = 0
            # print("touched the left side...")
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.canjump = True
            # print("touched the bottom")
        if self.rect.top < 0:
            self.rect.top = 0
            # print("touched the top")
    def jump(self):
        if self.canjump == True:
            self.canjump = False
            self.vy -= 50
            print(self.vy)


class Enemy(Sprite):
    # sprite for player
    # properties of the class
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        '''sets image path to correct location joining image folder to file name then converting to a more efficient format'''
        # self.image = pygame.image.load(os.path.join(img_folder, "Tie.png")).convert()
        '''sets transparent color key to black'''
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.screen_rect = screen.get_rect()
        self.vx = 5
        self.vy = 5
        self.cofric = 0.5
    # stuff it can do....
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right > WIDTH:
            self.vx*=-1
            self.rect.y += 10
            self.rect.x = WIDTH - 50
        if self.rect.left < 0:
            self.vx*=-1
            self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def jump(self):
        print("I jumped...")