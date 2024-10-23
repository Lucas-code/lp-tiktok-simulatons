from Box2D import b2ContactListener, b2Contact, b2Fixture, b2Body

class ContactListener(b2ContactListener):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.collisions = []

    def BeginContact(self, contact : b2Contact):
        fixtureA : b2Fixture = contact.fixtureA
        fixtureB : b2Fixture = contact.fixtureB

        from Polygon import PolygonEdgeData, Polygon
        from Ball import Ball

        bodyA : b2Body = fixtureA.body
        bodyB : b2Body = fixtureB.body

        if(any(map(lambda x: isinstance(x.userData,Polygon),(bodyA,bodyB))) and any(map(lambda x: isinstance(x.userData,Ball),(bodyA,bodyB)))):
            self.collisions.append((bodyA,bodyB))
        
    def EndContact(self, contact : b2Contact):
        fixtureA : b2Fixture = contact.fixtureA
        fixtureB : b2Fixture = contact.fixtureB

        from Polygon import PolygonEdgeData, Polygon
        from Ball import Ball

        bodyA : b2Body = fixtureA.body
        bodyB : b2Body = fixtureB.body


        print(type(fixtureA.userData),type(fixtureB.userData))
        # print(any(map(lambda x: isinstance(x.userData,PolygonEdgeData),(bodyA,bodyB))),any(map(lambda x: isinstance(x.userData,Ball),(bodyA,bodyB))))

        if(any(map(lambda x: isinstance(x.userData,Polygon),(bodyA,bodyB))) and any(map(lambda x: isinstance(x.userData,Ball),(bodyA,bodyB)))):
            if isinstance(bodyA,Ball):
                bodyA.userData.auraPoints += fixtureB.userData.score
            else:
                bodyB.userData.auraPoints += fixtureA.userData.score

