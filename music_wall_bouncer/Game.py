import pygame
from pygame import Vector2
import random

from Camera import Camera
from Square import Square
from midi import list_notes_from_midi
from utils import utils


class Game:
    def __init__(self):
        self.all_notes = list_notes_from_midi(r"assets\sound\Naruto No Chord.mid")
        # print(self.all_notes)

        self.square = Square(Vector2(10,utils.height/2))
        self.camera = Camera(utils.width,utils.height)
        self.camera.set_target(self.square)

        self.points = []

        self.time = 0
        self.fixedDeltaTime = 0.016

        #################
        # self.pointsUp = []
        # self.pointsDown = []
        # self.pointsLeft = []
        # self.pointsRight = []
        # self.pointsUp = self.loadPosFromFile("posUp.txt")
        # self.pointsDown = self.loadPosFromFile("posDown.txt")

        # self.points = self.pointsUp + self.pointsDown

        # self.pointsUp = self.addSpaceBetweenPoint(self.pointsUp)
        # self.pointsDown = self.addSpaceBetweenPoint(self.pointsDown)

        # self.pointsUp = self.makeGridAlignedPolygonUp(self.pointsUp)
        # self.pointsDown = self.makeGridAlignedPolygonDown(self.pointsDown)

        # self.polygon = [self.pointsDown[0]] + self.pointsUp + [self.pointsUp[-1]]  + list(reversed(self.pointsDown))
        
        # for point in self.pointsLeft + self.pointsRight:
        #     self.polygon.insert(point['index'],point['pos'])

    def makeGridAlignedPolygonUp(self, points):
        aligned_points = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            aligned_points.append(p1)
            if p2.y < p1.y:
                aligned_points.append(Vector2(p1.x, p2.y))
            else:
                aligned_points.append(Vector2(p2.x, p1.y))
        aligned_points.append(points[-1])  # Add the last point
        return aligned_points

    def makeGridAlignedPolygonDown(self, points):
        aligned_points = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            aligned_points.append(p1)
            if p2.y > p1.y:
                aligned_points.append(Vector2(p1.x, p2.y))
            else:
                aligned_points.append(Vector2(p2.x, p1.y))
        aligned_points.append(points[-1])  # Add the last point
        return aligned_points


    def addSpaceBetweenPoint(self,points):
        new_points = []
        for p in points:
            new_points.append(Vector2(p.x-50,p.y))
            new_points.append(Vector2(p.x , p.y))
            new_points.append(Vector2(p.x + 50, p.y))
        return new_points


    def update(self):
        self.time += self.fixedDeltaTime
        for note in self.all_notes:
            if note['start_time'] <= self.time and not note['play'] and note['velocity'] > 0:
                note['play'] = True
                pos = Vector2(0,0)
                if random.random() > 0.1:
                    if self.square.vel.y < 0:
                        pos = Vector2(self.square.pos.x, self.square.pos.y)
                        self.points.append(pos)
                        # self.savePosToFile(pos,"posUp.txt")
                    elif self.square.vel.y > 0:
                        pos = Vector2(self.square.pos.x, self.square.pos.y) #+ self.square.width)
                        self.points.append(pos)
                    # self.savePosToFile(pos, "posDown.txt")
                    self.square.vel.y *= -1
                else:
                    if self.square.vel.x < 0:
                        pos = Vector2(self.square.pos.x, self.square.pos.y)
                        self.points.append(pos)
                        # self.savePosToFile(pos,"posLeft.txt")
                    elif self.square.vel.x > 0:
                        pos = Vector2(self.square.pos.x, self.square.pos.y) #+ self.square.width)
                        self.points.append(pos)
                    # self.savePosToFile(pos, "posRight.txt")
                    self.square.vel.x *= -1
                
                if note == (next((n for n in reversed(self.all_notes) if n['velocity'] > 0), None)):
                    self.square.vel = Vector2(0,0)

                utils.player.note_on(note['name'], min(note['velocity'] * utils.volumeScale,127)  )
            if note['start_time'] <= self.time and not note['play'] and note['velocity'] == 0:
                note['play'] = True
                utils.player.note_off(note['name'], 0)                

        self.square.update(self.fixedDeltaTime)
        self.camera.update()

    def draw(self):

        # if self.polygon:
        #     pygame.draw.polygon(utils.screen, (26, 72, 112),
        #                         [self.camera.apply_pos(p) for p in self.polygon])
        #     pygame.draw.polygon(utils.screen, (26, 100, 23),
        #                         [self.camera.apply_pos(p) for p in self.polygon],4)

        for p in self.points:
            pos = self.camera.apply_pos(Vector2(p.x,p.y))
            pygame.draw.rect(utils.screen,(255,23,23),pygame.Rect(pos,(10,10)))

        self.square.draw(self.camera)


    def savePosToFile(self, pos, filename):
        with open(filename, "a") as file:
            file.write(f"{pos.x}, {pos.y}\n")

    def loadPosFromFile(self, filename):
        positions = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    x, y = map(float, line.strip().split(","))
                    positions.append(Vector2(x, y))
        except FileNotFoundError:
            print(f"No saved positions found in {filename}.")
        return positions