import math
import random
import pygame
from pygame import Vector2
from Box2D import b2EdgeShape, Box2D, b2Body
from Particle import Particle
from Utils import utils


class Ring:
    def __init__(self, pos, radius):

        self.colourPalette = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
        ]
        self.currentColourIndex = 0
        self.nextColourIndex = 1
        self.colourTransSpeed = 0.01
        self.interpolationFactor = 0
        self.color = self.colourPalette[self.currentColourIndex]

        self.particles : list[Particle] = []
        
        self.active = True

        self.rotationSpeed = random.randint(1,50)/1000
        
        self.radius = radius

        self.size = 360
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((x, y))

        self.body : b2Body= utils.world.CreateKinematicBody(position=utils.from_Pos(pos))
        self.body.userData = self

        self.create_edge_shape()
    
    def create_edge_shape(self):

        rand_angle = random.randint(40,100)
        rand_gap = random.randint(30,50)

        for i in range(self.size):
            angle = i * (360 / self.size)
            if (0 <= angle <= rand_angle) or (rand_angle + rand_gap <= angle  <= 360):
                v1 = self.vertices[i]
                v2 = self.vertices[(i + 1) % self.size]
                edge = b2EdgeShape(vertices=[v1, v2])
                self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)
    
    def trigger_particles(self):
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            velocity = Vector2(math.cos(angle), math.sin(angle)) * random.uniform(1, 3)
            particle = Particle(utils.to_Pos(self.body.position), velocity, self.color, random.randint(30, 60))
            self.particles.append(particle)
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
    
    def draw(self):
        if self.active:
            self.color = self.interpolate_color(self.colourPalette[self.currentColourIndex],
                                        self.colourPalette[self.nextColourIndex], self.interpolationFactor)
            self.interpolationFactor += self.colourTransSpeed
            if self.interpolationFactor >= 1:
                self.interpolationFactor = 0
                self.currentColourIndex = self.nextColourIndex
                self.nextColourIndex = (self.nextColourIndex + 1) % len(self.colourPalette)

            self.body.angle += self.rotationSpeed

            self.draw_edges()
        
        self.update_particles()
        for particle in self.particles:
            particle.draw()
    
    # Function to interpolate between two colors
    def interpolate_color(self,color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 2)