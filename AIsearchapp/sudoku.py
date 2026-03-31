import random
import copy
from algorithms import SearchResult
import time


def is_valid_sudoku(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == num:
                return False
    return True


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


def board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def tuple_to_board(t):
    return [list(row) for row in t]


def get_candidates(board, row, col):
    used = set(board[row])
    used |= {board[r][col] for r in range(9)}
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            used.add(board[r][c])
    return [n for n in range(1, 10) if n not in used]


def solve_sudoku_dfs(board_input):
    result = SearchResult()
    start_time = time.time()
    board = copy.deepcopy(board_input)

    stack = [board]
    visited_count = 0

    while stack:
        b = stack.pop()
        visited_count += 1
        result.nodes_explored = visited_count

        empty = find_empty(b)
        if empty is None:
            result.solution = b
            result.success = True
            result.path = [board_input, b]
            result.solution_depth = 81 - sum(1 for r in range(9) for c in range(9) if board_input[r][c] == 0)
            break

        row, col = empty
        candidates = get_candidates(b, row, col)
        for num in reversed(candidates):
            new_b = copy.deepcopy(b)
            new_b[row][col] = num
            stack.append(new_b)

    result.time_taken = time.time() - start_time
    return result


def solve_sudoku_bfs(board_input):
    result = SearchResult()
    start_time = time.time()
    board = copy.deepcopy(board_input)

    from collections import deque
    queue = deque([board])
    visited_count = 0

    while queue:
        b = queue.popleft()
        visited_count += 1
        result.nodes_explored = visited_count

        if visited_count > 50000:
            result.time_taken = time.time() - start_time
            result.success = False
            return result

        empty = find_empty(b)
        if empty is None:
            result.solution = b
            result.success = True
            result.path = [board_input, b]
            result.solution_depth = 81 - sum(1 for r in range(9) for c in range(9) if board_input[r][c] == 0)
            break

        row, col = empty
        candidates = get_candidates(b, row, col)
        for num in candidates:
            new_b = copy.deepcopy(b)
            new_b[row][col] = num
            queue.append(new_b)

    result.time_taken = time.time() - start_time
    return result


def sudoku_heuristic(board):
    """Count remaining empty cells (fewer = closer to goal)."""
    empty_count = sum(1 for r in range(9) for c in range(9) if board[r][c] == 0)
    
    if empty_count == 0:
        return 0
    
    min_candidates = 10
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                cands = get_candidates(board, r, c)
                if len(cands) == 0:
                    return float('inf')  
                min_candidates = min(min_candidates, len(cands))
    
    return empty_count + (min_candidates - 1)


def solve_sudoku_greedy(board_input):
    result = SearchResult()
    start_time = time.time()
    import heapq
    board = copy.deepcopy(board_input)
    counter = [0]
    heap = [(sudoku_heuristic(board), counter[0], board)]
    visited_count = 0

    while heap:
        h, _, b = heapq.heappop(heap)
        visited_count += 1
        result.nodes_explored = visited_count

        if visited_count > 100000:
            result.time_taken = time.time() - start_time
            result.success = False
            return result

        empty = find_empty(b)
        if empty is None:
            result.solution = b
            result.success = True
            result.path = [board_input, b]
            result.solution_depth = 81 - sum(1 for r in range(9) for c in range(9) if board_input[r][c] == 0)
            break

        row, col = empty
        candidates = get_candidates(b, row, col)
        if not candidates:
            continue

        best_cell = (row, col)
        best_cands = candidates
        min_len = len(candidates)
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    cands = get_candidates(b, r, c)
                    if len(cands) < min_len:
                        min_len = len(cands)
                        best_cell = (r, c)
                        best_cands = cands

        br, bc = best_cell
        for num in best_cands:
            new_b = copy.deepcopy(b)
            new_b[br][bc] = num
            h_val = sudoku_heuristic(new_b)
            if h_val != float('inf'):
                counter[0] += 1
                heapq.heappush(heap, (h_val, counter[0], new_b))

    result.time_taken = time.time() - start_time
    return result


def solve_sudoku_astar(board_input):
    result = SearchResult()
    start_time = time.time()
    import heapq
    board = copy.deepcopy(board_input)
    
    initial_empty = sum(1 for r in range(9) for c in range(9) if board[r][c] == 0)
    counter = [0]
    heap = [(sudoku_heuristic(board), counter[0], 0, board)]
    visited_count = 0

    while heap:
        f, _, g, b = heapq.heappop(heap)
        visited_count += 1
        result.nodes_explored = visited_count

        if visited_count > 100000:
            result.time_taken = time.time() - start_time
            result.success = False
            return result

        empty = find_empty(b)
        if empty is None:
            result.solution = b
            result.success = True
            result.path = [board_input, b]
            result.solution_depth = initial_empty
            break

        best_cell = None
        best_cands = None
        min_len = 10

        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    cands = get_candidates(b, r, c)
                    if len(cands) < min_len:
                        min_len = len(cands)
                        best_cell = (r, c)
                        best_cands = cands

        if best_cell is None or not best_cands:
            continue

        br, bc = best_cell
        new_g = g + 1
        for num in best_cands:
            new_b = copy.deepcopy(b)
            new_b[br][bc] = num
            h_val = sudoku_heuristic(new_b)
            if h_val != float('inf'):
                counter[0] += 1
                heapq.heappush(heap, (new_g + h_val, counter[0], new_g, new_b))

    result.time_taken = time.time() - start_time
    return result


def generate_sudoku(difficulty="Medium"):
    """Generate a valid Sudoku puzzle."""
    board = [[0]*9 for _ in range(9)]
    
    def fill_board(b):
        empty = find_empty(b)
        if not empty:
            return True
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if is_valid_sudoku(b, row, col, num):
                b[row][col] = num
                if fill_board(b):
                    return True
                b[row][col] = 0
        return False

    fill_board(board)
    solved = copy.deepcopy(board)

    remove_counts = {"Easy": 30, "Medium": 45, "Hard": 55}
    to_remove = remove_counts.get(difficulty, 45)

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    for r, c in cells:
        if removed >= to_remove:
            break
        val = board[r][c]
        board[r][c] = 0
        removed += 1

    return board, solved


def solve_sudoku(board, algorithm="A*"):
    algo_map = {
        "DFS": solve_sudoku_dfs,
        "BFS": solve_sudoku_bfs,
        "Greedy Best-First": solve_sudoku_greedy,
        "A*": solve_sudoku_astar,
    }
    return algo_map[algorithm](board)
