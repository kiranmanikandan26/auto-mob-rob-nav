# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Create, Initialize and Control the robot. Only robot's methods are present in this class.
# Last Modifide Date : 28-03-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import math
import pygame
from .config import *
from .models import RobotState

class HomeRobot:
    def __init__(self, x, y, name="Buddy"):
        # ----- Initialize the robot at start -----
        self.x = x
        self.y = y
        self.name = name
        self.angle = 0
        self.speed = 0
        self.turn_rate = 0
        
        # ----- State -----
        self.state = RobotState.SEARCHING
        self.path = []
        self.sensor_readings = [SENSOR_RANGE] * len(SENSOR_ANGLES)
        self.closest_obstacle_dist = float('inf')
        self.closest_obstacle_angle = 0
        
        # ----- Performance metrics -----
        self.total_distance = 0
        self.obstacles_avoided = 0
        self.steps = 0
        self.collision_warning = False
        
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            # ----- Calculate distance between robot and obstacle -----
            dx = self.x - obstacle.x
            dy = self.y - obstacle.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # ----- Check for overlapping -----
            if distance < ROBOT_RADIUS + obstacle.radius:
                return True, obstacle
        
        return False, None
    
    def sense(self, obstacles):
        self.sensor_readings = []
        min_dist = SENSOR_RANGE
        min_angle = 0
        
        for sensor_angle in SENSOR_ANGLES:
            # ----- Calculate sensor direction -----
            sensor_rad = math.radians(sensor_angle)
            ray_angle = self.angle + sensor_rad
            
            # ----- Find closest obstacle using Ray Cast -----
            closest_dist = SENSOR_RANGE
            
            for obstacle in obstacles:
                # ----- Vector from robot to obstacle -----
                dx = obstacle.x - self.x
                dy = obstacle.y - self.y
                dist_to_center = math.sqrt(dx*dx + dy*dy)
                angle_to_obstacle = math.atan2(dy, dx)
                
                # ----- Angular difference between ray and direction to obstacle -----
                angle_diff = abs(angle_to_obstacle - ray_angle)
                normalized_angle = normalize_angle(angle_diff)
                angle_diff = abs(normalized_angle)
                
                # ----- If ray points roughly toward obstacle (within 30 degrees) -----
                if angle_diff < math.radians(30):
                    dist_to_edge = dist_to_center - obstacle.radius
                    if 0 < dist_to_edge < closest_dist:
                        closest_dist = dist_to_edge
            
            self.sensor_readings.append(closest_dist)
            
            # ----- Track the closest obstacle overall -----
            if closest_dist < min_dist:
                min_dist = closest_dist
                min_angle = sensor_angle
        
        self.closest_obstacle_dist = min_dist
        self.closest_obstacle_angle = min_angle
        
        # ----- Check for collision -----
        self.collision_warning = min_dist < SAFE_DISTANCE
        
        return self.sensor_readings
    
    def decide_action(self, target, obstacles):
        collision, collided_obstacle = self.check_collision(obstacles)
        if collision:
            dx = self.x - collided_obstacle.x
            dy = self.y - collided_obstacle.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                overlap = ROBOT_RADIUS + collided_obstacle.radius - distance
                if overlap > 0:
                    dx /= distance
                    dy /= distance
                    self.x += dx * overlap * 1.1
                    self.y += dy * overlap * 1.1
            self.state = RobotState.AVOIDING
            self.obstacles_avoided += 1
            return
        
        # ----- Get sensor readings -----
        distances = self.sense(obstacles)
        
        # ----- Calculate angle to target -----
        dx = target.x - self.x
        dy = target.y - self.y
        dist_to_target = math.sqrt(dx*dx + dy*dy)

        if dist_to_target < target.radius + ROBOT_RADIUS:
            self.state = RobotState.TARGET_REACHED
            target.reached = True
            self.speed = 0
            return
        
        target_angle = math.atan2(dy, dx)

        angle_diff = target_angle - self.angle
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # ----- Weight sensors by distance -----
        weights = []
        for i, dist in enumerate(distances):
            if dist < SAFE_DISTANCE * 1.5:
                weight = (SAFE_DISTANCE * 2 - dist) / SAFE_DISTANCE
                weight = max(0, min(1, weight))
            else:
                weight = 0
            weights.append(weight)
        
        # ----- Calculate avoidance and steer -----
        avoidance_turn = 0
        total_weight = sum(weights)
        
        # ----- Weighted average of sensor angles -----
        if total_weight > 0:
            for i, (angle, weight) in enumerate(zip(SENSOR_ANGLES, weights)):
                turn_direction = -math.radians(angle) / math.radians(90)
                avoidance_turn += turn_direction * weight
            
            avoidance_turn /= total_weight

            avoidance_turn *= ROBOT_TURN_SPEED * 3
        
        seeking_turn = 0
        if abs(angle_diff) > 0.05:
            seeking_turn = ROBOT_TURN_SPEED if angle_diff > 0 else -ROBOT_TURN_SPEED
        
        # ----- Combine behaviors with dynamic weighting based on obstacle proximity -----
        if self.closest_obstacle_dist < SAFE_DISTANCE:
            self.state = RobotState.AVOIDING
            self.turn_rate = avoidance_turn * 1.5
            self.speed = ROBOT_MAX_SPEED * 0.4
            self.obstacles_avoided += 1
        elif self.closest_obstacle_dist < SAFE_DISTANCE * 2:
            self.state = RobotState.AVOIDING
            avoid_weight = 1 - (self.closest_obstacle_dist - SAFE_DISTANCE) / SAFE_DISTANCE
            seek_weight = 1 - avoid_weight
            self.turn_rate = (avoidance_turn * avoid_weight + seeking_turn * seek_weight)
            self.speed = ROBOT_MAX_SPEED * 0.7
        else:
            self.state = RobotState.MOVING_TO_TARGET
            self.turn_rate = seeking_turn
            self.speed = ROBOT_MAX_SPEED
    
    def update(self, target, obstacles):
        if self.state == RobotState.TARGET_REACHED:
            return
        
        # ----- Remember previous position for distance tracking -----
        prev_x, prev_y = self.x, self.y
        
        # ----- Decide what to do -----
        self.decide_action(target, obstacles)
        
        # ----- Update angle based on turn rate -----
        self.angle += self.turn_rate
        
        # ----- Update position based on speed and angle -----
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed
        
        # ----- Check if new position would cause collision -----
        would_collide = False
        for obstacle in obstacles:
            dx = new_x - obstacle.x
            dy = new_y - obstacle.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < ROBOT_RADIUS + obstacle.radius:
                would_collide = True
                break
        
        # ----- Only move if no collision predicted -----
        if not would_collide:
            self.x = new_x
            self.y = new_y
        else:
            # ----- Try to slide along obstacle in negative case -----
            self.turn_rate *= 2
            self.speed *= 0.5
        
        # ----- Keep robot within bounds -----
        self.x = max(ROBOT_RADIUS, min(WINDOW_WIDTH - ROBOT_RADIUS, self.x))
        self.y = max(ROBOT_RADIUS, min(WINDOW_HEIGHT - ROBOT_RADIUS, self.y))
        
        self.total_distance += math.sqrt((self.x - prev_x)**2 + (self.y - prev_y)**2)
        if self.steps % 5 == 0:
            self.path.append((self.x, self.y))
            if len(self.path) > 500:
                self.path.pop(0)
        
        self.steps += 1
    
    def draw(self, screen):
        if self.collision_warning:
            pygame.draw.circle(screen, (255, 200, 200), 
                             (int(self.x), int(self.y)), SAFE_DISTANCE, 2)
        
        # ----- Draw sensor rays -----
        for i, sensor_angle in enumerate(SENSOR_ANGLES):
            if i < len(self.sensor_readings):
                ray_angle = self.angle + math.radians(sensor_angle)
                ray_length = self.sensor_readings[i]
                
                end_x = self.x + math.cos(ray_angle) * ray_length
                end_y = self.y + math.sin(ray_angle) * ray_length

                if ray_length < SAFE_DISTANCE:
                    color = APP_COLORS.COLLISION
                elif ray_length < SAFE_DISTANCE * 2:
                    color = (255, 255, 0)
                else:
                    color = APP_COLORS.SENSOR_RAY
                
                pygame.draw.line(screen, color, (self.x, self.y), (end_x, end_y), 2)
        
        #  ----- Draw robot body with collision warning -----
        if self.collision_warning:
            # Draw warning ring
            pygame.draw.circle(screen, APP_COLORS.COLLISION, 
                             (int(self.x), int(self.y)), ROBOT_RADIUS + 5, 3)
        
        pygame.draw.circle(screen, APP_COLORS.ROBOT, (int(self.x), int(self.y)), ROBOT_RADIUS)
        pygame.draw.circle(screen, APP_COLORS.ROBOT_SENSOR, (int(self.x), int(self.y)), ROBOT_RADIUS, 2)
        
        # ----- Draw direction indicator -----
        eye_offset = ROBOT_RADIUS * 0.5
        eye_x = self.x + math.cos(self.angle) * eye_offset
        eye_y = self.y + math.sin(self.angle) * eye_offset
        
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 5)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)
        
        # ----- Draw robot's name -----
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, APP_COLORS.TEXT)
        screen.blit(text, (self.x - 20, self.y - ROBOT_RADIUS - 20))