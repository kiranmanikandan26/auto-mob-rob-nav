# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Main simulation manager. Handles key controls
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import pygame
import sys
from .config import APP_COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from .environment import HomeEnvironment
from .user_interface import UIManager
from .models import RobotState
from .slam import ImplementSlam

class SimulationManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Home Robot Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.speed_multiplier = 1
        # ----- Slam Implementation -----
        self.slam = ImplementSlam(WINDOW_WIDTH, WINDOW_HEIGHT, cell_size=20)
        self.show_slam = True
        
        # ----- Create environment -----
        self.env = HomeEnvironment(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setup_scenario()
        
        # ----- Create UI manager -----
        self.ui = UIManager(self.screen)
        
    def setup_scenario(self):
        # Create mixed home layout
        self.env.create_mixed_home_layout()
        
        # Place robot at starting position
        self.env.set_robot(100, 100, "Harry")
        
        # Set target at far corner - Kitchen area
        self.env.set_target(850, 600)
        
    def reset_simulation(self):
        self.env = HomeEnvironment(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setup_scenario()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_UP:
                    self.speed_multiplier = min(5, self.speed_multiplier + 0.5)
                elif event.key == pygame.K_DOWN:
                    self.speed_multiplier = max(0.5, self.speed_multiplier - 0.5)
                elif event.key == pygame.K_0:
                    # ----- Scenario 1: Mixed home -----
                    self.env.obstacles = []
                    self.env.create_mixed_home_layout()
                    self.env.set_robot(100, 100, "Harry")
                    self.env.set_target(850, 600)
                elif event.key == pygame.K_1:
                    # ----- Scenario 2: Living room -----
                    self.env.obstacles = []
                    self.env.create_living_room_layout()
                    self.env.set_robot(100, 100, "Harry")
                    self.env.set_target(850, 600)
                elif event.key == pygame.K_2:
                    # ----- Scenario 3: Kitchen -----
                    self.env.obstacles = []
                    self.env.create_kitchen_layout()
                    self.env.set_robot(100, 100, "Harry")
                    self.env.set_target(850, 600)
                elif event.key == pygame.K_3:
                    # ----- Scenario 4: Bedroom -----
                    self.env.obstacles = []
                    self.env.create_bedroom_layout()
                    self.env.set_robot(100, 100, "Harry")
                    self.env.set_target(850, 600)
                elif event.key == pygame.K_s:
                    self.show_slam = not self.show_slam
                    print(f"SLAM display: {'ON' if self.show_slam else 'OFF'}")
    
    def update(self):
        if not self.paused and self.env.robot and self.env.target:
            # ----- Multiple updates per frame for speed multiplier -----
            for _ in range(self.speed_multiplier):
                self.env.robot.update(self.env.target, self.env.obstacles)
                if self.env.robot.state == RobotState.TARGET_REACHED:
                    break
    
    def run(self):
        # ----- Main simulation loop -----
        while self.running:
            self.handle_events()
            self.update()
            # Clear screen - Because it adds it to the actual total
            self.screen.fill(APP_COLORS.BACKGROUND)
            # Draw environment - obstacles, target
            self.env.draw(self.screen)
            
            # ----- Draw SLAM if enabled -----
            if hasattr(self, 'show_slam') and self.show_slam and hasattr(self, 'slam'):
                self.slam.draw(self.screen, show_grid=True)
                # Also draw the stats
                if hasattr(self, 'ui'):
                    self.ui.draw_slam_stats(self.slam)
            
            # ----- Draw dashboard -----
            target_reached = (self.env.target and self.env.target.reached)
            self.ui.draw_dashboard(
                self.env.robot, 
                self.env.target, 
                self.paused, 
                self.speed_multiplier
            )
            self.ui.draw_target_reached(target_reached)
            
            # ----- Update display -----
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()