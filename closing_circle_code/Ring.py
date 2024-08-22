import math

import pygame
from Box2D import b2EdgeShape, Box2D, b2Body

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

        self.radius = radius

        self.size = 360
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((x, y))

        self.body : b2Body= utils.world.CreateKinematicBody(position=utils.from_Pos(pos))
        # self.body.gravityScale = 0
        # self.body.awake = False
        self.body.userData = self

        self.create_edge_shape()

    def update_vertices(self):
        """Recalculate the vertices based on the current radius."""
        self.vertices.clear()
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            self.vertices.append((x, y))
    
    def create_edge_shape(self):
        for i in range(self.size):
            angle = i * (360 / self.size)
            if (0 <= angle <= 360):
                v1 = self.vertices[i]
                v2 = self.vertices[(i + 1) % self.size]
                edge = b2EdgeShape(vertices=[v1, v2])
                self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)

    def update_radius(self, new_radius):
        """Update the radius and recreate the edge shapes."""
        self.radius = new_radius
        self.update_vertices()

        # Destroy the existing fixtures
        for fixture in self.body.fixtures:
            self.body.DestroyFixture(fixture)

        # Recreate edge shapes with the new radius
        self.create_edge_shape()
    
    def draw(self):
        self.color = self.interpolate_color(self.colourPalette[self.currentColourIndex],
                                      self.colourPalette[self.nextColourIndex], self.interpolationFactor)
        self.interpolationFactor += self.colourTransSpeed
        if self.interpolationFactor >= 1:
            self.interpolationFactor = 0
            self.currentColourIndex = self.nextColourIndex
            self.nextColourIndex = (self.nextColourIndex + 1) % len(self.colourPalette)
        self.draw_edges()
        self.update_radius(self.radius-0.004)
    
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