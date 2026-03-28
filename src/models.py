# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Application models, better for code reusability
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

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
    color: tuple = APP_COLORS.OBSTACLE_PRIMARY_RED
    
    def __init__(self, x, y, radius, color=APP_COLORS.OBSTACLE_PRIMARY_RED):
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