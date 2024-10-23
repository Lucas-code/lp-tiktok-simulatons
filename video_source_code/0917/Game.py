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
        self.redBall = Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(255,0,0))
        self.blueBall = Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(0,0,255))
        self.balls = [self.redBall, self.blueBall]
        self.rings = [Ring(Vector2(utils.width/2,utils.height/2),20-(i*5)) for i in range(4) ]
        self.current_note_index = 0
        self.isActive = True
        self.winner = None

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                sound_effect.play()
                
                # print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    # def adjust_ring_color(self):
    #     if self.redBall.score > self.blueBall.score:
    #         self.ring.color = (255,0,0)
    #     elif self.blueBall.score > self.redBall.score:
    #         self.ring.color = (0,0,255)
    #     elif self.blueBall.score == self.redBall.score:
    #         self.ring.color = (255,255,255)
    
    def draw(self):
        for ball in self.balls:
            ball.draw()
            ballPos = Vector2(utils.to_Pos(ball.circle_body.position))
            ringPos = Vector2(utils.width/2,utils.height/2)
            distance = ballPos.distance_to(ringPos)
            if self.rings:
                if distance > (self.rings[-1].radius * utils.PPM) and self.isActive:
                    self.rings[-1].active = False
                    self.rings[-1].trigger_particles()
                    utils.world.DestroyBody(self.rings[-1].body)
                    self.rings.pop()
                    if self.rings == []:
                        self.winner = ball
                        self.isActive = False
                        break
        
        for ring in self.rings:
            ring.draw()

        # numBallsText = font.render(f"Number of balls: {len(self.balls)}", True, (255, 255, 255))
        # utils.screen.blit(numBallsText, (135,75))
        
        # redScoreText = font.render(f"Red : {self.redBall.score}", True, (255, 0, 0))
        # utils.screen.blit(redScoreText, (70,550))

        # blueScoreText = font.render(f"Blue : {self.blueBall.score}", True, (0, 0, 255))
        # utils.screen.blit(blueScoreText, (330,550))

        if not self.isActive:
            winner= "Blue"if self.winner.color == (0,0,255) else "Red"
            winnerText = font.render(f"{winner} Wins!", True, self.winner.color)
            utils.screen.blit(winnerText, (utils.width/2-65,utils.height/2-20))