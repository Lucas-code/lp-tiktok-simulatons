from Box2D import b2Body

import math

import pygame
from pygame import Vector2

from Utils import utils

font = pygame.font.Font(None, 20)

class Ball:
    def __init__(self,pos,radius,color,timeLeft):
        self.color = (255,255,255)
        self.radius = radius
        self.circle_body : b2Body = utils.world.CreateDynamicBody(position=(utils.from_Pos((pos.x, pos.y))))
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.userData = self
        self.timeLeft = timeLeft
        self.active = True
        self.createdTime = pygame.time.get_ticks()
    
    def draw(self):
        if self.active:
            secondsPassed = (pygame.time.get_ticks() - self.createdTime) / 1000
            timeLeft = math.ceil(int(max(0, self.timeLeft - secondsPassed)))
            # print(timeLeft)
            if timeLeft <= 0:
                self.deactivateBall()
            else:
                text_surface = font.render(f"{timeLeft:01}", True, (255, 255, 255))
                pos = utils.to_Pos(self.circle_body.position)
                pos = (pos[0]-4,pos[1] - (self.radius * utils.PPM ) - 13)
                # pos[0] -= 10
                # pos[1] -= 15
                utils.screen.blit(text_surface, pos)

        for fixture in self.circle_body.fixtures:
            self.draw_circle(fixture.shape, self.circle_body, fixture)

    def draw_circle(self,circle, body, fixture):
        position = utils.to_Pos(body.transform * circle.pos)
        pygame.draw.circle(utils.screen, self.color, [int(x) for x in position], int(circle.radius * utils.PPM))
        pygame.draw.circle(utils.screen, (0,0,0), [int(x) for x in position], int(circle.radius * utils.PPM - 2),4)

    def deactivateBall(self):
        self.active = False
        position = self.circle_body.position
        utils.world.DestroyBody(self.circle_body)
        self.circle_body = utils.world.CreateStaticBody(position=position)
        self.circle_shape = self.circle_body.CreateCircleFixture(radius=self.radius, density=1, friction=0.0, restitution=1.0)
        self.circle_body.userData = self
    
    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])
