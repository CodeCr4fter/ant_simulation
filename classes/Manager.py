from collections import deque
from typing import List, Set, Tuple, Type, Dict
from config import *
from classes.Food import Food
from classes.Pheromones import Pheromone1, Pheromone2, Pheromone3, Pheromone4

class Manager:
    def __init__(self, obj_classes: Dict[str, Type]):
        self.repository: List[List[Set]] = [[set() for _ in range(SPATIAL_PARTITIONING_COLS)] for _ in range(SPATIAL_PARTITIONING_ROWS)]
        self.obj_classes = obj_classes
        self.tile_width = WIDTH // SPATIAL_PARTITIONING_COLS
        self.tile_height = HEIGHT // SPATIAL_PARTITIONING_ROWS

    def checkOverlap(self, sq_R: float, Xc: float, Yc: float, row: int, col: int) -> bool:
        # https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
        X1 = col * self.tile_width
        Y1 = row * self.tile_height
        X2 = (col+1) * self.tile_width
        Y2 = (row+1) * self.tile_height
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

    def check(self, x: float, y: float, sq_radius: float) -> List[Tuple[Set, Tuple[int, int]]]:
        row = y // self.tile_height
        col = x // self.tile_width
        if row >= SPATIAL_PARTITIONING_ROWS:
            row = SPATIAL_PARTITIONING_ROWS - 1
        if col >= SPATIAL_PARTITIONING_COLS:
            col = SPATIAL_PARTITIONING_COLS - 1

        q = deque([(int(row), int(col))])
        checked = set([(row, col)])
        modifications = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        output = []

        while q:
            current_row, current_col = q.popleft()
            if self.checkOverlap(sq_radius, x, y, current_row, current_col):
                output.append((self.repository[current_row][current_col], (current_row, current_col)))
                checked.add((current_row, current_col))

                for mod in modifications:
                    new_tile = (int(current_row + mod[0]), int(current_col + mod[1]))
                    if (new_tile not in checked and
                        new_tile[0] >= 0 and new_tile[0] < SPATIAL_PARTITIONING_ROWS and
                        new_tile[1] >= 0 and new_tile[1] < SPATIAL_PARTITIONING_COLS and
                        self.repository[new_tile[0]][new_tile[1]]):
                        q.append(new_tile)
                        checked.add(new_tile)

        return output

    def add(self, x: float, y: float, obj_type: str = None) -> None:
        row = y // self.tile_height
        col = x // self.tile_width
        if row < SPATIAL_PARTITIONING_ROWS and col < SPATIAL_PARTITIONING_COLS:
            if obj_type:
                self.repository[row][col].add(self.obj_classes[obj_type](x, y))
            else:
                # Default to the first class in obj_classes if no obj_type is specified
                default_class = next(iter(self.obj_classes.values()))
                self.repository[row][col].add(default_class(x, y))

    def remove(self, obj) -> bool:
        row = obj.y // self.tile_height
        col = obj.x // self.tile_width
        if obj in self.repository[row][col]:
            self.repository[row][col].remove(obj)
            return True
        return False

# Initialize managers for food and pheromones
food_manager = Manager({"food": Food})
pheromone_manager = Manager({"Pheromone1": Pheromone1, "Pheromone2": Pheromone2, 
                             "Pheromone3": Pheromone3, "Pheromone4": Pheromone4})
