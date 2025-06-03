import pygame
import time
from config import TIMER_DURATION 

class UI:
    def __init__(self, screen, board, theme):
        self.screen = screen
        self.board = board
        self.theme = theme

    def draw(self, timer_enabled=False, start_time=None, time_2048=None):
        self.screen.fill(self.theme['background'])
        
        # Отрисовка счёта
        self.draw_score()
        
        # Отрисовка таймера, если он включен и 2048 не достигнут
        if timer_enabled and start_time is not None and not self.board.won:
            elapsed = time.time() - start_time
            remaining = max(0, TIMER_DURATION - elapsed)
            mins, secs = divmod(int(remaining), 60)
            timer_text = f"{mins:02d}:{secs:02d}"
            font = pygame.font.SysFont('Arial', 36, bold=True)
            text_color = (255, 0, 0) if remaining < 30 else self.theme['button_colors']['text']
            text_surface = font.render(timer_text, True, text_color)
            text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 20, 20))
            self.screen.blit(text_surface, text_rect)
        
        # Отрисовка доски
        screen_width, screen_height = self.screen.get_size()
        tile_size = min(screen_width, screen_height - 150) // self.board.size
        padding = 10
        board_size = tile_size * self.board.size + padding * 2
        board_x = (screen_width - board_size) // 2
        board_y = (screen_height - board_size) // 2 + 50

        # Отрисовка фона доски
        pygame.draw.rect(self.screen, self.theme['board'], 
                        (board_x, board_y, board_size, board_size), 
                        border_radius=10)

        for r in range(self.board.size):
            for c in range(self.board.size):
                value = self.board.grid[r][c]
                rect = pygame.Rect(
                    board_x + c * tile_size + padding, 
                    board_y + r * tile_size + padding, 
                    tile_size - padding*2, 
                    tile_size - padding*2
                )
                color = self.theme['tile_colors'].get(value, self.theme['board'])
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                
                if value:
                    font_size = tile_size // 2 if value < 100 else tile_size // 3
                    font = pygame.font.SysFont('Arial', font_size, bold=True)
                    text_color = (0, 0, 0) if value < 8 else (255, 255, 255)
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        
        if self.board.won and not self.board.has_pressed_continue:
            self.draw_win(timer_enabled, time_2048)
        elif self.board.is_game_over():
            self.draw_game_over(timer_enabled, time_2048)
    
    def draw_score(self):
        """Отрисовывает текущий счёт"""
        score_text = f"Счёт: {self.board.score}"
        font = pygame.font.SysFont('Arial', 48, bold=True)
        text_color = self.theme['button_colors']['text']
        text_surface = font.render(score_text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 60))
        self.screen.blit(text_surface, text_rect)
    
    def draw_game_over(self, timer_enabled=False, time_2048=None):
        """Рисует экран проигрыша"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        center_x, center_y = self.screen.get_width() // 2, self.screen.get_height() // 2
        
        # Заголовок
        font_large = pygame.font.SysFont('Arial', 72, bold=True)
        if timer_enabled and not time_2048:
            game_over_text = font_large.render("ВРЕМЯ ВЫШЛО!", True, (255, 70, 70))
        else:
            game_over_text = font_large.render("ВЫ ПРОИГРАЛИ", True, (255, 70, 70))
        game_over_rect = game_over_text.get_rect(center=(center_x, center_y - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Финальный счёт
        font_medium = pygame.font.SysFont('Arial', 48)
        score_text = font_medium.render(f"Финальный счёт: {self.board.score}", True, (220, 220, 220))
        score_rect = score_text.get_rect(center=(center_x, center_y + 10))
        self.screen.blit(score_text, score_rect)
        
        # Инструкция
        font_small = pygame.font.SysFont('Arial', 36)
        instruction = font_small.render("Нажмите R чтобы начать снова", True, (220, 220, 220))
        instr_rect = instruction.get_rect(center=(center_x, center_y + 100))
        self.screen.blit(instruction, instr_rect)
    
    def draw_win(self, timer_enabled=False, time_2048=None):
        """Рисует экран победы"""
        if not self.board.has_pressed_continue:
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            center_x, center_y = self.screen.get_width() // 2, self.screen.get_height() // 2
            
            # Заголовок "ПОБЕДА!"
            font_large = pygame.font.SysFont('Arial', 72, bold=True)
            win_text = font_large.render("ПОБЕДА!", True, (100, 255, 100))
            win_rect = win_text.get_rect(center=(center_x, center_y - 100))
            self.screen.blit(win_text, win_rect)
            
            # Сообщение
            font_medium = pygame.font.SysFont('Arial', 36)
            if time_2048:
                mins, secs = divmod(int(time_2048), 60)
                time_str = f"{mins:02d}:{secs:02d}"
                message = font_medium.render(f"Вы собрали 2048 за {time_str}!", True, (220, 220, 220))
            else:
                message = font_medium.render("Вы собрали плитку 2048!", True, (220, 220, 220))
            message_rect = message.get_rect(center=(center_x, center_y))
            self.screen.blit(message, message_rect)
            
            # Инструкции
            font_small = pygame.font.SysFont('Arial', 30)
            continue_text = font_small.render("Продолжить игру - ПРОБЕЛ", True, (220, 220, 220))
            continue_rect = continue_text.get_rect(center=(center_x, center_y + 80))
            self.screen.blit(continue_text, continue_rect)
            
            menu_text = font_small.render("Выйти в меню - ESC", True, (220, 220, 220))
            menu_rect = menu_text.get_rect(center=(center_x, center_y + 120))
            self.screen.blit(menu_text, menu_rect)