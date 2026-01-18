import time
from rich.live import Live
from dataclasses import dataclass
import uuid
from .utils import Particle

@dataclass
class VirtualPixel:
    id: uuid.uuid4
    x: int
    y: int



class Canvas:
    def __init__(self, fps=10):
        self.fps = fps
    
    def draw(self, pixels):
        pass

class TerminalCanvas(Canvas):
    def __init__(self, fps=10):
        super().__init__(fps)
        self.live = Live()
        self.live.start()
        self.particle = "██"
        self.value_map = {
            0: "  ",
            1: "██",
            2: "░░"
            }

    def draw(self, pixels):
        drawing = ""
        for x_row in pixels:
            for pixel in x_row:
                if isinstance(pixel, Particle):
                    drawing += self.particle
                else:
                    drawing += self.value_map[pixel]
            drawing += "\n"
        self.live.update(drawing)
        time.sleep(1/self.fps)
    
