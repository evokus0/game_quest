# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game)
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

# Followed Bradfield's tutorials for the start and GO screens, drawing text, saving scores.
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
        # Note - Bradfield's code doesh't work, looked in the comments and people said to use 'r+' instead of 'w' since 'w' is write only and not read.
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
        self.static_platforms = Group()
        self.mobT1_group = Group()
        self.mobT2_group = Group()
        self.tempGroup = Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground = Platform(self, WIDTH/2, HEIGHT-40, WIDTH, 40, GREEN)
        # ground.rect.x = WIDTH / 2
        # ground.rect.y = HEIGHT - 50
        # ground2 = Platform(self, WIDTH - 25, HEIGHT-40, WIDTH - 25, 40, GREEN)

        self.all_sprites.add(ground)
        self.static_platforms.add(ground)

        # REMEMBER THAT GROUND IS NOT IN PLATFORM GROUP!

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
        # Right now the player still seems to move forward.
        if self.player.pos.x >= WIDTH / 4:
            self.player.pos.x = WIDTH / 4
            # set player location based on velocity
            self.player.pos.x += self.player.vel.x
            # scroll plats with player
            for plat in self.platforms:
                # creates slight scroll based on player y velocity
                plat.vel.x = -self.player.vel.x
                if plat.rect.right < 0:
                    plat.kill()

        while len(self.mobT1_group) < 7:
            mob = MobT1(self, random.randrange(WIDTH * 3/4, WIDTH + 200), HEIGHT - 100, 20, 40)
            self.mobT1_group.add(mob)
            self.all_sprites.add(mob)

        # Kill trigger for passing below thee screen
        if self.player.rect.bottom > HEIGHT:
            self.playing = False

        # Hit detection for regular platforms
        phits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if phits:
            if self.player.rect.top > phits[0].rect.top:
                self.player.vel.y = 10
                self.player.rect.top = phits[0].rect.bottom + 5
                # self.player.hitpoints -= 5
                # print("hitpoints are now " + str(self.player.hitpoints))
                # print(self.player.hitpoints)
            # print("it collided")
            else:
                self.player.vel.y = 0
                self.player.pos.y = phits[0].rect.top+1
        
        # Hit detection for ground / static platforms
        ghits = pg.sprite.spritecollide(self.player, self.static_platforms, False)
        if ghits:
            self.player.vel.y = 0
            self.player.pos.y = ghits[0].rect.top+1


        # # if mobT2_hits:
        #     # self.player.hitpoints -= 0.5
        #     # # print("hitpoints are now " + str(self.player.hitpoints))


        # CAN"T GET THESE TO WORK ! always some idiosyncracy with them... Just going to spawn mobs on flat ground.

        # # Chris Bradfield platform gen system, modified for horizontal
        # while len(self.platforms) < 7:
        #     width = random.randrange(50, 100)
        #     p = Platform(self, random.randint(400, WIDTH+100), HEIGHT-40, width, 40, BLUE)
        #     self.platforms.add(p)
        #     self.all_sprites.add(p)

        # # Plat generator, comes from ccozort's game "Leapin' Wizards"
  
        #     # while len(self.platforms) < 7:
        #     #     width = random.randrange(150, 200)
        #     #     newPlat = Platform(self, random.randint(WIDTH-100, WIDTH+100), HEIGHT-40, width, 40, BLUE)
        #     #     self.tempGroup.add(newPlat)
        #     #     selfCollide = pg.sprite.groupcollide(self.tempGroup, self.platforms, True, False)
        #     #     allCollide = pg.sprite.groupcollide(self.tempGroup, self.all_sprites, True, False)
        #     #     if not selfCollide and not allCollide:
        #     #         self.platforms.add(newPlat)
        #     #         self.all_sprites.add(newPlat)
        #     #         self.tempGroup.remove(newPlat)
        #     #         # print(len(self.tempGroup))
            #         break


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