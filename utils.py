import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pygame

def choose_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    root.destroy()
    return file_path

def load_image(image_path, grid_size, tile_size):
    try:
        img = Image.open(image_path)
        img = img.resize((grid_size * tile_size, grid_size * tile_size))
        image_tiles = []
        for i in range(grid_size):
            for j in range(grid_size):
                box = (j * tile_size, i * tile_size, (j + 1) * tile_size, (i + 1) * tile_size)
                tile = img.crop(box)
                tile = pygame.image.fromstring(tile.tobytes(), tile.size, tile.mode)
                image_tiles.append(tile)
        image_tiles[-1] = None
        return image_tiles, None
    except Exception as e:
        return None, f"Error loading image: {str(e)}"

def is_solvable(flat_board, grid_size, empty_pos):
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] != grid_size * grid_size - 1 and flat_board[j] != grid_size * grid_size - 1:
                if flat_board[i] > flat_board[j]:
                    inversions += 1
    empty_row = empty_pos[0]
    if grid_size % 2 == 1:
        return inversions % 2 == 0
    else:
        return (inversions + empty_row) % 2 == 1

def shuffle_board(board, grid_size, empty_pos):
    flat_board = [num for row in board for num in row]
    random.shuffle(flat_board)
    while not is_solvable(flat_board, grid_size, empty_pos):
        random.shuffle(flat_board)
    idx = 0
    for i in range(grid_size):
        for j in range(grid_size):
            board[i][j] = flat_board[idx]
            if board[i][j] == grid_size * grid_size - 1:
                empty_pos[:] = [i, j]
            idx += 1
    return board, empty_pos
# COPYRIGHT by Perfect Dragon King (PDK)