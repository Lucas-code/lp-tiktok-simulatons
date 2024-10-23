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
        self.balls = [Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(255,0,0))]
        self.ring = Ring(Vector2(utils.width/2,utils.height/2),20)
        self.current_note_index = 0
        self.isActive = True

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
            if distance > (self.ring.radius * utils.PPM) and self.isActive:
                utils.world.DestroyBody(ball.circle_body)
                self.balls.remove(ball)
                self.balls.append(Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(255,0,0)))
                self.balls.append(Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(255,0,0)))
                # ball.score -= 1
                # self.adjust_ring_color()
                # if ball.score <= 0:
                #     self.isActive = False
                #     self.ring.active = False
                # else:
                #     ball.respawn()
        
        self.ring.draw()

        numBallsText = font.render(f"Number of balls: {len(self.balls)}", True, (255, 255, 255))
        utils.screen.blit(numBallsText, (135,75))
        
        # redScoreText = font.render(f"Red : {self.redBall.score}", True, (255, 0, 0))
        # utils.screen.blit(redScoreText, (70,550))

        # blueScoreText = font.render(f"Blue : {self.blueBall.score}", True, (0, 0, 255))
        # utils.screen.blit(blueScoreText, (330,550))

        # if not self.isActive:
            # winner, colour = ("Blue", (0,0,255)) if self.redBall.score == 0 else ("Red", (255,0,0))
            # winnerText = font.render(f"{winner} Wins!", True, colour)
            # utils.screen.blit(winnerText, (utils.width/2-65,utils.height/2-20))