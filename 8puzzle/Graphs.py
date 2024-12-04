import random
import heapq
import math
import time
import matplotlib.pyplot as plt

goal_State = [[0,1,2], [3,4,5], [6,7,8]]
class State:
    def __init__(self, board):
        self.board = board
        self.zerpos = self.get_zero_position()

    def get_possible_moves(self):
        directions = {
            (-1, 0): "up", 
            (1, 0): "down", 
            (0, -1): "left", 
            (0, 1): "right"
        }
        x, y = self.get_zero_position()
        moves = []
        for d, name in directions.items():
            if 0 <= x + d[0] < 3 and 0 <= y + d[1] < 3:
                moves.append((d, name))
        return moves

    def get_zero_position(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def apply_move(self, move):
        direction, name = move
        x, y = self.get_zero_position()
        new_board = [row[:] for row in self.board]
        new_board[x][y], new_board[x + direction[0]][y + direction[1]] = new_board[x + direction[0]][y + direction[1]], new_board[x][y]
        return State(new_board), name

    def is_goal(self):
        return self.board == goal_State

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        return self.board == other.board

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action  # Store move name here (up, down, left, right)
        self.cost = cost # g(n)
        self.depth = depth
        self.heuristic = heuristic  # h(n)

    def total_cost(self):
        return self.cost + self.heuristic # f(n) = g(n) + h(n)
    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        path.reverse()  # Reverse to get actions from start to goal
        return path
    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

def bfs_with_metrics(initial_state):
    start_time = time.time()
    queue = [Node(initial_state)]
    visited = set()
    nodes_expanded = 0

    while queue:
        current_node = queue.pop(0)
        current_state = current_node.state
        nodes_expanded += 1

        if current_state.is_goal():
            end_time = time.time()
            print_metrics(current_node.get_path(), nodes_expanded, current_node.depth, start_time, end_time)
            return current_node.get_path()

        visited.add(current_state)

        for move in current_state.get_possible_moves():
            new_state, move_name = current_state.apply_move(move)
            if new_state not in visited:
                queue.append(Node(new_state, current_node, move_name, current_node.cost, current_node.depth + 1))

    end_time = time.time()
    print_metrics(None, nodes_expanded,0, start_time, end_time) 
    return None


def dfs_with_metrics(initial_state):
    start_time = time.time()
    stack = [Node(initial_state)]
    visited = set()
    nodes_expanded = 0
    dfsdepth = 0  # Initialize dfsdepth

    while stack:
        current_node = stack.pop()
        current_state = current_node.state
        nodes_expanded += 1

        # Update max_depth if the current node's depth is greater
        if current_node.depth > dfsdepth:
            dfsdepth = current_node.depth

        if current_state.is_goal():
            end_time = time.time()
            print_metrics(current_node.get_path(), nodes_expanded, dfsdepth, start_time, end_time)
            return current_node.get_path()

        visited.add(current_state)

        for move in current_state.get_possible_moves():
            new_state, move_name = current_state.apply_move(move)
            if new_state not in visited:
                stack.append(Node(new_state, current_node, move_name, current_node.cost, current_node.depth + 1))

    end_time = time.time()
    print_metrics(None, nodes_expanded, dfsdepth, start_time, end_time)
    return None


def ids_with_metrics(initial_state):
    start_time = time.time()
    depth_limit = 0
    nodes_expanded = 0

    while True:
        stack = [Node(initial_state)]
        visited = set()
        found_solution = False

        while stack:
            current_node = stack.pop()
            current_state = current_node.state
            nodes_expanded += 1

            if current_state.is_goal():
                end_time = time.time()
                print_metrics(current_node.get_path(), nodes_expanded, current_node.depth, start_time, end_time)
                return current_node.get_path()

            visited.add(current_state)

            if current_node.depth < depth_limit:
                for move in current_state.get_possible_moves():
                    new_state, move_name = current_state.apply_move(move)
                    if new_state not in visited:
                        stack.append(Node(new_state, current_node, move_name, current_node.cost, current_node.depth + 1))

        depth_limit += 1

def manhattan_heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                goal_row = (state.board[i][j]) // 3
                goal_col = (state.board[i][j]) % 3
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def eclidean_heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                goal_row = (state.board[i][j]) // 3
                goal_col = (state.board[i][j]) % 3
                distance += math.sqrt((i - goal_row) ** 2 + (j - goal_col) ** 2) 
    return distance
def a_star_with_metrics(initial_state, heuristic):
    start_time = time.time()
    open_list = []
    closed_list = set()
    start_node = Node(initial_state)
    heapq.heappush(open_list, (start_node.total_cost(), start_node))
    nodes_expanded = 0

    while open_list:
        current_node = heapq.heappop(open_list)[1]
        current_state = current_node.state
        nodes_expanded += 1

        if current_state.is_goal():
            end_time = time.time()
            print_metrics(current_node.get_path(), nodes_expanded, current_node.depth, start_time, end_time)
            return current_node.get_path()

        closed_list.add(current_state)

        for move in current_state.get_possible_moves():
            new_state, move_name = current_state.apply_move(move)
            if new_state in closed_list:
                continue

            new_cost = current_node.cost + 1  # Assuming cost of 1 for each move
            new_heuristic = heuristic(new_state)
            new_node = Node(new_state, current_node, move_name, new_cost, current_node.depth + 1, new_heuristic)

            # Check if new state is already in open list with a higher f_score
            if any(new_state == node[1].state and new_node.total_cost() >= node[0] for node in open_list):
                continue

            heapq.heappush(open_list, (new_node.total_cost(), new_node))

    end_time = time.time()
    print_metrics(None, nodes_expanded, 0, start_time, end_time)
    return None

def is_solvable(board):
    # Flatten the board and count inversions
    flat_board = [num for row in board for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])
    return inversions % 2 == 0


