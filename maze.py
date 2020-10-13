import tkinter as tk
from PIL import Image, ImageTk
from map_class import Map
import random
import math

import psutil
import time
import os
import ast
import A_STAR.Repeated_AStar as f_astar
import A_STAR.adaptive_AStar as a_astar


ROWS, COLS = 50, 50

samp = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]
samp_a = (0, 0)
samp_g = (49, 49)


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=ROWS, columns=COLS, size=50, color_unblocked="white", color_blocked="navy", shortest_path='green', color_expanded="red"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color_unblocked = color_unblocked
        self.color_blocked = color_blocked
        self.shortest_path = shortest_path
        self.color_expanded = color_expanded
        self.pieces = {}

        # Create map and log the obstacles
        self.maze = Map(self.rows).maze
        #self.maze = load_map("saved_mazes", "maze_2.txt")
        self.obstacles = self.find_obstacles()

        self.goal_pos = samp_g
        self.agent_pos = samp_a
        # self.goal_pos = self.generate_pos()
        # self.agent_pos = self.generate_pos()

        self.a_star = []
        self.expanded = []
        # self.astar('forward')
        self.astar('forward')

        # region canvas and bindings
        tk.Frame.__init__(self, parent)
        canvas_width = columns * size
        canvas_height = rows * size
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        # this binding will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        # self.canvas.bind("<Enter>", self.astar)
        # endregion

    def find_obstacles(self):
        # Iterate through the maze, if we see objects add (x,y) to the list
        obstacles = []
        for row, _ in enumerate(self.maze):
            for col, cell in enumerate(self.maze[row]):
                if cell == 1:
                    obstacles.append((row, col))
        return obstacles

    def generate_pos(self):
        row = random.randint(0, self.rows-1)
        col = random.randint(0, self.columns-1)

        # invalid positions include obstacles and goal or agent states already added
        invalid_positions = self.obstacles + \
            [val for val in self.pieces.values()]

        # keep generating positions until they are valid
        while (row, col) in invalid_positions:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.columns-1)

        return (row, col)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(
            0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def draw_square(self, x, y, color):
        x2 = x + self.size
        y2 = y + self.size
        self.canvas.create_rectangle(
            x, y, x2, y2, outline="black", fill=color, tags="square")

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")

        for row in range(self.rows):
            for col in range(self.columns):
                x = (col * self.size)
                y = (row * self.size)
                # Walkable regions: color1
                # Blocked regions: color2

                color = self.color_unblocked if self.maze[row][col] == 0 else self.color_blocked

                if (row, col) in self.a_star:
                    color = self.shortest_path

                if (row, col) in self.expanded:
                    color = self.color_expanded
                self.draw_square(x, y, color)

        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def astar(self, event, type='forward'):
        # region time/memory mgmt.
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024
        t1 = time.perf_counter()
        # endregion
        if type == "forward":
            self.a_star, self.expanded = f_astar.forward_astar(
                self.maze, self.agent_pos, self.goal_pos)
        elif type == "backward":
            self.a_star, self.expanded = f_astar.forward_astar(
                self.maze, self.goal_pos, self.agent_pos)
        elif type == "adaptive":
            self.a_star, self.expanded = a_astar.forward_astar(
                self.maze, self.agent_pos, self.goal_pos)
        else:
            print("--Failed. A* Type Invalid--")

        # region time/memory mgmt.
        t2 = time.perf_counter()
        # To check how much memory used
        mem_after = process.memory_info().rss / 1024 / 1024
        total_time = t2 - t1
        print("Before memory: {}MB".format(mem_before))
        print("After memory: {}MB".format(mem_after))
        print("Total time: {}second".format(total_time))
        print("TOTAL EXPANDED:{}\n SHORTEST PATH LEN: {}".format(
            len(self.expanded)+len(self.a_star), len(self.a_star)))
        # endregion

        return

    def print_path(self):
        print(self.a_star)


def generate_image(file_name, size=50):
    width = height = size
    img = Image.open(file_name)
    img = img.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


def load_map(path, fileName):
    # Opens first maze file
    with open(os.path.join(path, fileName), 'r') as file:
        # Gets grid in string form
        grid_str = file.readline()
        # converts string to list of lists
        return ast.literal_eval(grid_str)


if __name__ == "__main__":
    # create the gameboard
    root = tk.Tk()
    root.title('Maze')

    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    # region add game pieces
    piece_size = math.floor(board.size/1.5)

    goal_img = generate_image('imgs/house.png', piece_size)
    board.addpiece("goal", goal_img, *board.goal_pos)

    agent_img = generate_image('imgs/agent.png', piece_size)
    board.addpiece("agent", agent_img, *board.agent_pos)
    # endregion
    # run the app
    root.mainloop()
