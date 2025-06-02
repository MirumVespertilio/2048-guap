import pygame
from config import *
from board import Board
from ui import UI

class Game:
    def __init__(self, screen, theme_name=DEFAULT_THEME, grid_size=DEFAULT_GRID_SIZE):
        self.screen = screen
        self.theme = THEMES[theme_name]
        self.board = Board(grid_size)
        self.ui = UI(self.screen, self.board, self.theme)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.board.won:
                self.board.has_pressed_continue = True  # Продолжаем игру после победы
            elif event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_r:
                self.board.reset()
            elif not self.board.is_game_over() and not (self.board.won and not self.board.has_pressed_continue):
                if event.key == pygame.K_LEFT:
                    self.board.move('left')
                elif event.key == pygame.K_RIGHT:
                    self.board.move('right')
                elif event.key == pygame.K_UP:
                    self.board.move('up')
                elif event.key == pygame.K_DOWN:
                    self.board.move('down')
        return None
    
    def run(self):
        self.ui.draw()