import pygame

from src.config import APP_COLORS


class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
    
    # ---------- Draw Daashboard ----------
    def draw_dashboard(self, robot, target):

        # Semi-transparent Panel
        panel = pygame.Surface((320, 240))
        panel.set_alpha(200)
        panel.fill((240, 240, 240))
        self.screen.blit(panel, (10, 10))
        
        # Get Robot Status
        y = 20
        title = self.title_font.render("Home Friendly", True, APP_COLORS.NAVY)
        self.screen.blit(title, (20, y))
        y += 35
        
        status = self.font.render(f"Status: {robot.state.value}", True, APP_COLORS.NAVY)
        self.screen.blit(status, (20, y))
        y += 25
        
        pos = self.font.render(f"Position: ({int(robot.x)}, {int(robot.y)})", True, APP_COLORS.NAVY)
        self.screen.blit(pos, (20, y))

        dist_text = self.font.render(f"Distance: {int(robot.total_distance)} px", True, APP_COLORS.NAVY)
        avoid_text = self.font.render(f"Obstacles avoided: {robot.obstacles_avoided}", True, APP_COLORS.NAVY)