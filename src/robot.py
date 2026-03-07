import math

import pygame
from src.config import APP_COLORS, ROBOT_MAX_SPEED, ROBOT_RADIUS, ROBOT_TURN_SPEED, SAFE_DISTANCE, SENSOR_ANGLES, SENSOR_RANGE
from src.models import RobotState


class HomeRobot:

     # ---------- Robot Initialization ----------
    def __init__(self, x, y, name="myRobot"):
        self.x = x
        self.y = y
        self.name = name
        self.angle = 0
        self.speed = 0
        self.turn_rate = 0
        self.state = RobotState.SEARCHING
        self.path = []
        self.steps = 0
        self.total_distance = 0
        self.obstacles_avoided = 0
        
    # ---------- Robot Movement ----------
    def update(self, target, obstacles):
        # Store previous position
        prev_x, prev_y = self.x, self.y
        
        # Check Collision Before Moving
        collision, _ = self.check_collision(obstacles)
        if collision:
            self.state = RobotState.AVOIDING
            self.speed *= 0.5  # Slow down
            return
        
        # Move and Check Collision After Moving
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed
        
        # Only Move if no Collision Predicted
        would_collide = False
        for obstacle in obstacles:
            dx = new_x - obstacle.x
            dy = new_y - obstacle.y
            if math.sqrt(dx * dx + dy * dy) < ROBOT_RADIUS + obstacle.radius:
                would_collide = True
                break
        
        if not would_collide:
            self.x, self.y = new_x, new_y
        
        # Track Total Distance
        self.total_distance += math.sqrt((self.x - prev_x) ** 2 + (self.y - prev_y) ** 2)

        if self.state == RobotState.AVOIDING:
            self.obstacles_avoided += 1

        self.total_distance += math.sqrt((self.x - prev_x) ** 2 + (self.y - prev_y) ** 2)

    # ---------- Sensor Implementation ----------
    def sense(self, obstacles):
        self.sensor_readings = []
        for sensor_angle in SENSOR_ANGLES:
            ray_angle = self.angle + math.radians(sensor_angle)
            closest_dist = SENSOR_RANGE
            
            for obstacle in obstacles:
                dx = obstacle.x - self.x
                dy = obstacle.y - self.y
                dist_to_center = math.sqrt(dx * dx + dy * dy)
                
                angle_to_obstacle = math.atan2(dy, dx)
                angle_diff = abs(angle_to_obstacle - ray_angle)
                
                if angle_diff < math.radians(30):
                    dist_to_edge = dist_to_center - obstacle.radius
                    if 0 < dist_to_edge < closest_dist:
                        closest_dist = dist_to_edge
            
            self.sensor_readings.append(closest_dist)
        return self.sensor_readings
    
    # ---------- Check for Obstacles and Collision ----------
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            dx = self.x - obstacle.x
            dy = self.y - obstacle.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < ROBOT_RADIUS + obstacle.radius:
                return True, obstacle
        
        return False, None
    
    # ---------- Core Decision Making to Avoid Obstacle and Act ----------
    def decide_action(self, target, obstacles):
        # Get Sensor Data
        distances = self.sense(obstacles)
        
        # Calculate Target Direction
        dx = target.x - self.x
        dy = target.y - self.y
        target_angle = math.atan2(dy, dx)
        angle_diff = target_angle - self.angle
        
        # Weight Sensors by Proximity
        weights = []
        for dist in distances:
            if dist < SAFE_DISTANCE * 1.5:
                weight = (SAFE_DISTANCE * 2 - dist) / SAFE_DISTANCE
                weight = max(0, min(1, weight))
            else:
                weight = 0
            weights.append(weight)
        
        # Calculate Counter Steering
        counter_steer = 0
        total_weight = sum(weights)
        
        if total_weight > 0:
            for i, (angle, weight) in enumerate(zip(SENSOR_ANGLES, weights)):
                turn_direction = -math.radians(angle) / math.radians(90)
                counter_steer += turn_direction * weight
            counter_steer /= total_weight
            counter_steer *= ROBOT_TURN_SPEED * 3
        
        # Calculate Turn
        look_for_turn = 0
        if abs(angle_diff) > 0.05:
            look_for_turn = ROBOT_TURN_SPEED if angle_diff > 0 else -ROBOT_TURN_SPEED
        
        # Act based on obstacle Proximity
        min_dist = min(distances) if distances else SENSOR_RANGE
        
        if min_dist < SAFE_DISTANCE:
            self.turn_rate = counter_steer * 1.5
            self.speed = ROBOT_MAX_SPEED * 0.4
            self.state = RobotState.AVOIDING
        elif min_dist < SAFE_DISTANCE * 2:
            avoid_weight = 1 - (min_dist - SAFE_DISTANCE) / SAFE_DISTANCE
            get_weight = 1 - avoid_weight
            self.turn_rate = counter_steer * avoid_weight + look_for_turn * get_weight
            self.speed = ROBOT_MAX_SPEED * 0.7
            self.state = RobotState.AVOIDING
        else:
            self.turn_rate = look_for_turn
            self.speed = ROBOT_MAX_SPEED
            self.state = RobotState.MOVING_TO_TARGET
        
    # ---------- Draw robot and Configure Direction Indicator ----------
    def draw(self, screen):
        pygame.draw.circle(screen, APP_COLORS.BLUE, (int(self.x), int(self.y)), ROBOT_RADIUS)
        
        eye_x = self.x + math.cos(self.angle) * ROBOT_RADIUS * 0.5
        eye_y = self.y + math.sin(self.angle) * ROBOT_RADIUS * 0.5
        pygame.draw.circle(screen, APP_COLORS.WHITE, (int(eye_x), int(eye_y)), 5)
        pygame.draw.circle(screen, APP_COLORS.BLACK, (int(eye_x), int(eye_y)), 2)

        for i, (angle, dist) in enumerate(zip(SENSOR_ANGLES, self.sensor_readings)):
            ray_angle = self.angle + math.radians(angle)
            end_x = self.x + math.cos(ray_angle) * dist
            end_y = self.y + math.sin(ray_angle) * dist
            
            # Assign Color Based on Distance
            if dist < SAFE_DISTANCE:
                color = APP_COLORS.RED  # Red
            elif dist < SAFE_DISTANCE * 2:
                color = APP_COLORS.YELLOW  # Yellow
            else:
                color = APP_COLORS.ORG_YELLOW  # Yellow-orange
            
            pygame.draw.line(screen, color, (self.x, self.y), (end_x, end_y), 2)
    
        # Draw Path
        if len(self.path) > 1:
            pygame.draw.lines(screen, APP_COLORS.PURPLE, False, self.path, 2)