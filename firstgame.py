#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.locals import *
from player import *
from blocks import *

WIN_WIDTH = 800
WIN_HEIGHT = 600
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BG_COLOR = "#004400"

LEVEL = [
        '-------------------------------------',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '- ---                               -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-       -------                     -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-                      --           -',
        '-   -                               -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-         ----                      -',
        '-                                   -',
        '-                                   -',
        '-                 -            -    -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '-   -----                 ----      -',
        '-                                   -',
        '-                                   -',
        '-                                   -',
        '--------------------------------------']


class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def _apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()  # The CLock object

    screen = pygame.display.set_mode(DISPLAY)  # Creates the window
    pygame.display.set_caption('My First Game')

    bg = pygame.Surface(DISPLAY)  # Creates a visible surface
    bg.fill(Color(BG_COLOR))

    # Create a player
    hero = Player(40, 40)
    up = left = right = False

    # Groupping sprites
    entities = pygame.sprite.Group()
    entities.add(hero)
    platforms = []  # Store platforms to match intersections

    # Build level
    x = y = 0  # coordinates
    for row in LEVEL:
        for col in row:
            if col == '-':
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH  # Sets width of the blocks
        y += PLATFORM_HEIGHT  # Sets height
        x = 0  # Each line from the beginning

    total_level_width  = len(LEVEL[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(LEVEL)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    # THE MAIN LOOP
    while True:
        fpsClock.tick(50)

        # Events handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Verify movements keys
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_UP:
                up = False

        # Draws background (left top coordinates)
        screen.blit(bg, (0, 0))

        # Center camera according hero position
        camera.update(hero)

        # Move  a hero
        hero.update(left, right, up, platforms)

        # Draw sprites
        #entities.draw(screen)
        for e in entities:
            screen.blit(e.image, camera._apply(e))

        pygame.display.update()  # The window actually draws only here.




if __name__ == "__main__":
    main()
