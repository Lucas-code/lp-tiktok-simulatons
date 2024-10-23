import pygame
import random
from pygame import Vector2
from time import sleep
from Ball import Ball
from Polygon import Polygon
from Utils import utils

sound_effect = pygame.mixer.Sound("assets/sound/beep.mp3")
font = pygame.font.Font(None, 36)

class Game:
    def __init__(self) -> None:
        self.numSides = 8
        self.polygonRad = 20
        self.center = Vector2(utils.width/2,utils.height/2)
        self.polygon = Polygon(self.center,self.polygonRad,self.numSides)
        self.ball = Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(0,0,255))
        self.isActive = True

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                sound_effect.play()
                # self.numSides -= 1
                # utils.world.DestroyBody(self.polygon.body)
                # self.polygon.body = self.polygon.create_polygon_body(self.numSides,self.polygonRad,self.center)
                print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    def draw(self):
        self.polygon.draw()
        self.ball.draw()