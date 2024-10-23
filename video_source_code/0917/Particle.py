import pygame
from pygame import Vector2

import random
from Utils import utils

class Particle:
    def __init__(self, pos, velocity, color, lifetime):
        self.pos = Vector2(pos)
        self.velocity = Vector2(velocity)
        self.color = color
        self.lifetime = lifetime

    def update(self):
        self.pos += self.velocity
        self.lifetime -= 1

    def draw(self):
        if self.lifetime > 0:
            pygame.draw.circle(utils.screen, self.color, self.pos, 2)
