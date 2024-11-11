import random
import math
import pygame

from config import *
from utils import sq_dist, adjust_colour
from classes.Manager import food_manager, pheromone_manager

class Ant:
    def __init__(self, x, y, nest):
        self.x = x
        self.y = y
        self.nest = nest
        self.speed = ANT_SPEED
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction
        self.has_food = False
        self.food_to_collect = None
        self.food_amount = 0
        self.direction_change_cooldown = 0
        self.pheromone_cooldown = PHEROMONE_COOLDOWN

    def move(self, ANTHILL_POINT):
        if sq_dist((self.x, self.y), ANTHILL_POINT) < ANT_SPEED * 2: # returning food to anthill
            self.has_food = False
            self.food_to_collect = None
            self.food_amount = 0
            self.direction_change_cooldown = 0

        if self.direction_change_cooldown == 0:
            if not self.food_to_collect: # doesn't have direction on food
                for tile, coords in food_manager.check(self.x, self.y, FOOD_DETECTION_RANGE_SQUARED):
                    if not self.food_to_collect:
                        for food in tile:
                            dist_to_food = sq_dist((self.x, self.y), (food.x, food.y))
                            if self.food_amount < MAX_FOOD_AMOUNT and not self.has_food and dist_to_food < FOOD_DETECTION_RANGE_SQUARED:  # Close to food
                                self.direction = self.direction_to_point(food.x, food.y)
                                self.food_to_collect = food
                                break

            if not self.has_food and self.food_to_collect: # has direction on food but doesn't have food yet
                dist_to_food = sq_dist((self.x, self.y), (self.food_to_collect.x, self.food_to_collect.y))
                self.direction = self.direction_to_point(self.food_to_collect.x, self.food_to_collect.y)
                if dist_to_food < FOOD_COLLECTION_RANGE_SQUARED:
                    if food_manager.remove(self.food_to_collect):  # Remove food after it's collected
                        self.food_amount += 1
                        if self.food_amount == MAX_FOOD_AMOUNT:
                            self.has_food = True  # Ant takes the food
                    self.food_to_collect = None

            if not self.food_to_collect and self.has_food:
                self.direction = self.direction_to_point(ANTHILL_POINT[0], ANTHILL_POINT[1]) + random.uniform(-0.5, 0.5)


            if not self.food_to_collect and not self.has_food:
                for tile, coords in pheromone_manager.check(self.x, self.y, PHEROMONE_DETECTION_RANGE_SQUARED):
                    for pheromone in tile:
                        dist_to_pheromone = sq_dist((self.x, self.y), (pheromone.x, pheromone.y))
                        direction_to_pheromone = self.direction_to_point(pheromone.x, pheromone.y)
                        direction_to_anthill = self.direction_to_point(ANTHILL_POINT[0], ANTHILL_POINT[1])
                        if abs(direction_to_pheromone - direction_to_anthill) > math.pi * 0.7 and dist_to_pheromone < PHEROMONE_DETECTION_RANGE_SQUARED:
                            self.direction = self.direction_to_point(pheromone.x, pheromone.y)
                            break
            self.direction_change_cooldown = DIRECTION_CHANGE_COOLDOWN

        self.direction += random.uniform(-RANDOM_ANT_DIRECTION, RANDOM_ANT_DIRECTION)
        if self.has_food:
            if self.pheromone_cooldown == 0:
                if self.nest == "Nest1":
                    pheromone_manager.add(int(self.x), int(self.y), "Pheromone1")  # Leave a pheromone trail
                elif self.nest == "Nest2":
                    pheromone_manager.add(int(self.x), int(self.y), "Pheromone2")  # Leave a pheromone trail                    
                self.pheromone_cooldown = PHEROMONE_COOLDOWN
            else:
                self.pheromone_cooldown -= 1

        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        #if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
        #    self.direction -= math.pi
        if self.x >= WIDTH: # Right wall 
            self.x = WIDTH 
            self.direction = math.pi - self.direction + random.uniform(-0.1, 0.1) 
        elif self.x <= 0: # Left wall 
            self.x = 0 
            self.direction = math.pi - self.direction + random.uniform(-0.1, 0.1) 
        elif self.y >= HEIGHT: # Bottom wall 
            self.y = HEIGHT 
            self.direction = -self.direction + random.uniform(-0.1, 0.1) 
        elif self.y <= 0: # Top wall 
            self.y = 0 
            self.direction = -self.direction + random.uniform(-0.1, 0.1) 
        
        # Update position 
        self.x += self.speed * math.cos(self.direction) 
        self.y += self.speed * math.sin(self.direction) 
        # Wrap angle between 0 and 2π 
        self.direction %= 2 * math.pi
        
        if self.direction_change_cooldown > 0: self.direction_change_cooldown -= 1

    def direction_to_point(self, x, y):
        return math.atan2(y - self.y, x - self.x)
    
    def draw(self, surface, colour):
        color = adjust_colour(colour, 150) if self.has_food else colour
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 3)

#ants = [Ant(ANTHILL_POINT[0], ANTHILL_POINT[1]) for _ in range(NUM_OF_ANTS)]