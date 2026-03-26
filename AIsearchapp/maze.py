import random
from algorithms import dfs, bfs, greedy_bfs, astar


def generate_maze(rows=15, cols=15, seed=None):
    """Generate a maze using recursive backtracking."""
    if seed is not None:
        random.seed(seed)

    # Start with all walls
    maze = [[1] * cols for _ in range(rows)]

    def carve(r, c):
        maze[r][c] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                maze[r + dr//2][c + dc//2] = 0
                carve(nr, nc)

    carve(1, 1)

    # Ensure start and end are open
    maze[1][1] = 0
    maze[rows-2][cols-2] = 0

    # Open a path to end if needed
    maze[rows-2][cols-3] = 0
    maze[rows-3][cols-2] = 0

    return maze


def get_neighbors_maze(state, maze):
    r, c = state
    rows, cols = len(maze), len(maze[0])
    neighbors = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors


def maze_heuristic(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def solve_maze(maze, start, end, algorithm="A*"):
    goal_test = lambda s: s == end
    get_neighbors = lambda s: get_neighbors_maze(s, maze)
    heuristic = lambda s: maze_heuristic(s, end)

    algo_map = {
        "DFS": lambda s, gt, gn, h: dfs(s, gt, gn, h, max_depth=10000),
        "BFS": bfs,
        "Greedy Best-First": greedy_bfs,
        "A*": astar,
    }
    fn = algo_map[algorithm]
    return fn(start, goal_test, get_neighbors, heuristic)
