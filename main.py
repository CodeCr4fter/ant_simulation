from collections import deque

import pygame
import random
import math

# Pygame initialization
pygame.init()

# Screen size
WIDTH, HEIGHT = 960, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

ANTHILL_POINT = (WIDTH // 2, HEIGHT // 2)
PHEROMONE_STRENGTH = 100
ANT_SPEED = 1
NUM_OF_ANTS = 100
PHEROMONE_DETECTION_RANGE_SQUARED = 200 ** 2
FOOD_DETECTION_RANGE_SQUARED = 100 ** 2
FOOD_COLLECTION_RANGE_SQUARED = 10 ** 2
DIRECTION_TOLERANCE = .7

DIRECTION_CHANGE_COOLDOWN = 5
MAX_FOOD_AMOUNT = 1
PHEROMONE_COOLDOWN = 30
FOOD_SPAWN_RANGE = 50
FOOD_SPAWN_AMOUNT_PER_CLICK = 40
SPATIAL_PARTITIONING_COLS = 32
SPATIAL_PARTITIONING_ROWS = 18
def spawn_food(x, y, amount):
    for i in range(amount):
        food_x = random.uniform(x - FOOD_SPAWN_RANGE, x + FOOD_SPAWN_RANGE)
        food_y = random.uniform(y - FOOD_SPAWN_RANGE, y + FOOD_SPAWN_RANGE)
        food_manager.add(int(food_x), int(food_y))

class Manager():
    def __init__(self, obj_class):
        self.repository = [[set() for _ in range(SPATIAL_PARTITIONING_COLS)] for _ in range(SPATIAL_PARTITIONING_ROWS)] # list of sets
        self.obj_class = obj_class
        self.tile_width = WIDTH // SPATIAL_PARTITIONING_COLS
        self.tile_height = HEIGHT // SPATIAL_PARTITIONING_ROWS

    def checkOverlap(self, sq_R, Xc, Yc, row, col):
        # https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
        X1 = col * (WIDTH // SPATIAL_PARTITIONING_COLS)
        Y1 = row * (HEIGHT // SPATIAL_PARTITIONING_ROWS)
        X2 = (col+1) * (WIDTH // SPATIAL_PARTITIONING_COLS)
        Y2 = (row+1) * (HEIGHT // SPATIAL_PARTITIONING_ROWS)
        # check if circle is inside the tile

        # Find the nearest point on the
        # rectangle to the center of
        # the circle
        Xn = max(X1, min(Xc, X2))
        Yn = max(Y1, min(Yc, Y2))

        # Find the distance between the
        # nearest point and the center
        # of the circle
        # Distance between 2 points,
        # (x1, y1) & (x2, y2) in
        # 2D Euclidean space is
        # ((x1-x2)**2 + (y1-y2)**2)**0.5
        Dx = Xn - Xc
        Dy = Yn - Yc

        return (Dx ** 2 + Dy ** 2) <= sq_R
        # returns true if tile overlaps with ant radius, false otherwise
    def check(self, x, y, sq_radius):
        row = y // self.tile_height
        col = x // self.tile_width
        if row >= SPATIAL_PARTITIONING_ROWS:
            row = SPATIAL_PARTITIONING_ROWS - 1
        if col >= SPATIAL_PARTITIONING_COLS:
            col = SPATIAL_PARTITIONING_COLS - 1

        q = deque()
        q.append((int(row), int(col)))
        checked = set()
        checked.add((row, col))
        modifications = ((-1, 0), (0, -1), (1, 0), (0, 1))
        output = []
        while q:
            (row, col) = q.popleft()
            if self.checkOverlap(sq_radius, x, y, row, col):
                output.append((self.repository[row][col], (row, col)))
                checked.add((row, col))

                for mod in modifications:
                    new_tile = (int(row + mod[0]), int(col + mod[1]))
                    # The last condition in the line below isn't really valid, but it improves performance and ants still fulfill their goal, so I decided to leave it.
                    # Just making sure you're aware of that if you decide to play with the code.
                    if new_tile not in checked and new_tile not in q and new_tile[0] >= 0 and new_tile[0] < SPATIAL_PARTITIONING_ROWS and new_tile[1] >= 0 and new_tile[1] <  SPATIAL_PARTITIONING_COLS and self.repository[new_tile[0]][new_tile[1]]:
                        q.append(new_tile)
        return output
        # returns list of sets
    def add(self, x, y):
        row = y // self.tile_height
        col = x // self.tile_width
        if row < SPATIAL_PARTITIONING_ROWS and col < SPATIAL_PARTITIONING_COLS:
            self.repository[row][col].add(self.obj_class(x, y))
    def remove(self, obj):
        row = obj.y // self.tile_height
        col = obj.x // self.tile_width
        if obj in self.repository[row][col]:
            self.repository[row][col].remove(obj)
            return True
        return False



def sq_dist(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
# Ant Class
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = ANT_SPEED
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction
        self.has_food = False
        self.food_to_collect = None
        self.food_amount = 0
        self.direction_change_cooldown = 0
        self.pheromone_cooldown = PHEROMONE_COOLDOWN
    def move(self):
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

        self.direction += random.uniform(-0.2, 0.2)
        if self.has_food:
            if self.pheromone_cooldown == 0:
                pheromone_manager.add(int(self.x), int(self.y))  # Leave a pheromone trail
                self.pheromone_cooldown = PHEROMONE_COOLDOWN
            else:
                self.pheromone_cooldown -= 1

        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            self.direction -= math.pi
        if self.direction_change_cooldown > 0: self.direction_change_cooldown -= 1


    def direction_to_point(self, x, y):
        return math.atan2(y - self.y, x - self.x)
    
    def draw(self, surface):
        color = GREEN if self.has_food else WHITE
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 3)


# Food class
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), 1)


# Pheromone class
class Pheromone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.strength = PHEROMONE_STRENGTH  # Pheromone strength (fades over time)

    def decay(self):
        if self.strength > 0:
            self.strength -= 1
    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, int(self.strength / PHEROMONE_STRENGTH * 255)), (self.x, self.y), 3)

def draw_grid():
    for row in range(SPATIAL_PARTITIONING_ROWS):
        tile_height = HEIGHT // SPATIAL_PARTITIONING_ROWS
        tile_width = WIDTH // SPATIAL_PARTITIONING_COLS
        for col in range(SPATIAL_PARTITIONING_COLS):
            pygame.draw.rect(screen, GRAY, (col * tile_width, row * tile_height, tile_width, tile_height), width=1)

def draw_radius():
    for ant in ants:
        pygame.draw.circle(screen, WHITE, (ant.x, ant.y), radius=math.sqrt(FOOD_DETECTION_RANGE_SQUARED), width=1)
def draw_tile(coords):
    tile_height = HEIGHT // SPATIAL_PARTITIONING_ROWS
    tile_width = WIDTH // SPATIAL_PARTITIONING_COLS
    pygame.draw.rect(screen, GREEN, (coords[1] * tile_width, coords[0] * tile_height, tile_width, tile_height), width=3)



clock = pygame.time.Clock()
food_manager = Manager(Food)
pheromone_manager = Manager(Pheromone)

ants = [Ant(ANTHILL_POINT[0], ANTHILL_POINT[1]) for _ in range(NUM_OF_ANTS)]

# Spawning initial food
spawn_food(480, 150, FOOD_SPAWN_AMOUNT_PER_CLICK * 3)
spawn_food(480, 930, FOOD_SPAWN_AMOUNT_PER_CLICK * 3)



# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            spawn_food(x, y, FOOD_SPAWN_AMOUNT_PER_CLICK)
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

    # Draw frame
    # pygame.draw.rect(screen, WHITE, (0, 0, width, height), width=1)
  
    pygame.draw.circle(screen, YELLOW, ANTHILL_POINT, radius=20)

    # draw_grid()

    # Move and draw ants
    for ant in ants:
        ant.move()
        ant.draw(screen)

    # Draw food
    for row in food_manager.repository:
        for tile in row:
            for food in tile:
                food.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


