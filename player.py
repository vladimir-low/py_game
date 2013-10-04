#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pyganim

WIDTH = 22
HEIGHT = 32
COLOR = '#888889'
SPEED = 7
JUMP_STRENGTH = 10
GRAVITY = 0.35

ANIMATION_DELAY = 0.1
ANIMATION_RIGHT = [
                    'mario/r1.png',
                    'mario/r2.png',
                    'mario/r3.png',
                    'mario/r4.png',
                    'mario/r5.png'
                ]
ANIMATION_LEFT = [
                    'mario/l1.png',
                    'mario/l2.png',
                    'mario/l3.png',
                    'mario/l4.png',
                    'mario/l5.png'
                ]
ANIMATION_JUMP_LEFT = [('mario/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('mario/jr.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('mario/j.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('mario/0.png', ANIMATION_DELAY)]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.xvel = 0  # Velocity. 0 - not move
        self.yvel = 0
        self.onGround = False  # Whether a hero on the ground
        self.startX = x  # Initial position
        self.startY = y
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))  # Transparent background

        # Animation
        boltAnim = []
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

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # If a hero overlaps with block
                if self.xvel > 0:  # If move right
                    print "Move right:"
                    print xvel, yvel
                    print self.rect.x, self.rect.y
                    self.rect.right = p.rect.left  # Stop movement

                if self.xvel < 0:
                    print "Move left:"
                    print xvel, yvel
                    print self.rect.x, self.rect.y
                    self.rect.left = p.rect.right

                if self.yvel > 0:  # if move down
                    print "Move down:"
                    print xvel, yvel
                    print self.rect.x, self.rect.y
                    self.rect.bottom = p.rect.top
                    self.onGround = True  # Stand on the ground
                    self.yvel = 0  # Stop gravitation

                if self.yvel < 0:
                    print "Move up:"
                    print xvel, yvel
                    print self.rect.x, self.rect.y
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
