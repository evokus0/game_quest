
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.
# mr cozort planted a landmine by importing Sprite directly...
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
from random import randint
vec = pg.math.Vector2

class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(10, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100
        self.ammo = 100
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits: 
            self.vel.y = -15
    def update(self):
        self.acc = vec(0, 0.5)
        if self.vel.x <= 0.1 and self.vel.x >= -0.1:
            self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        # if keys[pg.K_w]:
            # self.acc.y = -PLAYER_ACC
        # if keys[pg.K_s]:
            # self.acc.y = PLAYER_ACC
        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_w]:
            self.jump()
        if keys[pg.K_UP]:
            self.jump()
        if keys[pg.K_z]:
            self.jump()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # # wrap around the sides of the screen [disabled]
        # if self.pos.x > WIDTH:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = WIDTH
        # if self.pos.y < 0:
        #     self.pos.y = HEIGHT
        # if self.pos.y > HEIGHT:
        #     self.pos.y = 0

        self.rect.midbottom = self.pos
class Platform(Sprite):
    def __init__(self, game, x, y, w, h, color):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        # self.image = self.game.spritesheet.get_image(0,256,128,16, 1, 1)
        # self.image.set_colorkey(BLACK)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn()
    def spawn(self):
        pass
    #     self.mobT1 = MobT1(self.game)
    #     self.mobT1.rect.midbottom = self.rect.midtop
    #     self.game.mobT1_group.add(self.mobT1)
    #     self.game.all_sprites.add(self.mobT1)
    # def update(self):
        # self.mobT1.rect.midbottom = self.rect.midtop
class MobT1(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(MAGENTA)
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.rect = self.image.get_rect()
        self.hitpoints = 100

class MobT2(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = -1
    # def blitme(self, x, y):
        # self.screen.blit(self.image, (x, y))
    def update(self):
        self.rect.x += self.vx
        if self.rect.x < 0:
            self.kill()
            # self.rect.x = WIDTH
            self.rect.height = random.randint(20,40)
# created a healthbar and tied it to players hitpoints
# I added it to the main.py under new, and it won't change its width
# I think I need to add a blit to update the graphic
