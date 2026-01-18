import random
from .draw import Canvas
import uuid
from .utils import Particle

class Engine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.EMPTY = 0
        self.OBSTICLE = 2
        self.USED = 3

        self.canvases = []
        self.pixels = []
        for _ in range(self.height):
            self.pixels.append([self.EMPTY for _ in range(width)])
    
    def add_canvas(self, canvas: Canvas):
        if isinstance(canvas, Canvas):
            self.canvases.append(canvas)
        else:
            raise ValueError("Wrong class")
    
    def run(self):
        self.start()
        while True:
            self.loop()
            for canvas in self.canvases:
                canvas.draw(self.pixels)
            self.update()
    
    def start(self):
        pass

    def loop(self):
        pass

    def update(self):
        pass

class BallDropEngine(Engine):
    def __init__(self, width=9, height=8):
        super().__init__(width, height)

    def start(self):
        pass

    def loop(self):
        pass

    def add_particle(self, y, x):
        red = random.randint(0, 30)
        green = random.randint(0, 30)
        blue = random.randint(0, 30)
        self.pixels[y][x] = Particle(uuid.uuid4(), red, green, blue)


    def update(self):
        new_pixels = [y.copy() for y in self.pixels]
        for y in range(self.height):
            xes = [x for x in range(self.width)]
            random.shuffle(xes)
            for x in xes:
                if isinstance(self.pixels[y][x], Particle):
                    if self.pixels[y+1][x] == self.EMPTY:
                        new_pixels[y][x] = self.EMPTY
                        new_pixels[y+1][x] = self.pixels[y][x]
                        self.pixels[y+1][x] = self.USED
                        continue
                    if self.pixels[y+1][x+1] == self.EMPTY and self.pixels[y+1][x-1] == self.EMPTY:
                        i = random.choice([1, -1])
                        new_pixels[y][x] = self.EMPTY
                        new_pixels[y+1][x+i] = self.pixels[y][x]
                        self.pixels[y+1][x+i] = self.USED
                        continue
                    if self.pixels[y+1][x+1] == self.EMPTY:
                        new_pixels[y][x] = self.EMPTY
                        new_pixels[y+1][x+1] = self.pixels[y][x]
                        self.pixels[y+1][x+1] = self.USED
                        continue
                    if self.pixels[y+1][x-1] == self.EMPTY:
                        new_pixels[y][x] = self.EMPTY
                        new_pixels[y+1][x-1] = self.pixels[y][x]
                        self.pixels[y+1][x-1] = self.USED
                        continue
        self.pixels = new_pixels
                