import heapq
import time
from collections import deque
from typing import Any, Callable, List, Optional, Tuple, Dict


class SearchResult:
    def __init__(self):
        self.solution = None
        self.path = []
        self.nodes_explored = 0
        self.time_taken = 0.0
        self.solution_depth = 0
        self.success = False


def dfs(start, goal_test, get_neighbors, heuristic=None, max_depth=1000):
    result = SearchResult()
    start_time = time.time()

    stack = [(start, [start])]
    visited = set()
    visited.add(str(start))

    while stack:
        state, path = stack.pop()
        result.nodes_explored += 1

        if goal_test(state):
            result.solution = state
            result.path = path
            result.solution_depth = len(path) - 1
            result.success = True
            break

        if len(path) >= max_depth:
            continue

        for neighbor in reversed(get_neighbors(state)):
            key = str(neighbor)
            if key not in visited:
                visited.add(key)
                stack.append((neighbor, path + [neighbor]))

    result.time_taken = time.time() - start_time
    return result


def bfs(start, goal_test, get_neighbors, heuristic=None):
    result = SearchResult()
    start_time = time.time()

    queue = deque([(start, [start])])
    visited = set()
    visited.add(str(start))

    while queue:
        state, path = queue.popleft()
        result.nodes_explored += 1

        if goal_test(state):
            result.solution = state
            result.path = path
            result.solution_depth = len(path) - 1
            result.success = True
            break

        for neighbor in get_neighbors(state):
            key = str(neighbor)
            if key not in visited:
                visited.add(key)
                queue.append((neighbor, path + [neighbor]))

    result.time_taken = time.time() - start_time
    return result


def greedy_bfs(start, goal_test, get_neighbors, heuristic):
    result = SearchResult()
    start_time = time.time()

    counter = [0]
    heap = [(heuristic(start), counter[0], start, [start])]
    visited = set()
    visited.add(str(start))

    while heap:
        h, _, state, path = heapq.heappop(heap)
        result.nodes_explored += 1

        if goal_test(state):
            result.solution = state
            result.path = path
            result.solution_depth = len(path) - 1
            result.success = True
            break

        for neighbor in get_neighbors(state):
            key = str(neighbor)
            if key not in visited:
                visited.add(key)
                counter[0] += 1
                heapq.heappush(heap, (heuristic(neighbor), counter[0], neighbor, path + [neighbor]))

    result.time_taken = time.time() - start_time
    return result


def astar(start, goal_test, get_neighbors, heuristic):
    result = SearchResult()
    start_time = time.time()

    counter = [0]
    g_cost = {str(start): 0}
    heap = [(heuristic(start), counter[0], start, [start])]
    visited = set()

    while heap:
        f, _, state, path = heapq.heappop(heap)
        key = str(state)

        if key in visited:
            continue
        visited.add(key)
        result.nodes_explored += 1

        if goal_test(state):
            result.solution = state
            result.path = path
            result.solution_depth = len(path) - 1
            result.success = True
            break

        g = g_cost.get(key, float('inf'))

        for neighbor in get_neighbors(state):
            nkey = str(neighbor)
            new_g = g + 1
            if new_g < g_cost.get(nkey, float('inf')):
                g_cost[nkey] = new_g
                counter[0] += 1
                f_val = new_g + heuristic(neighbor)
                heapq.heappush(heap, (f_val, counter[0], neighbor, path + [neighbor]))

    result.time_taken = time.time() - start_time
    return result


ALGORITHMS = {
    "DFS": dfs,
    "BFS": bfs,
    "Greedy Best-First": greedy_bfs,
    "A*": astar,
}
