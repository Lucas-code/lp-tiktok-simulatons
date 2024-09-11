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
        self.ball = Ball(Vector2(utils.width/2 + random.randint(-15,15),utils.height/2 + random.randint(-15,15)),1,(255,0,0))
        self.rings = [Ring(Vector2(utils.width/2,utils.height/2),25-(i*5)) for i in range(5) ]
        # self.ring = Ring(Vector2(utils.width/2,utils.height/2),25)
        # self.ring2 = Ring(Vector2(utils.width/2,utils.height/2),20)
        # self.ring3 = Ring(Vector2(utils.width/2,utils.height/2),15)
        # self.ring4 = Ring(Vector2(utils.width/2,utils.height/2),10)
        self.startTime = pygame.time.get_ticks() 
        self.elapsed_time = 0
        self.current_note_index = 0

    def update(self):
        self.elapsed_time = pygame.time.get_ticks() - self.startTime
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                sound_effect.play()
                
                # print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    def draw(self):
        # self.ring.draw()
        # self.ring2.draw()
        # self.ring3.draw()
        # self.ring4.draw()
        

        for ring in self.rings:
                    
            ballPos = Vector2(utils.to_Pos(self.ball.circle_body.position))
            ringPos = Vector2(utils.width/2,utils.height/2)
            distance = ballPos.distance_to(ringPos)
            # print(distance,(ring.radius * utils.PPM))
            if distance > (ring.radius * utils.PPM) and ring.active:
                ring.active = False
                ring.trigger_particles()
                utils.world.DestroyBody(ring.body)
            ring.draw()
        self.ball.draw()
        seconds = (self.elapsed_time % 60000) // 1000
        text_surface = font.render(f"Time: {seconds:02} seconds", True, (255, 255, 255))
        utils.screen.blit(text_surface, (utils.width/2 - 100,10))