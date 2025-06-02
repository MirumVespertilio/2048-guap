import pygame

class UI:
    def __init__(self, screen, board, theme):
        self.screen = screen
        self.board = board
        self.theme = theme

    def draw(self):
        self.screen.fill(self.theme['background'])
        # Отрисовка доски (прежний код)
        size = min(self.screen.get_width(), self.screen.get_height())
        tile_size = size // self.board.size
        padding = 10
        board_size = tile_size * self.board.size + padding * 2
        board_x = (self.screen.get_width() - board_size) // 2
        board_y = (self.screen.get_height() - board_size) // 2

        for r in range(self.board.size):
            for c in range(self.board.size):
                value = self.board.grid[r][c]
                rect = pygame.Rect(board_x + c * tile_size + padding, 
                                board_y + r * tile_size + padding, 
                                tile_size - padding*2, 
                                tile_size - padding*2)
                color = self.theme['tile_colors'].get(value, self.theme['board'])
                pygame.draw.rect(self.screen, color, rect)
                
                if value:
                    font = pygame.font.SysFont(None, tile_size // 3)  # ← Вернул исходный шрифт
                    text_color = (0, 0, 0)  # ← Чёрный цвет текста как было изначально
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        
        # Проверка на проигрыш (новый код)
        if self.board.is_game_over():
            self.draw_game_over()
        
    def draw_game_over(self):
        """Рисует экран проигрыша"""
        # Полупрозрачное затемнение
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Текст "Game Over" (красивый шрифт только здесь)
        font_large = pygame.font.SysFont('Arial', 72, bold=True)
        text = font_large.render("ПОТРАЧЕНО", True, (255, 70, 70))
        text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Инструкция
        font_small = pygame.font.SysFont('Arial', 36)
        instruction = font_small.render("Нажмите R чтобы начать снова", True, (220, 220, 220))
        instr_rect = instruction.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        self.screen.blit(instruction, instr_rect)
