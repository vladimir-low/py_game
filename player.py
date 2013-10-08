#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pyganim

WIDTH = 22
HEIGHT = 32
COLOR = '#888889'
SPEED = 5
JUMP_STRENGTH = 10
GRAVITY = 0.45

ANIMATION_DELAY = 0.1
ANIMATION_RIGHT = [
                    'img/mario/r1.png',
                    'img/mario/r2.png',
                    'img/mario/r3.png',
                    'img/mario/r4.png',
                    'img/mario/r5.png'
                ]
ANIMATION_LEFT = [
                    'img/mario/l1.png',
                    'img/mario/l2.png',
                    'img/mario/l3.png',
                    'img/mario/l4.png',
                    'img/mario/l5.png'
                ]
ANIMATION_JUMP_LEFT = [('img/mario/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('img/mario/jr.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('img/mario/j.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('img/mario/0.png', ANIMATION_DELAY)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.xvel = 0  # Velocity. 0 - not move
        self.yvel = 0
        self.onGround = False  # Whether a hero on the ground
        self.died = False  # Died or alive
        self.win = False  # Win the game
        self.startX = x  # Initial position
        self.startY = y
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))  # Transparent background

        # Animation
        self.boltAnimRight = pyganim.PygAnimation([(x, ANIMATION_DELAY) for x in ANIMATION_RIGHT])
        self.boltAnimRight.play()

        self.boltAnimLeft = pyganim.PygAnimation([(x, ANIMATION_DELAY) for x in ANIMATION_LEFT])
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # Stay by default

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.yvel = -JUMP_STRENGTH
            self.image.fill(pygame.Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -SPEED  # Move left on x-n
            self.image.fill(pygame.Color(COLOR))
            if up:  # Animation for left jump
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = SPEED  # Move right on x+n
            self.image.fill(pygame.Color(COLOR))
            if up:  # Animation for right jump
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0  # Else - hold on.
            if not up:
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # We don't know whether a player on the ground
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if self.died:
            return 'died'
        elif self.win:
            return 'win'

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # If a hero overlaps with block
                # Regular blocks
                if xvel > 0:  # If move right
                    self.rect.right = p.rect.left  # Stop movement
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:  # if move down
                    self.rect.bottom = p.rect.top
                    self.onGround = True  # Stand on the ground
                    self.yvel = 0  # Stop gravitation
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

                # Enemies
                from blocks import BlockSpikes
                if yvel > 0 and isinstance(p, BlockSpikes):
                    self.died = True

                # Artefacts
                from blocks import BlockArtefact
                if yvel > 0 and isinstance(p, BlockArtefact):
                    self.win = True
