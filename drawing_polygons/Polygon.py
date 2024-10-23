import pygame
import Box2D
import math
from Utils import utils

class Polygon:
    def __init__(self, pos, radius, sides) -> None:
        self.pos = pos
        self.radius = radius
        self.sides = sides
        self.colour = (255,255,255)

        self.body = self.create_polygon_body(self.sides, self.radius, self.pos)
    
    def create_polygon_body(self,num_sides, radius, position) -> Box2D.b2Body:
        # Create a dynamic body (movable)
        # print(position,utils.from_Pos(position))
        body : Box2D.b2Body = utils.world.CreateKinematicBody(position=utils.from_Pos(position))
        body.userData = self
        
        vertices = []
        angle_step = 2 * math.pi / num_sides 
        
        for i in range(num_sides):
            # Calculate the angle for the current vertex
            angle = i * angle_step
            
            # Calculate the x and y coordinates using polar to Cartesian conversion
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            vertices.append((x, y))

        for vertex in vertices:
            print(vertex)
        
        try:
            for i in range(num_sides):
                v1 = vertices[i]
                v2 = vertices[(i + 1) % num_sides]  # Wrap around to create the last edge
                body.CreateEdgeFixture(vertices=[v1, v2], density=1.0, friction=0.0, restitution=0.1)
        except:
            print("idk man")

        return body
    
    def draw(self):
        colours = [
            (0,255,0),
            (255,255,255),
            (255,0,0)
        ]
        i = 0
        for fixture in self.body.fixtures:
            # Extract edge vertices and draw them as lines
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])

            pygame.draw.line(utils.screen, colours[i], v1, v2, 2)
            i = (i + 1) % len(colours)