from heapq import heappop, heappush

import math


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

    def recalc(self, goal_pos, new_g):
        self.g = math.dist(new_g, self.pos)
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
    row_bound, col_bound = len(maze), len(maze[0])
    # we can't assume matrix will be square so we need to factor rows and cols

    start = Node(start_pos)
    # start.h = heuristic(start_pos, goal_pos)
    goal = Node(goal_pos)
    count = 0
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
        count += 1
        # ! Move it to closed list
        closedList.append(curr_square.pos)

        # Goal square is in closed list -> path found
        if goal_pos in closedList:
            print("goal found, finding shortest path...")
            shortest_path = construct_path(curr_square)
            backtracking = list_difference(closedList, shortest_path)
            return shortest_path, backtracking

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
            new_node.recalc(goal_pos, start_pos)
            # Add square to open list
            heappush(openList, new_node)

        # adj_pos = [(-1, 0), (-1, 1), (0, 1), (1, 1),
        #            (1, 0), (1, -1), (0, -1), (-1, -1)]
    # Open list is empty -> no path found
    print("Path not found")
    return [], []
# * Step 3: BACKTRACK. Go from each square to parent square until start pos is reached. That's the path


def add_positions(pos1, pos2):
    return tuple(map(sum, zip(pos1, pos2)))


def list_difference(a, b):
    # We dont have any duplicates in our list so converting to set wont change anything
    return list(set(a)-set(b))


def construct_path(node):
    path = []
    curr = node

    # Go from goal node to start node via parents
    while curr is not None:
        path.insert(0, curr.pos)
        curr = curr.parent

    return path
