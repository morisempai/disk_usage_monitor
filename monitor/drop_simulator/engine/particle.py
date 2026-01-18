import uuid

class Particle:
    def __init__(self, x, y, mass=1, radius=1, friction=0.96):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.friction = friction

        self.velocity_x = 0
        self.velocity_y = 0