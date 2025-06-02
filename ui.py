import pygame

class UI:
    def __init__(self, screen, board, theme):
        self.screen = screen
        self.board = board
        self.theme = theme

    def draw(self):
        self.screen.fill(self.theme['background'])
        
        # Отрисовка счёта
        self.draw_score()
        
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
        
        if self.board.is_game_over():
            self.draw_game_over()
    
    def draw_score(self):
        """Отрисовывает текущий счёт (всегда чёрный текст)"""
        score_text = f"Счёт: {self.board.score}"
        font = pygame.font.SysFont('Arial', 48, bold=True)
        text_surface = font.render(score_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 60))
        self.screen.blit(text_surface, text_rect)
    
    def draw_game_over(self):
        """Рисует экран проигрыша с правильным расположением элементов"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        center_x, center_y = self.screen.get_width() // 2, self.screen.get_height() // 2
        
        # Заголовок "ПОТРАЧЕНО"
        font_large = pygame.font.SysFont('Arial', 72, bold=True)
        game_over_text = font_large.render("ПОТРАЧЕНО", True, (255, 70, 70))
        game_over_rect = game_over_text.get_rect(center=(center_x, center_y - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Финальный счёт
        font_medium = pygame.font.SysFont('Arial', 48)
        score_text = font_medium.render(f"Финальный счёт: {self.board.score}", True, (220, 220, 220))
        score_rect = score_text.get_rect(center=(center_x, center_y + 10))
        self.screen.blit(score_text, score_rect)
        
        # Инструкция (теперь ниже)
        font_small = pygame.font.SysFont('Arial', 36)
        instruction = font_small.render("Нажмите R чтобы начать снова", True, (220, 220, 220))
        instr_rect = instruction.get_rect(center=(center_x, center_y + 100))  # Смещено вниз
        self.screen.blit(instruction, instr_rect)