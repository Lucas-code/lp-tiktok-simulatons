import pygame
import random
from pygame import Vector2
from time import sleep
from Ball import Ball
from Ring import Ring
from Utils import utils

sound_effect = pygame.mixer.Sound("assets/sound/beep.mp3")
font = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.ballLife = 5
        self.ballRad = 1
        self.balls = []
        self.ball = Ball(Vector2(utils.width/2 + random.randint(-15,15),utils.height/2 + random.randint(-15,15)),self.ballRad,(255,0,0),self.ballLife)
        self.rings = [Ring(Vector2(utils.width/2,utils.height/2),25-(i*3)) for i in range(4) ]
        self.elapsed_time = 0
        self.current_note_index = 0
        self.current_ball = self.ball
        self.balls.append(self.ball)
        self.gameOver = False

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                sound_effect.play()
                
                # print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    def draw(self):
        if (not self.current_ball.active) and (not self.gameOver):
            self.ballLife += 1
            # self.ballRad += 0.1
            new_ball = Ball(Vector2(utils.width/2 + random.randint(-15,15),utils.height/2 + random.randint(-15,15)),self.ballRad,(255,0,0),self.ballLife)
            self.current_ball = new_ball
            self.balls.append(new_ball)

        for ring in self.rings:
                    
            ballPos = Vector2(utils.to_Pos(self.current_ball.circle_body.position))
            ringPos = Vector2(utils.width/2,utils.height/2)
            distance = ballPos.distance_to(ringPos)
            # print(distance,(ring.radius * utils.PPM))
            if distance > (ring.radius * utils.PPM) and ring.active:
                ring.active = False
                ring.trigger_particles()
                utils.world.DestroyBody(ring.body)
                if ring == self.rings[0]:
                    self.current_ball.deactivateBall()
                    self.gameOver = True
            ring.draw()
        for ball in self.balls:
            ball.draw()
        # text_surface = font.render(f"Time: {seconds:02} seconds", True, (255, 255, 255))
        # utils.screen.blit(text_surface, (utils.width/2 - 100,10))