from Box2D import b2ContactListener, b2Contact, b2Fixture, b2Body
import random

colours = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
]

class ContactListener(b2ContactListener):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.collisions = []

    def BeginContact(self, contact : b2Contact):
        fixtureA : b2Fixture = contact.fixtureA
        fixtureB : b2Fixture = contact.fixtureB

        bodyA : b2Body = fixtureA.body
        bodyB : b2Body = fixtureB.body

        from Ring import Ring
        from Ball import Ball

        if(any(map(lambda x: isinstance(x.userData,Ring),(bodyA,bodyB))) and any(map(lambda x: isinstance(x.userData,Ball),(bodyA,bodyB)))):
            # if isinstance(bodyA,Ball):
            #     bodyA.userData.color = random.choice(colours)
            # else:
            #     bodyB.userData.color = random.choice(colours)
            self.collisions.append((bodyA,bodyB))

