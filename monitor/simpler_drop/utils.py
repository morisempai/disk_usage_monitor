from dataclasses import dataclass
import uuid

@dataclass
class Particle:
    id: uuid.UUID
    red: int
    green: int
    blue: int