import numpy as np

class Board:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.grid = np.zeros((Board.HEIGHT, Board.WIDTH), dtype=int)

    def is_valid_move(self, tetromino, x, y):
        for dx, dy in np.ndindex(tetromino.shape.shape):
            if tetromino.shape[dx, dy] and (x + dx < 0 or x + dx >= Board.WIDTH or y + dy < 0 or y + dy >= Board.HEIGHT or self.grid[y + dy, x + dx]):
                return False
        return True

    def place(self, tetromino, x, y):
        for dx, dy in np.ndindex(tetromino.shape.shape):
            if tetromino.shape[dx, dy]:
                self.grid[y + dy, x + dx] = tetromino.shape_index + 1

    def clear_lines(self):
        full_lines = np.all(self.grid != 0, axis=1)
        lines_cleared = np.sum(full_lines)
        if lines_cleared:
            self.grid = np.concatenate((np.zeros((lines_cleared, Board.WIDTH), dtype=int), self.grid[~full_lines]))
        return lines_cleared
    
    def is_game_over(self):
        return np.any(self.grid[0] != 0)
    
    def print_board(self):
        for row in self.grid:
            print(''.join(['#' if cell != 0 else '.' for cell in row]))
