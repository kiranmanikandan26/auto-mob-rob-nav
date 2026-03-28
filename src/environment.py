# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Create and maintain simulation environment
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import pygame
from .config import *
from .models import Obstacle, Target
from .robot import HomeRobot

class HomeEnvironment:

    # ----- Creates Home Environment With Obstacles -----
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.target = None
        self.robot = None
    
    # ----- Living Room Layout -----
    def create_living_room_layout(self):
        self.obstacles = [
            Obstacle(300, 200, 80, (139, 69, 19)),    # Brown sofa
            Obstacle(300, 280, 80, (160, 82, 45)),    # Cushions
            Obstacle(500, 400, 40, (210, 180, 140)),  # Coffee table
            Obstacle(700, 200, 60, (105, 105, 105)),  # TV stand
            Obstacle(150, 500, 30, (34, 139, 34)),    # Plant
            Obstacle(800, 550, 20, (255, 215, 0))     # Lamp
        ]
        return self.obstacles
    
     # ----- Kitchen Layout -----
    def create_kitchen_layout(self):
        self.obstacles = [
            Obstacle(400, 350, 100, (200, 200, 200)),  # Kitchen island
            Obstacle(650, 450, 30, (139, 69, 19)),     # Chair
            Obstacle(700, 450, 30, (139, 69, 19)),     # Chair
            Obstacle(675, 400, 30, (139, 69, 19)),     # Chair
            Obstacle(200, 150, 50, (255, 255, 255)),   # Refrigerator
        ]
        return self.obstacles
    
     # ----- Bed Room Layout -----
    def create_bedroom_layout(self):
        self.obstacles = [
            Obstacle(300, 300, 120, (100, 149, 237)),  # Bed
            Obstacle(500, 250, 25, (160, 82, 45)),     # Nightstand
            Obstacle(700, 500, 60, (210, 180, 140)),   # Dresser
            Obstacle(200, 550, 50, (139, 69, 19)),     # Wardrobe
        ]
        return self.obstacles
    
     # ----- Nested Rooms and Typical Wild Environment Layout -----
    def create_mixed_home_layout(self):
        self.obstacles = [
            # Living area
            Obstacle(250, 200, 70, (139, 69, 19)),     # Sofa
            Obstacle(450, 150, 40, (105, 105, 105)),   # TV
            
            # Kitchen area
            Obstacle(700, 300, 60, (200, 200, 200)),   # Island
            Obstacle(800, 450, 30, (139, 69, 19)),     # Stool
            
            # Bedroom area
            Obstacle(200, 550, 50, (100, 149, 237)),   # Bed corner
            Obstacle(350, 600, 30, (160, 82, 45)),     # Nightstand
            
            # Play area (kids' toys)
            Obstacle(600, 600, 20, (255, 0, 0)),       # Red ball
            Obstacle(650, 620, 15, (0, 255, 0)),       # Green ball
            Obstacle(620, 580, 12, (0, 0, 255)),       # Blue block
        ]
        return self.obstacles
    
     # ----- Target Location -----
    def set_target(self, x, y):
        self.target = Target(x, y)
        return self.target
    
     # ----- Set Robot in the Environment -----
    def set_robot(self, x, y, name="Home Env Robot"):
        self.robot = HomeRobot(x, y, name)
        return self.robot
    
     # ----- Draw Home Background -----
    def draw_background_grid(self, screen):
        # Draw grid lines
        for x in range(0, self.width, 50):
            pygame.draw.line(screen, APP_COLORS.GRID, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 50):
            pygame.draw.line(screen, APP_COLORS.GRID, (0, y), (self.width, y), 1)
    
     # ----- Draw the Rnvironment -----
    def draw(self, screen):
        # Draw background grid
        self.draw_background_grid(screen)
        
        # Draw obstacles
        for obs in self.obstacles:
            # Draw shadow (for 3D effect) -- Fine Tuning
            pygame.draw.circle(screen, (200, 200, 200), 
                              (int(obs.x + 5), int(obs.y + 5)), obs.radius)
            # Draw obstacle
            pygame.draw.circle(screen, obs.color, (int(obs.x), int(obs.y)), obs.radius)
            pygame.draw.circle(screen, APP_COLORS.OBSTACLE_BOUNDARY, 
                              (int(obs.x), int(obs.y)), obs.radius, 2)
        
        # Draw target if exists
        if self.target and not self.target.reached:
            # Draw glow effect -- Fine Tuning
            for i in range(3):
                alpha = 100 - i * 30
                glow_radius = self.target.radius + i * 5
                glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*APP_COLORS.TARGET_GLOW, alpha), 
                                 (glow_radius, glow_radius), glow_radius)
                screen.blit(glow_surface, 
                          (self.target.x - glow_radius, self.target.y - glow_radius))
            
            pygame.draw.circle(screen, APP_COLORS.TARGET, 
                              (int(self.target.x), int(self.target.y)), self.target.radius)
            pygame.draw.circle(screen, (255, 255, 255), 
                              (int(self.target.x), int(self.target.y)), self.target.radius, 2)
            
            # Draw target text
            font = pygame.font.Font(None, 20)
            text = font.render("TARGET", True, APP_COLORS.TARGET)
            screen.blit(text, (self.target.x - 30, self.target.y - self.target.radius - 20))
        
        # Draw robot path
        if self.robot and len(self.robot.path) > 1:
            pygame.draw.lines(screen, APP_COLORS.PATH, False, self.robot.path, 2)
        
        # Draw robot
        if self.robot:
            self.robot.draw(screen)