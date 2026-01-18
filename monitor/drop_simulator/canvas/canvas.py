from dataclasses import dataclass 
from enum import Enum
import logging
import asyncio
import datetime

logger = logging.getLogger()


class ObjActions(Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    MOVE = "MOVE"

# Single object
@dataclass
class QueueElement:
    x: int
    y: int
    radius: int
    action: ObjActions

class Canvas:
    def __init__(self, queue: list[QueueElement], fps=30):
        self.queue = queue
        self.fps = fps

    async def draw(self):
        while True:
            start = datetime.datetime.now()

            if not self.queue:
                logger.info("No frames to get!")
                await asyncio.sleep(0.01)
                continue
            frame = self.queue.pop(0)

            self.draw_frame(frame)
            took = (datetime.datetime.now() - start).microseconds/1000000
            if took > 1/self.fps:
                logger.warning("Too slow frame visualization!!")
                continue
            else:
                await asyncio.sleep(1/self.fps - took)
                continue

    def draw_frame(self, frame: dict[QueueElement]):
        pass