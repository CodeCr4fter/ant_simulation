import pygame

from config import *
from classes.Ant import Ant
from config import screen

class Nest:
    def __init__(self, x, y, colour, nest):
        self.x = x
        self.y = y
        self.nest = nest
        self.location = (self.x, self.y)
        self.ants = [Ant(self.x, self.y, nest) for _ in range(NUM_OF_ANTS)]
        self.food_level = 100
        self.colour = colour

    def draw_nest(self):
        pygame.draw.circle(screen, self.colour, self.location, radius=20)

    def move_ants(self):
        for ant in self.ants:
            ant.move(self.location)

    def draw_ants(self):
        for ant in self.ants:
            ant.draw(screen, self.colour)

Nest1 = Nest(ANTHILL_POINT_1[0], ANTHILL_POINT_1[1], GREEN, "Nest1")
Nest2 = Nest(ANTHILL_POINT_2[0], ANTHILL_POINT_2[1], BLUE, "Nest2")
Nest3 = Nest(ANTHILL_POINT_3[0], ANTHILL_POINT_3[1], RED, "Nest3")
Nest4 = Nest(ANTHILL_POINT_4[0], ANTHILL_POINT_4[1], YELLOW, "Nest4")