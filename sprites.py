
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.
# mr cozort planted a landmine by importing Sprite directly...
import pygame as pg
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2

from threading import *

class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hp = 100
    
    # doesn't work yet
    def pew(self):
        laser = PewPew(self.game, self.pos.x, self.pos.y, 10, 10)
        self.game.all_sprites.add(laser)
        self.platforms.add(laser)
        self.projectiles.add(laser)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits: 
            self.vel.y = -1*PLAYER_JUMP_STRENGTH

    def update(self):
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_w]:
            self.jump()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        # if self.pos.y < 0:
        #     self.pos.y = HEIGHT
        # if self.pos.y > HEIGHT:
        #     self.pos.y = 0

        self.rect.midbottom = self.pos

class Platform(Sprite):
    def __init__(self, color, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.vx = 5
    # def update(self):
    #     self.rect.x += self.vx
    #     if self.rect.x + self.rect.width > WIDTH or self.rect.x < 0:
    #         self.vx * -1

class Item(Sprite):
    # trying to include items that provide abilities
    def __init__(self, color, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
  
    # def x(self):
    #     pass

#doesn't work yet
class PewPew(Sprite):
    def __init__(self, game, color, x, y, w, h):
        Sprite.__init(self)
        self.game = game
        self.image = pg.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = xself.rect.y = y
    def update(self):
        # if self.game.player.vel.x > 0:
        # self.rect.y -= 1
        self.t = Timer(2.0, self.melt())
        self.t.start
        
    def melt(self):
        self.kill()

class Health_Bar(Sprite):
    def __init__(self, game, color, x, y, w, h):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.width = self.game.player.hp
        # self.game.screen.blit(self.image, (self.image(self.game.player.hp, 0)))