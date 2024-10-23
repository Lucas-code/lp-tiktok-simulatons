import pygame
import random
from pygame import Vector2
from time import sleep
from Ball import Ball
from Polygon import Polygon
from Utils import utils
from typing import List

sound_effect = pygame.mixer.Sound("assets/sound/beep.mp3")
font = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 26)

class Game:
    def __init__(self) -> None:

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        colours = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
        ]

        self.numSides = 10
        self.polygonRad = 20
        self.center = Vector2(utils.width/2,utils.height/2-30)
        self.polygon = Polygon(self.center,self.polygonRad,self.numSides)
        self.balls : List[Ball] = []
        for month in months:
            self.balls.append(Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,random.choice(colours),month))
        # self.ball = Ball(Vector2(utils.width/2 + random.randint(-30,30),utils.height/2 + random.randint(-30,30)),1,(0,0,255))
        self.isActive = True
        self.startTime = pygame.time.get_ticks() 
        self.elapsed_time = 0

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        self.elapsed_time = pygame.time.get_ticks() - self.startTime
        seconds = (self.elapsed_time % 60000) // 1000
        if seconds > 29:
            self.isActive = False
        if utils.contactListener:
            for bodyA, bodyB in utils.contactListener.collisions:
                sound_effect.play()
                # print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    def draw(self):
        self.polygon.draw()
        
        for ball in self.balls:
            ball.draw()
        
        seconds = (self.elapsed_time % 60000) // 1000
        text_surface = font2.render(f"Time Elapsed: {seconds:02} seconds", True, (255, 255, 255))
        utils.screen.blit(text_surface, (utils.width/2 - text_surface.get_rect().width / 2,10))
        
        for i, ball in enumerate(self.balls):
            # Calculate row and column based on index
            row = i // 4
            col = i % 4

            # Calculate grid position based on row and column
            grid_x = 115 + col * 120
            grid_y = 520 + row * 20

            # Combine month and score into a single text string
            combined_text = f'{ball.month}: {ball.auraPoints}'
            
            # Prepare the text to be displayed
            text_surface = font.render(combined_text, True, (255, 255, 255))

            # Get the size of the text surface
            text_rect = text_surface.get_rect()

            # Position text centered in the grid cell
            text_x = grid_x - text_rect.width / 2
            text_y = grid_y - text_rect.height / 2
            
            # Blit combined text
            utils.screen.blit(text_surface, (text_x, text_y))