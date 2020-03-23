# This file was created by: Chris Cozort
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: 

'''
Lore for last week:
Functions, methods, Classes, scope('global' vs local)
For loops, break, pass, % modulu, 
string and list traversal

Lore for this week:
GitHub, Modularity, import as
'''

# import libs
import pygame
import random
import os
from pygame.sprite import Sprite

from settings import *
from sprites import *

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

def get_mouse_now():
    x,y = pygame.mouse.get_pos()
    return (x,y)

# classes for game



# init pygame and create window
pygame.init()
# init sound mixer
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game...")
clock = pygame.time.Clock() 

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
# testSprite = Sprite()
# testSprite.image = pygame.Surface((50,50))
# testSprite.image.fill(GREEN)
# testSprite.rect = testSprite.image.get_rect()
# testSprite.rect.center = (WIDTH / 2, HEIGHT / 2)
all_sprites.add(player)
# all_sprites.add(testSprite)

for i in range(0,100):
    print(i)
    i = Enemy()
    i.rect[0] = random.randint(0,WIDTH-25)
    i.rect[1] = random.randint(0,HEIGHT)
    enemies.add(i)
    all_sprites.add(i)

# game loop


while RUNNING:
    #  keep loop running at the right speed
    clock.tick(FPS)
    ### process input events section of game loop
    for event in pygame.event.get():
        # check for window closing
        if event.type == pygame.QUIT:
            RUNNING = False
            # break
    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)
    all_sprites.update()

    blocks_hit_list = pygame.sprite.spritecollide(player, enemies, True)
    for block in blocks_hit_list:
        print(enemies)
    ### draw and render section of game loop
    screen.fill(REDDISH)
    all_sprites.draw(screen)
    # double buffering draws frames for entire screen
    pygame.display.flip()
    # pygame.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pygame.quit()