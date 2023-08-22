import pygame
import random
from tetromino import Tetromino
from board import Board
import numpy as np


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Board.WIDTH * 30, Board.HEIGHT * 30))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_tetromino = Tetromino(random.randint(0, 6))
        self.current_x = Board.WIDTH // 2
        self.current_y = 0
        self.drop_counter = 0
        self.soft_drop_speed = 50  # This means the tetromino will drop every 50 milliseconds when the down key is held.
        self.held_tetromino = None
        self.can_hold = True
        self.bag = list(range(7))
        random.shuffle(self.bag)
        self.bag_index = 0
        self.level = 1
        self.lines_cleared = 0
        self.lines_to_next_level = 10  # for example, level up every 10 lines
        self.drop_speed = 1000 
        self.game_over = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                self.restart_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.board.is_valid_move(self.current_tetromino.rotate(), self.current_x, self.current_y):
                        self.current_tetromino = self.current_tetromino.rotate()
                elif event.key == pygame.K_DOWN:
                    if self.board.is_valid_move(self.current_tetromino, self.current_x, self.current_y + 1):
                        self.current_y += 1
                elif event.key == pygame.K_LEFT:
                    if self.board.is_valid_move(self.current_tetromino, self.current_x - 1, self.current_y):
                        self.current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.board.is_valid_move(self.current_tetromino, self.current_x + 1, self.current_y):
                        self.current_x += 1
                elif event.key == pygame.K_c:
                    if self.can_hold:
                        if not self.held_tetromino:
                            self.held_tetromino = self.current_tetromino
                            self.current_tetromino = self.get_next_tetromino()
                        else:
                            self.current_tetromino, self.held_tetromino = self.held_tetromino, self.current_tetromino
                        self.current_x = Board.WIDTH // 2
                        self.current_y = 0
                        self.can_hold = False
                elif event.key == pygame.K_SPACE:
                    while self.board.is_valid_move(self.current_tetromino, self.current_x, self.current_y + 1):
                        self.current_y += 1  
                    self.place_tetromino()
                    self.can_hold = True

        return True

    def update(self):
        if not self.can_place(self.current_tetromino, self.current_x, self.current_y + 1):
            self.place_tetromino()
            if not self.can_place(self.current_tetromino, self.current_x, self.current_y):
                self.game_over = True
                return
        else:
            self.current_y += 1


    def render(self):
        self.screen.fill((0, 0, 0))
        for x, y in np.ndindex((Board.WIDTH, Board.HEIGHT)):
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x * 30, y * 30, 30, 30), 1)
        
        for x, y in np.ndindex((Board.WIDTH, Board.HEIGHT)):
            block_value = self.board.grid[y, x]
            if block_value != 0:
                block_color = Tetromino.TETROMINO_COLORS[block_value - 1]
                pygame.draw.rect(self.screen, block_color, pygame.Rect(x * 30, y * 30, 30, 30))


        tetromino_color = self.current_tetromino.color
        for dx, dy in np.ndindex(self.current_tetromino.shape.shape):
            if self.current_tetromino.shape[dx, dy]:
                pygame.draw.rect(self.screen, tetromino_color, pygame.Rect((self.current_x + dx) * 30, (self.current_y + dy) * 30, 30, 30))

        if self.game_over:
            self.render_game_over()
        
                
        pygame.display.flip()
        
    def get_next_tetromino(self):
        tetromino = Tetromino(self.bag[self.bag_index])
        self.bag_index += 1
        if self.bag_index >= len(self.bag):
            self.bag_index = 0
            random.shuffle(self.bag)
        return tetromino
    
    def can_place(self, tetromino, x, y):
        return self.board.is_valid_move(tetromino, x, y)

    def place_tetromino(self):
        self.board.place(self.current_tetromino, self.current_x, self.current_y)
        lines_cleared = self.board.clear_lines()
        self.lines_cleared += lines_cleared

        while self.lines_cleared >= self.lines_to_next_level:
            self.level += 1
            self.lines_cleared -= self.lines_to_next_level
            self.drop_speed = max(150, int(self.drop_speed * 0.9))
            
        print(self.drop_speed)
        self.current_tetromino = self.get_next_tetromino()
        self.current_x = Board.WIDTH // 2
        self.current_y = 0

    def render_game_over(self):
        # Fill the screen with a semi-transparent overlay
        overlay = pygame.Surface((Board.WIDTH * 30, Board.HEIGHT * 30), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Display the game over text
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        text_x = (Board.WIDTH * 30 - game_over_text.get_width()) // 2
        text_y = (Board.HEIGHT * 30 - game_over_text.get_height()) // 2
        self.screen.blit(game_over_text, (text_x, text_y))

        # Display the restart button
        restart_text = font.render('Click to Restart', True, (255, 255, 255))
        restart_x = (Board.WIDTH * 30 - restart_text.get_width()) // 2
        restart_y = text_y + game_over_text.get_height() + 10
        self.screen.blit(restart_text, (restart_x, restart_y))

        pygame.display.flip()


    def restart_game(self):
        self.board = Board()
        self.current_tetromino = Tetromino(random.randint(0, 6))
        self.current_x = Board.WIDTH // 2
        self.current_y = 0
        self.drop_counter = 0
        self.held_tetromino = None
        self.can_hold = True
        self.bag = list(range(7))
        random.shuffle(self.bag)
        self.bag_index = 0
        self.level = 1
        self.lines_cleared = 0
        self.lines_to_next_level = 10
        self.drop_speed = 1000 - (self.level - 1) * 50
        self.game_over = False

    def run(self):
        while self.handle_input():
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.drop_counter += self.soft_drop_speed
            else:
                self.drop_counter += self.clock.tick(60)
            
            if not self.game_over:
                if self.drop_counter > self.drop_speed:
                    self.update()
                    self.drop_counter = 0
                self.render()
            else:
                self.render_game_over()

