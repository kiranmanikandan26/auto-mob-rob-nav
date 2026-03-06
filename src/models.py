from enum import Enum
from dataclasses import dataclass

class RobotState(Enum):
    SEARCHING = "Searching"
    AVOIDING = "Avoiding"
    MOVING = "Moving"
    REACHED = "Reached"

@dataclass
class Obstacle:
    x: float; y: float; radius: float; color: tuple

@dataclass
class Target:
    x: float; y: float; radius: int = 15; reached: bool = False