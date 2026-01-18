from canvas.canvas import Canvas, QueueElement, ObjActions
import datetime
import asyncio
import logging
from rich.live import Live
from scipy.spatial import KDTree 

logger = logging.getLogger()

# Stores all objects to draw (whiout coords)
class TerminalCanvas(Canvas):
    def __init__(self, queue: list, fps=60, width=20, height=20, pixel_start=(-200,-200), pixel_step=25, pixel_fire_radius=15):
        super().__init__(queue, fps)
        self.colours = ["  ", "░░", "▒▒", "▓▓" "██"]
        self.live = Live("", refresh_per_second=self.fps)
        self.live.start()

        self.width = width
        self.height = height
        self.pixel_start = pixel_start # coords of the first pixel
        self.pixel_step = pixel_step # how far pixel is from eachother (baisically it controlls zoom)
        self.pixel_fire_radius = pixel_fire_radius # extra space between pixel to fire

        self.pixels_coords = [] # Pixels to draw
        for y in range(self.pixel_start[1]+self.pixel_step*self.height, self.pixel_start[1], -self.pixel_step):
            for x in range(self.pixel_start[0], self.pixel_start[0]+self.pixel_step*self.width, self.pixel_step):
                self.pixels_coords.append((x,y))
                
    def draw_frame(self, frame: dict[QueueElement]):
        particles = []
        for _, obj in frame.items():
            particles.append((obj.x, obj.y))
        tree = KDTree(particles)
        draw_string = ""
        pixel_counter = 0
        for pixel in tree.query_ball_point(self.pixels_coords, self.pixel_fire_radius):
            pixel_counter += 1
            if len(pixel) >= len(self.colours):
                draw_string += self.colours[-1]
            else:
                draw_string += self.colours[len(pixel)]
            if pixel_counter >= self.width:
                draw_string += "\n"
                pixel_counter = 0
        self.live.update(draw_string)
        # print(tree.query_ball_point(self.pixels_coords, self.pixel_fire_radius))
