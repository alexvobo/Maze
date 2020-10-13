import numpy as np
import os


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


def generate_maze(count, size):
    # Check if mazes folder exists. If not, create it.
    path = 'saved_mazes'
    if not os.path.exists(path):
        os.makedirs(path)

    # Creates NUM_MAZES mazes and saves them in mazes directory
    for i in range(count):
        map_obj = Map(size)
        with open(os.path.join(path, "maze_" + str(size)+"_" + str(i) + ".txt"), 'w') as file:
            maze = map_obj.maze
            file.write(str(maze))
