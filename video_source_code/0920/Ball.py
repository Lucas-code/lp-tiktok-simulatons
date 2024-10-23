

import math
import random

import pygame
from pygame import Vector2

from Utils import utils

font = pygame.font.Font(None, 25)

class Ball:
    def __init__(self,pos,radius,color,month):
        self.color = color
        self.radius = radius
        self.auraPoints = 0
        self.month = month
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

        # Render the text to be displayed above the ball
        text_surface = font.render(f"{self.month}", True, (255, 255, 255))

        # Get the size of the text surface (width and height)
        text_rect = text_surface.get_rect()

        # Calculate the position of the text: centered horizontally and hovering slightly above the ball
        text_x = position[0] - text_rect.width / 2  # Center horizontally
        text_y = position[1] - self.radius - text_rect.height - 5  # Above the ball, with slight offset

        # Blit the text onto the screen at the computed position
        utils.screen.blit(text_surface, (text_x, text_y))

    def getPos(self):
        p = utils.to_Pos(self.circle_body.position)
        return Vector2(p[0],p[1])
