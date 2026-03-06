import pygame
from src.config import APP_COLORS
from src.models import Obstacle

class HomeEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.target = None
        self.robot = None
    
    def create_living_room_layout(self):
        self.obstacles = [
            Obstacle(300, 200, 80, (139, 69, 19)),  # Sofa
            Obstacle(500, 400, 40, (210, 180, 140)), # Table
            Obstacle(700, 200, 60, (105, 105, 105)), # TV
            Obstacle(150, 500, 30, (34, 139, 34)),   # Plant
        ]
        return self.obstacles
    
    def create_kitchen_layout(self):
        self.obstacles = [
            Obstacle(400, 350, 100, (200, 200, 200)), # Island
            Obstacle(650, 450, 30, (139, 69, 19)),    # Chair
            Obstacle(700, 450, 30, (139, 69, 19)),    # Chair
            Obstacle(200, 150, 50, (255, 255, 255)),  # Fridge
        ]
        return self.obstacles
    
    def create_mixed_home_layout(self):
        self.obstacles = [
            Obstacle(250, 200, 70, (139, 69, 19)),    # Sofa
            Obstacle(450, 150, 40, (105, 105, 105)),  # TV
            Obstacle(700, 300, 60, (200, 200, 200)),  # Island
            Obstacle(200, 550, 50, (100, 149, 237)),  # Bed
            Obstacle(600, 600, 20, (255, 0, 0)),      # Toy
        ]
        return self.obstacles
    
    def draw(self, screen):
        # Draw Obstacles
        for obs in self.obstacles:
            pygame.draw.circle(screen, obs.color, (int(obs.x), int(obs.y)), obs.radius)
        
        # Draw Target
        if self.target and not self.target.reached:
            pygame.draw.circle(screen, APP_COLORS.GREEN, (int(self.target.x), int(self.target.y)), 
                            self.target.radius)
        
        # Draw Robot
        if self.robot:
            self.robot.draw(screen)