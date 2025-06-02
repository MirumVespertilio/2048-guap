import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from menu import Menu

pygame.init()

# Получаем размеры экрана
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

# Устанавливаем размер окна, равный размеру экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048 Game")

def main():
    menu = Menu(screen)
    current_screen = "menu"  # может быть "menu", "game" или "settings"
    game_settings = {"theme": "light", "grid_size": 4}
    game = None

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_screen == "menu":
                button_clicked = menu.handle_event(event)
                if button_clicked:
                    if button_clicked == "Начать игру":
                        game = Game(screen, game_settings["theme"], game_settings["grid_size"], game_settings.get("timer_enabled", False))
                        current_screen = "game"
                    elif button_clicked == "Настройки":
                        menu.setup_settings_menu()
                        current_screen = "settings"
                    elif button_clicked == "Выход":
                        running = False
            
            elif current_screen == "settings":
                button_clicked = menu.handle_event(event)
                if button_clicked:
                    if button_clicked.startswith("Тема:"):
                        for button in menu.buttons:
                            if button.text == button_clicked and hasattr(button, 'theme_key'):
                                game_settings["theme"] = button.theme_key
                                menu.current_theme = button.theme_key
                                menu.setup_settings_menu()
                                break
                    elif button_clicked.startswith("Размер:"):
                        size = int(button_clicked.split("x")[0][-1])
                        game_settings["grid_size"] = size
                        menu.current_size = size  # Обновляем текущий размер в меню
                        menu.setup_settings_menu()  # Пересоздаем меню с новыми выделениями
                    elif button_clicked == "Таймер":
                        menu.timer_enabled = not menu.timer_enabled
                        game_settings["timer_enabled"] = menu.timer_enabled
                        menu.setup_settings_menu()
                    elif button_clicked == "Назад":
                        menu.setup_main_menu()
                        current_screen = "menu"
            
            elif current_screen == "game":
                if event.type == pygame.KEYDOWN:
                    result = game.handle_event(event)
                    if result == "menu":
                        current_screen = "menu"
                        menu.setup_main_menu()
        
        # Отрисовка текущего экрана
        if current_screen == "menu" or current_screen == "settings":
            menu.draw()
        elif current_screen == "game":
            game.run()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()