import pygame

from config import *
from classes.Manager import food_manager, pheromone_manager
from utils import spawn_food
from classes.Nest import Nest1, Nest2, Nest3, Nest4

# Pygame initialization
pygame.init()
clock = pygame.time.Clock()

# Spawning initial food
#spawn_food(food_manager, 480, 150, FOOD_SPAWN_AMOUNT_PER_CLICK * 3)
#spawn_food(food_manager, 480, 930, FOOD_SPAWN_AMOUNT_PER_CLICK * 3)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            spawn_food(food_manager, x, y, FOOD_SPAWN_AMOUNT_PER_CLICK)
    screen.fill(BLACK)
    # Draw pheromones
    for row in pheromone_manager.repository:
        for tile in row:
            for pheromone in tile:
                pheromone.decay()
                if pheromone.strength == 0:
                    pheromone_manager.remove(pheromone)
                    break
                else:
                    pheromone.draw(screen)
  
    Nest1.draw_nest()
    Nest1.move_ants()
    Nest1.draw_ants()

    Nest2.draw_nest()
    Nest2.move_ants()
    Nest2.draw_ants()   

    Nest3.draw_nest()
    Nest3.move_ants()
    Nest3.draw_ants()   

    Nest4.draw_nest()
    Nest4.move_ants()
    Nest4.draw_ants()   

    # Draw food
    for row in food_manager.repository:
        for tile in row:
            for food in tile:
                food.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
