import pygame
import Box2D
import math
from Utils import utils

font = pygame.font.Font(None, 36)

class Polygon:
    def __init__(self, pos, radius, sides) -> None:
        self.pos = pos
        self.radius = radius
        self.sides = 12
        self.colour = (255,255,255)
        self.auraScores = [100,0,-1000,0,1500,0,-150,0,-200,0,400,0]

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

        for i in range(num_sides):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % num_sides]  # Wrap around to create the last edge
            if self.auraScores[i] > 0:
                colour = (0,255,0)
            elif self.auraScores[i] < 0:
                colour = (255,0,0)
            else:
                colour = (255,255,255)
            fixture = body.CreateEdgeFixture(vertices=[v1, v2], density=1.0, friction=0.0, restitution=1.05, userData=PolygonEdgeData(self.auraScores[i],colour))
            # fixture.userData = PolygonEdgeData(self.auraScores[i],colour)

        return body
    
    def draw(self):
        for fixture in self.body.fixtures:
            # Extract edge vertices and draw them as lines
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])

            pygame.draw.line(utils.screen, fixture.userData.colour, v1, v2, 2)

            self.draw_edge_labels(v1,v2,f"{fixture.userData.score}")

    def draw_edge_labels(self,v1,v2,text):
        # For each edge, calculate the label position outside the polygon            
        # Calculate the midpoint of the edge
        mid_x = (v1[0] + v2[0]) / 2
        mid_y = (v1[1] + v2[1]) / 2

        # Calculate the vector along the edge
        edge_vec_x = v2[0] - v1[0]
        edge_vec_y = v2[1] - v1[1]

        # Calculate the normal vector (perpendicular to the edge)
        normal_vec_x = -edge_vec_y
        normal_vec_y = edge_vec_x

        # Normalize the normal vector
        length = math.sqrt(normal_vec_x ** 2 + normal_vec_y ** 2)
        normal_vec_x /= length
        normal_vec_y /= length

        # Offset the text position along the normal (outside the polygon)
        offset_distance = 30  # Distance from the edge to place the label
        text_x = mid_x + normal_vec_x * offset_distance
        text_y = mid_y + normal_vec_y * offset_distance

        # Render the text
        text_surface = font.render(f"{text}", True, (255, 255, 255))

        # Get the size of the text surface
        text_rect = text_surface.get_rect()

        # Adjust the position to center the text
        text_x -= text_rect.width / 2
        text_y -= text_rect.height / 2

        # Blit the text onto the screen at the computed position
        utils.screen.blit(text_surface, (text_x, text_y))
        # print((text_x, text_y))

class PolygonEdgeData:
    def __init__(self,score,colour):
        self.score = score
        self.colour = colour