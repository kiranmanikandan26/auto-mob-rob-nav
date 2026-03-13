# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Last Modifide Date : 13-03-2025

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import math

# ----- Window Settings -----
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# ----- Application Colors -----
class APP_COLORS:
    BACKGROUND = (245, 245, 245)
    ROBOT = (52, 152, 219)
    ROBOT_SENSOR = (41, 128, 185)
    OBSTACLE = (231, 76, 60)
    OBSTACLE_BOUNDARY = (192, 57, 43)
    TARGET = (46, 204, 113)
    TARGET_GLOW = (130, 224, 170)
    PATH = (155, 89, 182)
    SENSOR_RAY = (241, 196, 15)
    TEXT = (44, 62, 80)
    GRID = (220, 220, 220)
    COLLISION = (255, 0, 0)

# ----- Robot Settings -----
ROBOT_RADIUS = 20
ROBOT_MAX_SPEED = 2.3
ROBOT_TURN_SPEED = 0.035
SENSOR_RANGE = 120
SENSOR_ANGLES = [-60, -30, 0, 30, 60]
SAFE_DISTANCE = ROBOT_RADIUS * 2.8

# ----- Helper Function to Normalize the Robot's Angle, Used in sense method -----
def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle