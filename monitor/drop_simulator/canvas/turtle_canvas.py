from canvas.canvas import Canvas, QueueElement, ObjActions
import datetime
import turtle
import asyncio
import logging

logger = logging.getLogger()

# Stores all objects to draw (whiout coords)
class TurtleCanvas(Canvas):
    def __init__(self, queue: list, fps=30):
        super().__init__(queue, fps)
        screen = turtle.Screen()
        screen.setup(width=800, height=800)
        turtle.tracer(0)
        self.particles: dict[turtle.Turtle] = {}
    
    def draw_frame(self, frame: dict[QueueElement]):
        for id, obj in frame.items():
            match obj.action:
                case ObjActions.CREATE:
                    logger.info("Creating new object")
                    t = turtle.Turtle()
                    self.particles[id] = t
                    t.speed(0)
                    t.shape("circle")
                    t.penup()
                    t.turtlesize(obj.radius/10, obj.radius/10, 1)
                    t.goto(obj.x, obj.y)
                    continue
                case ObjActions.MOVE:
                    t = self.particles[id]
                    t.goto(obj.x, obj.y)
                    continue
                case ObjActions.DELETE:
                    t = self.particles[id]
                    t.hideturtle()
                    t.clear()
                    del self.particles[id]
                    continue
        turtle.update()