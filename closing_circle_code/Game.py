from pygame import Vector2
from time import sleep
from Ball import Ball
from Ring import Ring
from Utils import utils
from sound import *

midi_notes = process_sound(r"assets\sound\Mario Bros. - Super Mario Bros. Theme.mid")

class Game:
    def __init__(self):
        self.ball = Ball(Vector2(utils.width/2,utils.height/2),2,(255,0,0))
        self.ring = Ring(Vector2(utils.width/2,utils.height/2),25)
        self.current_note_index = 0

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        if utils.contactListener:
            for _,_ in utils.contactListener.collisions:
                if self.current_note_index >= len(midi_notes):
                    self.current_note_index = 0

                note, velocity = midi_notes[self.current_note_index]
                utils.midiOutput.note_on(note, velocity, utils.midiChannel)

                # Stop the previous note (optional)
                if self.current_note_index > 0:
                    prev_note, _ = midi_notes[self.current_note_index - 1]
                    utils.midiOutput.note_off(prev_note, utils.midiChannel)

                # Move to the next note
                self.current_note_index += 1
                
                # print("Collision has just been made")
                break
            utils.contactListener.collisions = []

    def draw(self):
        self.ring.draw() 
        self.ball.draw()