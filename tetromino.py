import numpy as np

class Tetromino:
    SHAPES = [
        np.array([[1, 1, 1, 1]]),  # I
        np.array([[1, 1], [1, 1]]),  # O
        np.array([[1, 1, 1], [0, 1, 0]]),  # T
        np.array([[1, 1, 0], [0, 1, 1]]),  # Z
        np.array([[0, 1, 1], [1, 1, 0]]),  # S
        np.array([[1, 1, 1], [1, 0, 0]]),  # J
        np.array([[1, 1, 1], [0, 0, 1]])  # L
    ]
    
    TETROMINO_COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (255, 165, 0)     # Orange
    ]


    def __init__(self, shape_index, rotation=0):
        self.shape_index = shape_index
        self.rotation = rotation
        self.color = Tetromino.TETROMINO_COLORS[shape_index]


    @property
    def shape(self):
        return np.rot90(Tetromino.SHAPES[self.shape_index], self.rotation)

    def rotate(self):
        return Tetromino(self.shape_index, (self.rotation + 1) % 4)
