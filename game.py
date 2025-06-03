import pygame
import time
from config import *
from board import Board
from ui import UI

class Game:
    def __init__(self, screen, theme_name=DEFAULT_THEME, grid_size=DEFAULT_GRID_SIZE, timer_enabled=DEFAULT_TIMER_ENABLED):
        self.screen = screen
        self.theme = THEMES[theme_name]
        self.board = Board(grid_size)
        self.ui = UI(self.screen, self.board, self.theme)
        self.timer_enabled = timer_enabled
        self.start_time = time.time() if timer_enabled else None
        self.time_2048 = None 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.board.won:
                self.board.has_pressed_continue = True
                self.board.won = False
                self.timer_enabled = False
            elif event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_r:
                self.board.reset()
                if self.timer_enabled:
                    self.start_time = time.time()
                    self.time_2048 = None
            elif not self.board.is_game_over() and not (self.board.won and not self.board.has_pressed_continue):
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    direction = self.get_direction(event.key)
                    original_grid = [row[:] for row in self.board.grid]
                    self.board.move(direction)
                    if original_grid != self.board.grid:
                        if any(2048 in row for row in self.board.grid) and not self.time_2048:
                            self.time_2048 = time.time() - self.start_time if self.start_time else None
                            self.board.won = True
                            self.timer_enabled = False
        return None
    
    def get_direction(self, key):
        """Преобразует код клавиши в направление"""
        if key == pygame.K_LEFT: return 'left'
        if key == pygame.K_RIGHT: return 'right'
        if key == pygame.K_UP: return 'up'
        if key == pygame.K_DOWN: return 'down'
        return None
    
    def run(self):
        if not self.board.is_game_over() and not self.board.won:
            if self.timer_enabled and self.start_time is not None:
                elapsed = time.time() - self.start_time
                if elapsed > TIMER_DURATION:
                    self.board.game_over = True
        
        self.ui.draw(self.timer_enabled, self.start_time, self.time_2048)