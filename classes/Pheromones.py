import pygame
from config import *

class Pheromone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.strength = PHEROMONE_STRENGTH  # Pheromone strength (fades over time)
        self.colour = GREEN

    def decay(self):
        if self.strength > 0:
            self.strength -= 1

    def draw(self, surface):
        #pygame.draw.circle(surface, (0, 0, int(self.strength / PHEROMONE_STRENGTH * 255)), (self.x, self.y), 1)
        pygame.draw.circle(surface, self.colour, (self.x, self.y), 1)

class Pheromone1(Pheromone):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = PHEROMONE_STRENGTH + 100
        self.colour = GREEN

class Pheromone2(Pheromone):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = PHEROMONE_STRENGTH + 200
        self.colour = BLUE

class Pheromone3(Pheromone):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = PHEROMONE_STRENGTH
        self.colour = RED

class Pheromone4(Pheromone):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = PHEROMONE_STRENGTH - 100
        self.colour = YELLOW