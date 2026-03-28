# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Appliccation configuration file with reusable helper functions
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import math

# ----- Window Settings -----
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# ----- Application Colors, all colors are in RGB -----
class APP_COLORS:
    BACKGROUND_LIGHT = (245, 245, 245)              # Application / Env background color - white
    ROBOT_PRIMARY_BLUE = (52, 152, 219)             # Robot's primary color - Blue
    ROBOT_ACCENT_BLUE = (41, 128, 185)              # Robot's sensor color - Accent blue
    OBSTACLE_PRIMARY_RED = (231, 76, 60)            # Primary obstacle color - Warm red
    OBSTACLE_BOUNDARY = (192, 57, 43)               # Darker color to contrast obstacle - Dark red
    TARGET_SUCCESS_GREEN = (46, 204, 113)           # Target reached color - Green
    TARGET_GLOW_MINT = (130, 224, 170)              # Glow to show the target - Mint
    TRAJECTORY_PURPLE = (155, 89, 182)              # Trajectory or Robot's path color - Purple
    SENSOR_WARNING_YELLOW = (241, 196, 15)          # Obstacle sensor warning color - Yellow
    TEXT_DARK = (44, 62, 80)                        # Application text color - Shades of black
    GRID_LIGHT = (220, 220, 220)                    # Differntiate grid lines for SLAM - Light gray
    COLLISION_ALERT = (255, 0, 0)                   # Collision alert warning - Red

# ----- Robot Settings -----
ROBOT_RADIUS = 20
ROBOT_MAX_SPEED = 2.3
ROBOT_TURN_SPEED = 0.035
SENSOR_RANGE = 120
SENSOR_ANGLES = [-60, -30, 0, 30, 60]
SAFE_DISTANCE = ROBOT_RADIUS * 2.8

# ----- Helper Functions -----
# Normalize the Robot's Angle, Used in sense method in robot.py
def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle