
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.



import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
import time
from random import randint
vec = pg.math.Vector2

class Player(Sprite):
    # 'game' perameter so it can see all things happening in the game
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
        phits = pg.sprite.spritecollide(self, self.game.platforms, False)
        ghits = pg.sprite.spritecollide(self, self.game.static_platforms, False)
        self.rect.x -= 1
        if phits or ghits: 
            self.vel.y = -15
    def update(self):
        self.acc = vec(0, 0.5)
        if self.vel.x <= 0.1 and self.vel.x >= -0.1:
            self.vel.x = 0
        keys = pg.key.get_pressed()
        # if keys[pg.K_LEFT]:
        #     self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()
        # if keys[pg.K_w]:
        #     self.jump()
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

        self.rect.midbottom = self.pos

    # Now with player shooting mechanic, from Bradfield's "Shmup", modified for horizontal.
    def shoot(self, game):
        if self.ammo > 10:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            game.all_sprites.add(bullet)    
            game.bullets.add(bullet)
            self.ammo -= 10
            if self.ammo <= 0:
                self.ammo = 0

class Bullet(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 10))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # kill if leaves the screen
        if self.rect.centerx > WIDTH:
            self.kill()

class EvilBullet(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 10))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = -10

    def update(self):
        self.rect.x += self.speedx
        # kill if leaves the screen
        if self.rect.centerx < 0:
            self.kill()

class Platform(Sprite):
    def __init__(self, game, x, y, w, h, color):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        # self.image = self.game.spritesheet.get_image(0,256,128,16, 1, 1)
        # self.image.set_colorkey(BLACK)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos






class RunnerMob(Sprite):
    # 2 kinds of mobs, this kind can move but not shoot.
    def __init__(self, game):
        Sprite.__init__(self)
        x = random.randrange(WIDTH, WIDTH + 100)
        y = HEIGHT - 125
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        # self.vx = random.randrange(-4, -1)
        self.vx = random.randrange(-3, 3)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.y = y
        # self.vy = 0

    def update(self):
        self.acc = vec(0, 0.5)
        self.rect.x += self.vx
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.rect.left < 0:
            self.kill()

class ShooterMob(Sprite):
    # Another mob type, this one can shoot but not move.
    def __init__(self, game):
        Sprite.__init__(self)
        x = random.randrange(WIDTH, WIDTH + 100)
        y = HEIGHT - 125
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.vx = 0
        self.pos = vec(x, y)
        self.rect.y = y
        self.bullet_shoot_timer = 0

    def update(self):
        now = pg.time.get_ticks()
        if now - self.bullet_shoot_timer > BULLET_SHOOT_FREQ:
            self.bullet_shoot_timer = now
            self.shoot(self.game)

        if self.rect.left < 0:
            self.kill()
    
    def shoot(self, game):
        bullet = EvilBullet(self.rect.centerx, self.rect.centery)
        game.all_sprites.add(bullet)    
        game.evil_bullets.add(bullet)