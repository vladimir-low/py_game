#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('blocks/platform.png')
        #self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        #self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
