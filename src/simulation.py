import math
import pygame

from src.config import APP_COLORS, WINDOW_WIDTH


def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                self.env.obstacles = []
                self.env.create_mixed_home_layout()
            elif event.key == pygame.K_1:
                self.env.obstacles = []
                self.env.create_living_room_layout()
            elif event.key == pygame.K_2:
                self.env.obstacles = []
                self.env.create_kitchen_layout()
            elif event.key == pygame.K_3:
                self.env.obstacles = []
                self.env.create_bedroom_layout()
            elif event.key == pygame.K_r:
                self.reset_simulation()
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
                
def draw_goal_acheived(self):
    if self.env.target and self.env.target.reached:
        # Draw Text
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.5 + 0.5
        size = int(36 + pulse * 20)
        
        font = pygame.font.Font(None, size)
        text = font.render("TARGET REACHED!", True, APP_COLORS.BRI_GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(text, text_rect)