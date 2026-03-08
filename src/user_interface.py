import pygame
import math
from .config import APP_COLORS, WINDOW_WIDTH

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        
    def draw_dashboard(self, robot, target, paused, speed_multiplier):
        # ----- Draw status panel -----
        panel = pygame.Surface((320, 280))
        panel.set_alpha(200)
        panel.fill((240, 240, 240))
        self.screen.blit(panel, (10, 10))
        
        # ----- Draw status text -----
        y_offset = 20
        
        # ----- Draw Title -----
        title = self.title_font.render("Home ENV Robot", True, APP_COLORS.TEXT)
        self.screen.blit(title, (20, y_offset))
        y_offset += 35
        
        # ----- Robot status -----
        if robot:
            status_text = self.font.render(
                f"Status: {robot.state.value}", 
                True, APP_COLORS.TEXT)
            self.screen.blit(status_text, (20, y_offset))
            y_offset += 25
            
            # ----- Robot position -----
            pos_text = self.font.render(
                f"Position: ({int(robot.x)}, {int(robot.y)})", 
                True, APP_COLORS.TEXT)
            self.screen.blit(pos_text, (20, y_offset))
            y_offset += 25
            
            # ----- metrics -----
            dist_text = self.font.render(
                f"Distance: {int(robot.total_distance)} px", 
                True, APP_COLORS.TEXT)
            self.screen.blit(dist_text, (20, y_offset))
            y_offset += 25
            
            avoid_text = self.font.render(
                f"Obstacles avoided: {robot.obstacles_avoided}", 
                True, APP_COLORS.TEXT)
            self.screen.blit(avoid_text, (20, y_offset))
            y_offset += 25
            
            # ----- Sensor reading -----
            if robot.closest_obstacle_dist < float('inf'):
                sensor_text = self.font.render(
                    f"Closest obstacle: {int(robot.closest_obstacle_dist)} px", 
                    True, APP_COLORS.TEXT)
                self.screen.blit(sensor_text, (20, y_offset))
                y_offset += 25
            
            steps_text = self.font.render(
                f"Steps: {robot.steps}", 
                True, APP_COLORS.TEXT)
            self.screen.blit(steps_text, (20, y_offset))
            y_offset += 35
            
        # ----- Robot controls -----
        controls = [
            "SPACE: Pause/Resume",
            "R: Reset",
            "↑/↓: Speed",
            "0: Mixed Home",
            "1: Living Room",
            "2: Kitchen",
            "3: Bedroom"
        ]
        
        for control in controls:
            ctrl_text = self.small_font.render(control, True, APP_COLORS.TEXT)
            self.screen.blit(ctrl_text, (20, y_offset))
            y_offset += 18
        
        # ----- Speed indicator -----
        speed_color = (0, 200, 0) if not paused else (200, 0, 0)
        speed_text = self.font.render(
            f"{'▶' if not paused else '⏸'} Speed: {speed_multiplier}x", 
            True, speed_color)
        self.screen.blit(speed_text, (WINDOW_WIDTH - 150, 20))
    
    def draw_target_text(self, target_reached):
        if target_reached:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.5 + 0.5
            size = int(36 + pulse * 20)
            
            font = pygame.font.Font(None, size)
            text = font.render("TARGET REACHED!", True, APP_COLORS.TARGET)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(text, text_rect)