def generate_initial_board():
    while True:
        numbers = list(range(9))
        random.shuffle(numbers)
        board = [numbers[i:i+3] for i in range(0, 9, 3)]
        if is_solvable(board):
            return board
        
running_times = []
No_Of_Nodes=[]
costs_of_paths=[]
depths=[]


def print_metrics(path, nodes_expanded, search_depth, start_time, end_time):
    running_time = end_time - start_time
    if path is not None:
        print("Path to goal:", path)
        print("Cost of path:", len(path))
        print("Nodes expanded:", nodes_expanded)
        print("Search depth:", search_depth)
        print("Running time:", running_time, "seconds")
    else:
        print("No solution found.")
        print("Nodes expanded:", nodes_expanded)
        print("Running time:",running_time, "seconds")
    
    running_times.append(running_time) 
    No_Of_Nodes.append(nodes_expanded)
    costs_of_paths.append(len(path))  
    depths.append(search_depth)



        

initial_board =  generate_initial_board()
initial_state = State(initial_board)
print("Initial Board:")
for row in initial_board:
    print(row)

# Run searches with metrics
print("\nBFS:")
bfs_with_metrics(initial_state)

print("\nDFS:")
dfs_with_metrics(initial_state)

print("\nIDFS:")
ids_with_metrics(initial_state)

print("\nA* with Manhattan Heuristic:")
a_star_with_metrics(initial_state, manhattan_heuristic)

print("\nA* with Euclidean Heuristic:")
a_star_with_metrics(initial_state, eclidean_heuristic)  

algorithms = ["BFS", "DFS", "IDFS", "A* (Manhattan)", "A* (Euclidean)"]



# Plotting the running times
if running_times:
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, running_times, color='skyblue')
    plt.xlabel("Search Algorithms")
    plt.ylabel("Running Time (seconds)")
    plt.title("Running Time Comparison of Search Algorithms")
    plt.show()
else:
    print("Running times data is missing.")

# Plotting Number of Nodes Expanded
if No_Of_Nodes:
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, No_Of_Nodes, color='lightcoral')
    plt.xlabel("Search Algorithms")
    plt.ylabel("Number of Nodes Expanded")
    plt.title("Nodes Expanded by Search Algorithms")
    plt.show()
else:
    print("Nodes expanded data is missing.")

# Plotting Search Depths
if depths:
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, depths, color='lightgreen')
    plt.xlabel("Search Algorithms")
    plt.ylabel("Search Depth")
    plt.title("Search Depth Comparison of Search Algorithms")
    plt.show()
else:
    print("Depths data is missing.")

# Plotting Cost of Paths
if costs_of_paths:
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, costs_of_paths, color='lightblue')
    plt.xlabel("Search Algorithms")
    plt.ylabel("Cost of Path")
    plt.title("Cost of Path Comparison of Search Algorithms")
    plt.show()
else:
    print("Costs of paths data is missing.")




