#                 ░░
#               ░░██░░
#             ░░      ░░
#           ░░██  XX  ██░░
#         ░░              ░░
#       ░░██  XX  ██  XX  ██░░
#     ░░                      ░░
#   ░░██  XX  ██  XX  ██  XX  ██░░
#     ░░                      ░░
# 00  00░░██  XX  ██  XX  ██░░00  00
#         ░░              ░░
#     00  00░░██  XX  ██░░00  00
#             ░░      ░░
#         00  00░░██░░00  00
#                 ░░
#             00  00  00 

from simpler_drop import TerminalCanvas
from simpler_drop import Engine

class MyEngine(Engine):
    def start(self):
        offset = 0
        for y in range(self.height//2, self.height):
            self.pixels[y][offset] = self.OBSTICLE
            self.pixels[y][offset+1] = self.OBSTICLE
            self.pixels[y][-offset-1] = self.OBSTICLE
            self.pixels[y][-offset-2] = self.OBSTICLE
            offset += 1
        self.particles_counter = 0
        self.counter = 0
    
    def loop(self):
        self.counter += 1
        if self.counter%5==0:
            self.add_particle(0, self.width//2)
            self.particles_counter += 1

engine = MyEngine()
engine.add_canvas(TerminalCanvas())
engine.run()