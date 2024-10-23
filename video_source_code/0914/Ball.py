

import math
import random

import pygame
from pygame import Vector2

from Utils import utils


class Ball:
    def __init__(self,pos,radius,color):
        self.color = color
        self.radius = radius
        self.score = 7
        self.circle_body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.userData = self

    def draw(self):
        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))
        pygame.draw.circle(utils.screen, (255,255,255), [int(x) for x in position], int(circle.radius * utils.PPM),4)

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])
    
    def respawn(self):
        newPos = Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30))
        self.circle_body.position = utils.from_Pos((newPos.x, newPos.y))
        self.circle_body.linearVelocity = (0, 0)
        self.circle_body.angularVelocity = 0
