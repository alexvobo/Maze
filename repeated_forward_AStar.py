from heapq import heappop, heappush

import time
import os
import math
G_VALUE = 1


class Node:
    def __init__(self, pos, f=0, g=0, h=0, parent=None):
        self.pos = pos   # type is tuple

        self.f = f
        self.g = g
        self.h = h

        self.parent = parent

    def __repr__(self):
        return repr((self.pos, self.f, self.h, self.g, self.parent))


def forward_astar(maze, start_pos, goal_pos):
    # region time/memory mgmt.
    # process = psutil.Process(os.getpid())
    # mem_before = process.memory_info().rss / 1024 / 1024
    # t1 = time.perf_counter()
    # endregion
    # region A*
    row_bound = len(maze)
    col_bound = len(maze[0])
    start = Node(start_pos)
    # start.h = heuristic(start_pos, goal_pos)
    goal = Node(goal_pos)
    count = 0
    max_iter = (row_bound*col_bound)//2
    # * Step 1: Add starting node to open list
    openList = []
    closedList = []
    heappush(openList, (start.f, start))

    # * Step 2: Repeat...
    while openList:
        count += 1

        # ^ A. Look for lowest f cost square in open list. This is curr_square
        curr_square = heappop(openList)
        # ^ B. Move it to closed list
        closedList.append(curr_square.pos)
        if curr_square.pos in closedList:
            print("goal found, backtracking...")
            return backtrack(curr_square)

        if count > max_iter:
            print("Too many cycles")
            return backtrack(curr_square)

        # ^ C. For each of the 4/8 squares adjacent to current square
        children = []

        adj_pos = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Clockwise around node
        for p in adj_pos:
            # Add current square to one of the adj positions to get new pos
            new_pos = add_positions(curr_square.pos, p)

            # If not within bounds -> ignore
            if new_pos[0] > row_bound-1 or new_pos[0] < 0 or new_pos[1] > col_bound or new_pos[1] < 0:
                continue

            # If not walkable or in closed list -> ignore
            if new_pos in closedList or maze[new_pos[0]][new_pos[1]] == 1:
                continue

            # If not in open list, add it. Make curr square the parent.
            if new_pos not in openList:
                new_node = Node(new_pos, parent=curr_square)
                children.append(new_node)
                #  Record f,g,h costs of square
            else:
                # If already in open list, check if path to that square is a better path
                # -> If path better, change parent of square to curr square, recalc G F scores of square
                pass
        # adj_pos = [(-1, 0), (-1, 1), (0, 1), (1, 1),
        #            (1, 0), (1, -1), (0, -1), (-1, -1)]

        # HEAP: Resort if necessary
        # ^ D. STOP WHEN...
        #! Goal square is in closed list -> path found
        #! Open list is empty -> no path found

    # * Step 3: BACKTRACK. Go from each square to parent square until start pos is reached. That's the path
    # endregion A*

    # region time/memory mgmt.
    # t2 = time.perf_counter()
    # # To check how much memory used
    # mem_after = process.memory_info().rss / 1024 / 1024
    # total_time = t2 - t1
    # print("Before memory: {}MB".format(mem_before))
    # print("After memory: {}MB".format(mem_after))
    # print("Total time: {}second".format(total_time))
    # endregion


def add_positions(pos1, pos2):
    return tuple(map(sum, zip(pos1, pos2)))


def computePath():
    pass


def backtrack(node):
    backtracking = []
    curr = node
    # Go from goal node to start node via parents
    while curr is not None:
        backtracking.append(curr.pos)
        curr = node.parent
    # Reverse the path since we are going from start to goal
    return backtracking[::-1]


def heuristic(start, end):
    # Return manhattan distance
    (x1, y1) = start
    (x2, y2) = end
    return abs(x1 - x2) + abs(y1 - y2)
