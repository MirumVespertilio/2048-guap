import random

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.won = False
        self.game_over = False
        self.has_pressed_continue = False
        self.add_random_tile()  # Добавляем плитки при старте игры
        self.add_random_tile()

    def reset(self):
        """Сбросить игровое поле"""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.won = False
        self.game_over = False
        self.has_pressed_continue = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Добавляет плитку (2 или 4) в случайную пустую ячейку"""
        empty = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        """Перемещает плитки в указанном направлении"""
        original_grid = [row[:] for row in self.grid]  # Копируем исходное поле

        if direction == 'left':
            for i in range(self.size):
                row = [tile for tile in self.grid[i] if tile != 0]
                new_row = self._merge(row)
                self.grid[i] = new_row + [0] * (self.size - len(new_row))

        elif direction == 'right':
            for i in range(self.size):
                row = [tile for tile in self.grid[i] if tile != 0]
                row = row[::-1]
                new_row = self._merge(row)
                self.grid[i] = [0] * (self.size - len(new_row)) + new_row[::-1]

        elif direction == 'up':
            self.grid = [list(col) for col in zip(*self.grid)]
            for i in range(self.size):
                col = [tile for tile in self.grid[i] if tile != 0]
                new_col = self._merge(col)
                self.grid[i] = new_col + [0] * (self.size - len(new_col))
            self.grid = [list(row) for row in zip(*self.grid)]

        elif direction == 'down':
            self.grid = [list(col) for col in zip(*self.grid)]
            for i in range(self.size):
                col = [tile for tile in self.grid[i] if tile != 0]
                col = col[::-1]
                new_col = self._merge(col)
                self.grid[i] = [0] * (self.size - len(new_col)) + new_col[::-1]
            self.grid = [list(row) for row in zip(*self.grid)] 

        # Проверяем, если поле изменилось
        if original_grid != self.grid:
            self.add_random_tile()

    def _merge(self, tiles):
        """Сливает плитки в ряду или колонке и обновляет счёт"""
        new_tiles = []
        skip = False
        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                new_value = tiles[i] * 2
                new_tiles.append(tiles[i] * 2)
                self.score += new_value 
                skip = True
            else:
                new_tiles.append(tiles[i])
        return new_tiles
    
    def is_game_over(self):
        """Проверяет, остались ли возможные ходы"""
        if self.game_over:  # Проверяем флаг game_over в первую очередь
            return True
        
        # Проверяем наличие пустых клеток
        if any(0 in row for row in self.grid):
            return False
        
        # Проверяем возможные слияния по горизонтали и вертикали
        for i in range(self.size):
            for j in range(self.size):
                if j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        
        return True
    
    def has_won(self):
        """Проверяет, достигнута ли плитка 2048 и устанавливает флаг won"""
        if any(2048 in row for row in self.grid) and not self.won:
            self.won = True
            self.game_over = False  # Не завершаем игру при победе
            return True
        return False

