from engine.engine import Particle, Obsticle, SimpleColisionEngine
from canvas.turtle_canvas import TurtleCanvas
from canvas.terminal_canvas import TerminalCanvas
import logging
from rich.live import Live


logging.basicConfig(level=logging.WARN)

class Engine(SimpleColisionEngine):

    def start(self):
        self.counter = 0

    def loop(self):
        if self.counter % 200 == 0:
            self.add_particle(Particle(1, 150, radius=15, mass=1, friction=0.9))
        self.counter += 1


if __name__ == "__main__":
    ps = []
    o1 = Obsticle(200, 0, 0, -200, friction=0.3)
    o2 = Obsticle( 0, -200, -200, 0, friction=0.3)
    engine = Engine(ps, [o1, o2])
    # canv = TurtleCanvas
    canv = TerminalCanvas
    engine.register_canvas(canv)
    engine.run()