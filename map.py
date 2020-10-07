import numpy as np


class Map:
    def __init__(self, GRID_SIZE):
        self.obstacles = [0, 1]
        self.probabilities = [0.7, 0.3]
        self.GRID_SIZE = GRID_SIZE
        self.maze = self.make_maze()

    # Given a probability, generates a 0 or a 1
    def create_obstacle_randomly(self):
        return np.random.choice(self.obstacles, 1, p=self.probabilities)[0]

    # Creates a GRID_SIZE x GRID_SIZE maze of 0,1 using discrete obstacle function
    def make_maze(self):
        grid = [[self.create_obstacle_randomly() for _ in range(self.GRID_SIZE)]
                for _ in range(self.GRID_SIZE)]
        # for x in grid:
        #     print(x)
        return grid
