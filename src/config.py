from enum import Enum


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
ROBOT_RADIUS = 20
ROBOT_MAX_SPEED = 2.5
ROBOT_TURN_SPEED = 0.03
SENSOR_RANGE = 120
SENSOR_ANGLES = [-60, -30, 0, 30, 5]
SAFE_DISTANCE = ROBOT_RADIUS * 2.5

# Application Colors
class APP_COLORS(Enum):
    BLUE = (0, 0, 255),
    WHITE = (255, 255, 255),
    BLACK = (0, 0, 0),
    GREEN = (0, 255, 0),
    RED = (255, 0, 0),
    YELLOW = (255, 255, 0),
    ORG_YELLOW = (241, 196, 15),
    PURPLE = (155, 89, 182),
    BRI_GREEN = (46, 204, 113),
    NAVY = (44, 62, 80)