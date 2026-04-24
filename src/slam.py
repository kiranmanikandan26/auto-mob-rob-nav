# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Basic SLAM implementation
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import numpy as np
import math
import pygame
from .config import WINDOW_WIDTH, WINDOW_HEIGHT, exception_handler, ERR_LG_FILES

class ImplementSlam:
    def __init__(self, width, height, cell_size=20):
        try:
            # ----- Initialize grid map -----
            self.cell_size = cell_size
            self.grid_width = width // cell_size
            self.grid_height = height // cell_size
            
            # ----- The map 0 = empty, 1 = obstacle, error or out = -1 -----
            self.grid = np.zeros((self.grid_width, self.grid_height)) - 1
            
            # ----- Robot -----
            # path
            self.trajectory = []
            # metrics
            self.steps = 0
            # obstacles found
            self.obstacles_found = 0
            
            print(f"SLAM initialized: {self.grid_width}x{self.grid_height} grid")
        except Exception as e:
            exception_handler(e, ERR_LG_FILES.SLAM)
    
    def convert_to_grid(self, x, y):
        try:
            # ----- Convert pixel coordinates to grid coordinates -----
            grid_x = int(x // self.cell_size)
            grid_y = int(y // self.cell_size)
            
            # ----- Wrap within grid boundary -----
            grid_x = max(0, min(grid_x, self.grid_width - 1))
            grid_y = max(0, min(grid_y, self.grid_height - 1))
        except Exception as e:
            exception_handler(e, ERR_LG_FILES.SLAM)
        
        return grid_x, grid_y
    
    def update(self, robot_x, robot_y, sensor_readings, sensor_angles, robot_angle):
        try:
            # ----- Update the map with new sensor information -----
            self.trajectory.append((robot_x, robot_y))
            if len(self.trajectory) > 1000:
                self.trajectory.pop(0)
            
            # ----- Mark the robot's current cell as explored -----
            robot_grid_x, robot_grid_y = self.convert_to_grid(robot_x, robot_y)
            if self.grid[robot_grid_x, robot_grid_y] == -1:
                self.grid[robot_grid_x, robot_grid_y] = 0
            
            # ----- Mark obstacles with sensor readings -----
            for i, (distance, sensor_angle) in enumerate(zip(sensor_readings, sensor_angles)):
                if distance >= 120:
                    continue
                
                # ----- Calculate the obstacle -----
                ray_angle = robot_angle + math.radians(sensor_angle)
                obstacle_x = robot_x + math.cos(ray_angle) * distance
                obstacle_y = robot_y + math.sin(ray_angle) * distance
                
                # ----- Mark the obstacle on the grid -----
                obs_grid_x, obs_grid_y = self.convert_to_grid(obstacle_x, obstacle_y)
                
                if self.grid[obs_grid_x, obs_grid_y] != 1:
                    self.grid[obs_grid_x, obs_grid_y] = 1
                    self.obstacles_found += 1
            
            self.steps += 1
        except Exception as e:
            exception_handler(e, ERR_LG_FILES.SLAM)
    
    def get_position_uncertainty(self):
        # ----- Simple estimate of how sure we are about our position -----
        # Had problems with initial control - balance and uncertainty
        if self.steps < 10:
            return 100
        # Now moving more - uncertainty decreases
        return max(10, 100 - self.steps)
    
    def draw(self, screen, show_grid=True):
        try:
            # ----- Draw the map on screen - with BRIGHT colors -----
            if not show_grid:
                return
            
            # ----- Draw grid lines first to appear it behind -----
            for x in range(0, WINDOW_WIDTH, self.cell_size):
                pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, WINDOW_HEIGHT), 1)
            for y in range(0, WINDOW_HEIGHT, self.cell_size):
                pygame.draw.line(screen, (200, 200, 200), (0, y), (WINDOW_WIDTH, y), 1)
            
            # ----- Draw each grid cell with bright colors -----
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    cell_value = self.grid[x, y]
                    
                    # ----- Skip unknown cells -----
                    if cell_value == -1:
                        continue
                    
                    # ----- bright colors for difference -----
                    if cell_value == 1:
                        color = (255, 0, 0, 255)
                        rect = pygame.Rect(
                            x * self.cell_size + 1,
                            y * self.cell_size + 1,
                            self.cell_size - 2,
                            self.cell_size - 2
                        )
                        pygame.draw.rect(screen, color, rect)
                        # ----- Add border -----
                        pygame.draw.rect(screen, (200, 0, 0), rect, 2)
                        
                    elif cell_value == 0:
                        color = (0, 255, 0, 100)
                        rect = pygame.Rect(
                            x * self.cell_size + 1,
                            y * self.cell_size + 1,
                            self.cell_size - 2,
                            self.cell_size - 2
                        )
                        # ----- Create a surface with alpha for transparency -----
                        s = pygame.Surface((self.cell_size-2, self.cell_size-2), pygame.SRCALPHA)
                        s.fill((0, 255, 0, 50))
                        screen.blit(s, (x * self.cell_size + 1, y * self.cell_size + 1))
            
            # ----- Draw the robot's path in bright cyan -----
            if len(self.trajectory) > 1:
                # ----- Draw every point to make it visible -----
                for i in range(1, len(self.trajectory)):
                    start = self.trajectory[i-1]
                    end = self.trajectory[i]
                    pygame.draw.line(screen, (0, 255, 255), start, end, 3)
        except Exception as e:
            exception_handler(e, ERR_LG_FILES.SLAM)
    
    def get_stats(self):
        # ----- Get simple statistics about the map -----
        total_cells = self.grid_width * self.grid_height
        explored_cells = np.sum(self.grid >= 0)
        obstacle_cells = np.sum(self.grid == 1)
        
        return {
            'explored': f"{explored_cells / total_cells * 100:.1f}%",
            'obstacles_found': self.obstacles_found,
            'path_length': len(self.trajectory),
            'uncertainty': self.get_position_uncertainty()
        }