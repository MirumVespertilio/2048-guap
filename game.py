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

    def run(self):
        self.ui.draw()