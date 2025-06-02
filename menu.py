import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(0, 0, 0), is_selected=False, border_color=None, theme_key=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.is_selected = is_selected
        self.border_color = border_color if border_color else (0, 0, 0)
        self.theme_key = theme_key
        self.font = pygame.font.SysFont('Bahnschrift', 40, bold=False)

    def draw(self, screen):
        # Цвет кнопки зависит от состояния
        if self.is_selected:
            color = self.hover_color  # Используем hover_color для выбранного состояния
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
            
        pygame.draw.rect(screen, color, self.rect, border_radius=1)
        
        # Обводка
        border_width = 4 if self.is_selected else 1
        pygame.draw.rect(screen, self.border_color, self.rect, border_width, border_radius=1)
        
        # Текст
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.current_theme = 'light'
        self.current_size = 4 
        self.setup_main_menu()

    def setup_main_menu(self):
        width, height = 300, 80
        center_x = self.screen.get_width() // 2 - width // 2
        center_y = self.screen.get_height() // 2 
        theme = THEMES[self.current_theme]
        btn_colors = theme['button_colors']
        
        self.buttons = [
            Button(
            center_x, center_y - 100, width, height, "Начать игру", btn_colors['normal'], 
            btn_colors['hover'], btn_colors['text'], border_color=btn_colors['border']
        ),
            Button(center_x, center_y, width, height, "Настройки", btn_colors['normal'], 
            btn_colors['hover'], btn_colors['text'], border_color=btn_colors['border']
        ),
            Button(center_x, center_y + 100, width, height, "Выход", (200, 100, 100), (250, 150, 150), (255, 255, 255))
        ]

    def setup_settings_menu(self):
        width, height = 400, 80
        center_x = self.screen.get_width() // 2 - width // 2
        center_y = self.screen.get_height() // 2 
        theme = THEMES[self.current_theme]
        btn_colors = theme['button_colors']
        
        # Фиксированные цвета для кнопок выбора темы
        self.buttons = [
            # Кнопка светлой темы
            Button(center_x - 220, center_y - 180, width, height, "Тема: Светлая", 
                (220, 220, 220), (240, 240, 240), (0, 0, 0), 
                self.current_theme == 'light', (255, 255, 255), theme_key='light'),
        
            # Кнопка тёмной темы
            Button(center_x - 220, center_y - 90, width, height, "Тема: Тёмная", 
                (60, 60, 80), (90, 90, 110), (255, 255, 255), 
                self.current_theme == 'dark', (255, 255, 255), theme_key='dark'),
            
            # Кнопка космической темы
            Button(center_x - 220, center_y, width, height, "Тема: Космос", 
                (15, 10, 40), (10, 5, 30), (255, 255, 255), 
                self.current_theme == 'cosmos', (255, 255, 255), theme_key='cosmos'),
            
            # Кнопка морской темы
            Button(center_x - 220, center_y + 90, width, height, "Тема: Морская", 
                (10, 30, 60), (5, 20, 40), (255, 255, 255), 
                self.current_theme == 'ocean', (255, 255, 255), theme_key='ocean'),
            
            # Кнопка сведневековой темы
            Button(center_x - 220, center_y + 180, width, height, "Тема: Средневековье", 
                (80, 60, 40), (60, 40, 30), (255, 255, 255), 
                self.current_theme == 'medieval', (255, 255, 255), theme_key='medieval'),
        
            # Кнопки размера
            Button(center_x + 220, center_y - 180, width, height, "Размер: 4x4", 
                btn_colors['normal'], btn_colors['hover'], btn_colors['text'], 
                self.current_size == 4),
            Button(center_x + 220, center_y - 90, width, height, "Размер: 5x5", 
                btn_colors['normal'], btn_colors['hover'], btn_colors['text'], 
                self.current_size == 5),
            Button(center_x + 220, center_y, width, height, "Размер: 6x6", 
                btn_colors['normal'], btn_colors['hover'], btn_colors['text'], 
                self.current_size == 6),
        
            # Кнопка назад
            Button(center_x, center_y + 300, width, height, "Назад", 
                (200, 150, 150), (230, 180, 180), (255, 255, 255))
        ]

    def draw(self):
        theme = THEMES[self.current_theme]
        self.screen.fill(theme['menu_background'])
        
        title_font = pygame.font.SysFont('Bahnschrift', 100, bold=False)
        title = title_font.render("2048", True, theme['title_color'])
        title_y = self.screen.get_height() // 4 - 50
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, title_y))
        
        for button in self.buttons:
            button.draw(self.screen)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, event):
                return button.text
        return None