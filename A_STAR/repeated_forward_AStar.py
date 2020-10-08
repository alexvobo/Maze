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

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def recalc(self, goal_pos):
        self.g += 1
        self.h = self.heuristic(self.pos, goal_pos)
        self.f = self.g + self.h

    def heuristic(self, start, end):
        # Return manhattan distance
        (x1, y1) = start
        (x2, y2) = end
        return abs(x1 - x2) + abs(y1 - y2)


def inHeap(pos, openList):
    for n in openList:
        if pos == n.pos:
            return True
    return False


def forward_astar(maze, start_pos, goal_pos):
    # region time/memory mgmt.
    # process = psutil.Process(os.getpid())
    # mem_before = process.memory_info().rss / 1024 / 1024
    # t1 = time.perf_counter()
    # endregion
    # region A*
    row_bound, col_bound = len(maze), len(maze[0])
    # we can't assume matrix will be square so we need to factor rows and cols

    start = Node(start_pos)
    # start.h = heuristic(start_pos, goal_pos)
    goal = Node(goal_pos)

    print("Start pos:", start.pos)
    print("Goal pos:", goal.pos)
    # * Step 1: Add starting node to open list
    openList = []
    closedList = []
    heappush(openList, start)
    # * Step 2: Repeat...
    while openList:

        # !  Look for lowest f cost square in open list.
        curr_square = heappop(openList)
        # print(curr_square)

        # ! Move it to closed list
        closedList.append(curr_square.pos)

        # Goal square is in closed list -> path found
        if goal_pos in closedList:
            print("goal found, backtracking...")
            return construct_path(curr_square)

        # !  For each of the 4 squares adjacent to current square...

        adj_pos = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Clockwise around node

        # Create the new search positions. we will filter them in the loop
        successors = list(
            map(lambda p: add_positions(curr_square.pos, p), adj_pos))

        for succ in successors:
            # If not within bounds -> ignore
            if succ[0] >= row_bound or succ[0] < 0 or succ[1] >= col_bound or succ[1] < 0:
                continue
            # If not walkable -> ignore
            if maze[succ[0]][succ[1]] == 1:
                continue
            # If in closed list or open list -> ignore
            if succ in closedList or inHeap(succ, openList):
                continue

            # Make curr square the parent.
            new_node = Node(succ, parent=curr_square)
            #  Calculate costs of square
            new_node.recalc(goal_pos)
            # Add square to open list
            heappush(openList, new_node)

        # adj_pos = [(-1, 0), (-1, 1), (0, 1), (1, 1),
        #            (1, 0), (1, -1), (0, -1), (-1, -1)]
    # Open list is empty -> no path found
    print("Path not found")
    return []
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


def construct_path(node):
    path = []
    curr = node

    # Go from goal node to start node via parents
    while curr is not None:
        path.insert(0, curr.pos)
        curr = curr.parent

    return path
