import random
from algorithms import dfs, bfs, greedy_bfs, astar, SearchResult


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def get_blank(state):
    return state.index(0)


def get_neighbors_8puzzle(state):
    neighbors = []
    blank = get_blank(state)
    row, col = divmod(blank, 3)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = list(state)
            new_pos = nr * 3 + nc
            new_state[blank], new_state[new_pos] = new_state[new_pos], new_state[blank]
            neighbors.append(tuple(new_state))
    return neighbors


def goal_test_8puzzle(state):
    return state == GOAL_STATE


def manhattan_distance(state):
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_pos = val - 1
        curr_row, curr_col = divmod(i, 3)
        goal_row, goal_col = divmod(goal_pos, 3)
        dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return dist


def misplaced_tiles(state):
    return sum(1 for i, val in enumerate(state) if val != 0 and val != GOAL_STATE[i])


def is_solvable(state):
    flat = [x for x in state if x != 0]
    inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])
    return inversions % 2 == 0


def generate_random_puzzle(difficulty="Medium"):
    steps = {"Easy": 10, "Medium": 25, "Hard": 50}
    n = steps.get(difficulty, 25)
    state = list(GOAL_STATE)
    for _ in range(n * 10):
        neighbors = get_neighbors_8puzzle(tuple(state))
        state = list(random.choice(neighbors))
    return tuple(state)


def solve_8puzzle(initial_state, algorithm="A*"):
    algo_map = {
        "DFS": lambda s, gt, gn, h: dfs(s, gt, gn, h, max_depth=50),
        "BFS": bfs,
        "Greedy Best-First": greedy_bfs,
        "A*": astar,
    }
    fn = algo_map[algorithm]
    return fn(initial_state, goal_test_8puzzle, get_neighbors_8puzzle, manhattan_distance)


def state_to_grid(state):
    return [list(state[i*3:(i+1)*3]) for i in range(3)]
