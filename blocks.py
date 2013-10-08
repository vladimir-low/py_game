#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = None


class BlockSolid(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('img/blocks/platform.png')


class BlockLight(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('img/blocks/cloud2_32x32.png')


class BlockBorder(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('img/blocks/heart.gif')


class BlockSpikes(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('img/blocks/spikes.png')


class BlockArtefact(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('img/blocks/pirate_trunk.png')
