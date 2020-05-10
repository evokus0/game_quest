# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement
# © 2019 KidsCanCode LLC / All rights reserved.

import pygame as pg
from pygame.sprite import Group
import random
from settings import *
from sprites import *
from os import path

# Health bar display, basic version
def draw_player_health(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Health bar, but for ammo
def draw_player_ammo(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# this is the game class, we create a new game at the bottom of the code...
class Game:

    def __init__(self):
        # initialize framework
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # loading assets
        self.dir = path.dirname(__file__)
        # load high score
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = Group()
        self.platforms = Group()
        self.mobT1_group = Group()
        self.mobT2_group = Group()
        self.tempGroup = Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground = Platform(self, 0, HEIGHT-40, WIDTH, 40, GREEN)
        # mobT2_1 = MobT2(WIDTH/2, HEIGHT-95, 20, 55)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        # self.all_sprites.add(mobT2_1)
        # self.mobT2_group.add(mobT2_1)

        # you need to add new instances of the platform class to groups or it wont update or draw
        # generates platforms that don't touch each other...
        # comes from ccozort's game "Leapin' Wizards"
        for plat in range(0, 6):
            if len(self.platforms) < 2:
                plat = Platform(self, random.randint(0,WIDTH-100), random.randint(0,HEIGHT-100), 100, 15, GREEN)
                self.platforms.add(plat)
                self.all_sprites.add(plat)
                plat.spawn()

            while True:
                newPlat = Platform(self, random.randint(0,WIDTH-100), random.randint(0,HEIGHT-100), 100, 15, GREEN)
                self.tempGroup.add(newPlat)
                selfCollide = pg.sprite.groupcollide(self.tempGroup, self.platforms, True, False)
                allCollide = pg.sprite.groupcollide(self.tempGroup, self.all_sprites, True, False)
                if not selfCollide and not allCollide:
                    self.platforms.add(newPlat)
                    self.all_sprites.add(newPlat)
                    self.tempGroup.remove(newPlat)
                    # print(len(self.tempGroup))
                    break

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # Update - listen to see if anything changes...
        self.all_sprites.update()
 
        # scrolling mechanic, activate at 1/4 of the screen
        if self.player.pos.x >= WIDTH * 1/4:
            self.player.pos.x -= int(abs(self.player.vel.x))
            for plat in self.platforms:
                plat.rect.x -= int(abs(self.player.vel.x))
                if plat.rect.right < 0:
                    plat.kill()
                    self.score += 1

        # Chris Bradfield platform gen system, modified for horizontal
        while len(self.platforms) < 7:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(WIDTH + 30, WIDTH + 75), 
                         random.randrange(0, WIDTH - width),
                         width, 20, CYAN)
            self.platforms.add(p)
            self.all_sprites.add(p)


        while len(self.platforms) < 7:
            self.platGen()     

        if self.player.rect.bottom > HEIGHT:
            self.playing = False

        # if self.player.rect.bottom > HEIGHT:
        #     for sprite in self.all_sprites:
        #         sprite.rect.y -= max(self.player.vel.y, 10)
        #         if sprite.rect.bottom < 0:
        #             sprite.kill()
        #     if len(self.platforms) == 0:
        #         self.playing = False

        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.vel.y = 0
            self.player.pos.y = hits[0].rect.top+1
            # if self.player.rect.top > hits[0].rect.top:
            #     self.player.vel.y = 15
            #     self.player.rect.top = hits[0].rect.bottom + 5
            # else:
            #     self.player.vel.y = 0
            #     self.player.pos.y = hits[0].rect.top+1

        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        # mobT2_hits = pg.sprite.spritecollide(self.player, self.mobT2_group, False)
        if hits:
            if self.player.rect.top > hits[0].rect.top:
                self.player.vel.y = 15
                self.player.rect.top = hits[0].rect.bottom + 5
                # self.player.hitpoints -= 5
            else:
                self.player.vel.y = 0
                self.player.pos.y = hits[0].rect.top+1

        # if mobT2_hits:
            # self.player.hitpoints -= 0.5
            # # print("hitpoints are now " + str(self.player.hitpoints))

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draw_player_health(self.screen, 10, 10, self.player.hitpoints/100)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        draw_player_health(self.screen, 10, 10, self.player.hitpoints)
        draw_player_ammo(self.screen, WIDTH-110, 10, self.player.ammo)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("YOU DIED!", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Your Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 8)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Current High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT * 5 / 8)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    #     # Health bar display, basic version
    # def draw_player_health(surf, x, y, w):
    #     outline_rect = pg.Rect(x, y, 100, 20)
    #     fill_rect = pg.Rect(x, y, w, 20)
    #     pg.draw.rect(surf, RED, fill_rect)
    #     pg.draw.rect(surf, WHITE, outline_rect, 2)

    #     # Health bar, but for ammo
    # def draw_player_ammo(surf, x, y, w):
    #     outline_rect = pg.Rect(x, y, 100, 20)
    #     fill_rect = pg.Rect(x, y, w, 20)
    #     pg.draw.rect(surf, RED, fill_rect)
    #     pg.draw.rect(surf, WHITE, outline_rect, 2)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()