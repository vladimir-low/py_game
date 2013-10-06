#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blocks/cloud2_32x32.png')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blocks/heart.gif')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blocks/spikes.jpg')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
