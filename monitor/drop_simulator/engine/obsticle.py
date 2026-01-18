from engine.utils import rotate

class Obsticle:
    def __init__(self, x1, y1, x2, y2, friction=0.9):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.friction = friction

        x_half_width = (x1 - x2)/2
        y_half_width = (y1 - y2)/2

        self.middle_x = x2 + x_half_width
        self.middle_y = y2 + y_half_width
        self.x_half_width = abs(x_half_width)
        self.y_half_width = abs(y_half_width)

        self.lengh = ((self.y1 - self.y2)**2 + (self.x1 - self.x2)**2)**0.5

        self.sin_coof = (x1 - x2)/self.lengh
        self.cos_coof = (y1 - y2)/self.lengh

        self.x1_rotated, self.y1_rotated = rotate(self.x1, self.y1, self.sin_coof, self.cos_coof)
        self.x2_rotated, self.y2_rotated = rotate(self.x2, self.y2, self.sin_coof, self.cos_coof)

        self.rotated_middle_y = self.y1_rotated - self.lengh/2
        self.rotated_middle_x = self.x1_rotated
