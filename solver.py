import heapq
import copy
import time

def a_star(board, empty_pos, grid_size, goal, single_step=False):
    if grid_size > 7:
        return None if single_step else [], {"error": "Grid size too large for A* algorithm. Maximum supported size is 7x7."}
    
    start_time = time.time()
    nodes_expanded = 0
    total_nodes = 0
    MAX_NODES = 10**6

    def heuristic(board):
        distance = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if board[i][j] != grid_size * grid_size - 1:
                    goal_i, goal_j = divmod(board[i][j], grid_size)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def board_to_tuple(board):
        return tuple(tuple(row) for row in board)

    def get_neighbors(board, empty_pos):
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        i, j = empty_pos
        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < grid_size and 0 <= nj < grid_size:
                new_board = [row[:] for row in board]
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                neighbors.append((new_board, [ni, nj]))
        return neighbors

    open_set = [(heuristic(board), 0, copy.deepcopy(board), empty_pos[:], [])]
    closed_set = set()
    goal_tuple = board_to_tuple(goal)

    if board_to_tuple(board) == goal_tuple:
        return [] if not single_step else None, {
            "nodes_expanded": 0,
            "total_nodes": 0,
            "steps": 0,
            "time": 0
        }

    while open_set:
        total_nodes += 1
        if total_nodes > MAX_NODES:
            end_time = time.time()
            return None, {
                "nodes_expanded": nodes_expanded,
                "total_nodes": total_nodes,
                "steps": 0,
                "time": end_time - start_time,
                "error": "A* exceeded node limit"
            }

        f, g, current_board, empty_pos, path = heapq.heappop(open_set)
        current_tuple = board_to_tuple(current_board)

        if current_tuple == goal_tuple:
            end_time = time.time()
            return path, {
                "nodes_expanded": nodes_expanded,
                "total_nodes": total_nodes,
                "steps": len(path),
                "time": end_time - start_time
            }

        if current_tuple in closed_set:
            continue

        closed_set.add(current_tuple)
        nodes_expanded += 1

        for next_board, next_empty in get_neighbors(current_board, empty_pos):
            next_tuple = board_to_tuple(next_board)
            if next_tuple not in closed_set:
                g_new = g + 1
                h = heuristic(next_board)
                f_new = g_new + h
                heapq.heappush(open_set, (f_new, g_new, next_board, next_empty, path + [(next_board, next_empty)]))

    end_time = time.time()
    return None, {
        "nodes_expanded": nodes_expanded,
        "total_nodes": total_nodes,
        "steps": 0,
        "time": end_time - start_time,
        "error": "A* failed to find a solution"
    }
# COPYRIGHT by Perfect Dragon King (PDK)