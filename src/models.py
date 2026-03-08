from enum import Enum
from dataclasses import dataclass
from .config import *

class RobotState(Enum):
    SEARCHING = "Searching for target"
    AVOIDING = "Avoiding obstacle"
    MOVING_TO_TARGET = "Moving to target"
    TARGET_REACHED = "Target reached!"
    STUCK = "Stuck - cannot reach target"

@dataclass
class Obstacle:
    x: float
    y: float
    radius: float
    color: tuple = APP_COLORS.OBSTACLE
    
    def __init__(self, x, y, radius, color=APP_COLORS.OBSTACLE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

@dataclass
class Target:
    x: float
    y: float
    radius: int = 15
    reached: bool = False
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.reached = False