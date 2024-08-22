

import math
import random

import pygame
from pygame import Vector2

from Utils import utils


class Ball:
    def __init__(self,pos,radius,color):
        self.color = color
        self.radius = radius
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.userData = self

        self.previousPositions = []
        self.storePosInterval = 3

    def draw(self):
        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)
        self.storePosInterval -= 1

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))
        pygame.draw.circle(utils.screen, (255,255,255), [int(x) for x in position], int(circle.radius * utils.PPM),4)

        for pos in self.previousPositions:
            pygame.draw.circle(utils.screen, self.color, [int(x) for x in pos], int(circle.radius * utils.PPM))
            pygame.draw.circle(utils.screen, (255,255,255), [int(x) for x in pos], int(circle.radius * utils.PPM),2)

        if self.storePosInterval <= 0:
            self.previousPositions.append(position)
            if len(self.previousPositions) > 10:
                self.previousPositions.pop(0)
            self.storePosInterval = 5

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])
