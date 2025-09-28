import random
from PIL import Image
import base64
from io import BytesIO

def split_image(image, grid_size=3):
    """Split an image into equal square tiles and assign labels 1..N, last one is blank."""
    width, height = image.size
    tile_width = width // grid_size
    tile_height = height // grid_size

    tiles, labels = [], []
    count = 1
    for row in range(grid_size):
        for col in range(grid_size):
            left, upper = col * tile_width, row * tile_height
            right, lower = (col + 1) * tile_width, (row + 1) * tile_height
            tile = image.crop((left, upper, right, lower)).resize((100, 100))
            tiles.append(tile)
            labels.append(count)
            count += 1

    # Last tile = blank
    tiles[-1] = None
    labels[-1] = None
    return tiles, labels

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

def shuffle_board(matrix, shuffle_count=10, grid_size=3):
    """Shuffle the board by making random valid moves."""

    blank_pos = None
    for r in range(grid_size):
        for c in range(grid_size):
            if matrix[r][c] is None:
                blank_pos = (r, c)
                break
        if blank_pos:
            break

    # Shuffle by moving the blank around
    for _ in range(shuffle_count):
        moves = get_neighbors(blank_pos, grid_size)
        r, c = random.choice(moves)
        br, bc = blank_pos
        matrix[br][bc], matrix[r][c] = matrix[r][c], matrix[br][bc]
        blank_pos = (r, c)

    return matrix

def is_solved(matrix, grid_size=3):
    """Check if the puzzle is solved (blank at last)."""
    expected_val = 1
    for r in range(grid_size):
        for c in range(grid_size):
            if r == grid_size-1 and c == grid_size-1:
                if matrix[r][c] is not None:
                    return False
            else:
                if matrix[r][c] != expected_val:
                    return False
                expected_val += 1
    return True

def pil_to_base64(img):
    """Convert PIL image to base64 string for HTML embedding."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()
