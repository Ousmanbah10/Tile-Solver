# a_star.py
import heapq
import streamlit as st

def get_neighbors(pos, grid_size=3):
    """Return valid neighbors of the blank tile (up, down, left, right)."""
    row, col = pos
    moves = []
    if row > 0:
        moves.append((row-1, col))  # Up
    if row < grid_size-1:
        moves.append((row+1, col))  # Down
    if col > 0:
        moves.append((row, col-1))  # Left
    if col < grid_size-1:
        moves.append((row, col+1))  # Right
    return moves

def matrix_to_tuple(matrix):
    """Convert matrix (list of lists) -> tuple of tuples (hashable)."""
    return tuple(tuple(row) for row in matrix)

def tuple_to_matrix(state):
    """Convert tuple of tuples -> list of lists (editable)."""
    return [list(row) for row in state]

def manhattan_distance(state, goal, grid_size=3):
    """Heuristic: Manhattan distance of all tiles to their goal positions."""
    dist = 0
    # Create goal position mapping
    pos = {}
    for r in range(grid_size):
        for c in range(grid_size):
            val = goal[r][c]
            if val is not None:
                pos[val] = (r, c)
    
    # Calculate Manhattan distance for each tile
    for r in range(grid_size):
        for c in range(grid_size):
            val = state[r][c]
            if val is not None and val in pos:
                gr, gc = pos[val]
                dist += abs(r - gr) + abs(c - gc)
    return dist

def find_blank(state, grid_size=3):
    """Locate the blank (None) tile in a given state."""
    for r in range(grid_size):
        for c in range(grid_size):
            if state[r][c] is None:
                return r, c
    return None

def a_star(start_matrix, goal_matrix, grid_size=3):
    """A* search to solve sliding puzzle.
    Returns a list of states from start -> goal.
    """
    start_state = matrix_to_tuple(start_matrix)
    goal_state = matrix_to_tuple(goal_matrix)
    
    # Priority queue: (f_score, counter, state)
    open_set = []
    counter = 0
    heapq.heappush(open_set, (0, counter, start_state))
    
    # Track the path
    came_from = {start_state: None}
    
    # Cost from start to current node
    g_score = {start_state: 0}
    
    while open_set:
        current_f, _, current_state = heapq.heappop(open_set)
        
        if current_state == goal_state:
            # Reconstruct path
            path = []
            while current_state is not None:
                path.append(tuple_to_matrix(current_state))
                current_state = came_from[current_state]
            return path[::-1]  # Reverse to get start->goal
        
        # Find blank position in current state
        blank_row, blank_col = find_blank(current_state, grid_size)
        
        # Get possible moves
        neighbors = get_neighbors((blank_row, blank_col), grid_size)
        
        for neighbor_row, neighbor_col in neighbors:
            # Create new state by swapping blank with neighbor
            new_matrix = tuple_to_matrix(current_state)
            new_matrix[blank_row][blank_col], new_matrix[neighbor_row][neighbor_col] = \
                new_matrix[neighbor_row][neighbor_col], new_matrix[blank_row][blank_col]
            
            new_state = matrix_to_tuple(new_matrix)
            tentative_g_score = g_score[current_state] + 1
            
            if new_state not in g_score or tentative_g_score < g_score[new_state]:
                # This path to neighbor is better than any previous one
                came_from[new_state] = current_state
                g_score[new_state] = tentative_g_score
                f_score = tentative_g_score + manhattan_distance(new_state, goal_state, grid_size)
                
                counter += 1
                heapq.heappush(open_set, (f_score, counter, new_state))
    
    return None  # No solution found

def get_move_sequence(solution_path, grid_size=3):
    """Convert solution path to list of coordinate moves."""
    if not solution_path or len(solution_path) < 2:
        return []
    
    moves = []
    for i in range(len(solution_path) - 1):
        current_state = solution_path[i]
        next_state = solution_path[i + 1]
        
        # Find blank position in current state
        blank_r, blank_c = find_blank(current_state, grid_size)
        
        # Find blank position in next state
        new_blank_r, new_blank_c = find_blank(next_state, grid_size)
        
        # The move is from new_blank position to old_blank position
        moves.append(f"({new_blank_r},{new_blank_c}) → ({blank_r},{blank_c})")
    
    return moves

def solve_with_astar():
    """
    Simple function to solve current puzzle and display results.
    Uses the current matrix from session state.
    """
    # Get current matrix from session state
    current_matrix = st.session_state.backend_matrix
    grid_size = 3
    
    # Define goal state
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    
    # Check if already solved
    if current_matrix == goal_state:
        st.success("✅ **Puzzle is already solved!**")
        return
    
    # Run A* algorithm
    with st.spinner("🧠 Running A* algorithm..."):
        solution_path = a_star(current_matrix, goal_state, grid_size)
    
    # Display results
    if solution_path:
        num_moves = len(solution_path) - 1
        st.success(f"**Solution found in {num_moves} moves:**")
        
        # Get move sequence
        moves = get_move_sequence(solution_path, grid_size)
        
        # Display moves as simple text
        for i, move in enumerate(moves, 1):
            st.write(f"**Move {i}:** {move}")
        
    else:
        st.error("No solution found!")