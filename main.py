import pygame
import random

pygame.init()
size = 660, 340
screen = pygame.display.set_mode(size)


class Board:
    water = pygame.Color('blue')
    miss = pygame.Color((0, 0, 153))
    ship = pygame.Color((166, 166, 166))
    injured = pygame.Color('orange')
    dead = pygame.Color('red')

    def __init__(self, hidden):
        self.hidden = hidden
        self.width = 10
        self.height = 10
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.disposition()

    # Задаёт положение доски на экране
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Проверяет координаты клетки на выход за доску
    def is_out(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    # Получает координаты клетки из позиции мыши
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if self.is_out(cell_x, cell_y):
            return None
        return cell_x, cell_y

    # Проверят есть ли место для корабля в данной клетке
    def is_free(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.is_out(x + dx, y + dy):
                    continue
                if self.board[y + dy][x + dx] != Board.water:
                    return False
        return True

    # Проверяет можно ли разместить коралбль в клетке
    def is_valid_ship(self, ship):
        for x, y in ship:
            if self.is_out(x, y) or not self.is_free(x, y):
                return False
        return True

    # Случайное не проверенное размещение корабля
    def random_ship(self, decks):
        result = []
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        direction = random.randint(0, 1)
        dx, dy = 0, 0
        if direction == 0:
            dx = 1
        else:
            dy = 1
        for deck in range(decks):
            result.append((x + dx * deck, y + dy * deck))
        return result

    # Случайное допустимое размещение корабля
    def random_valid_ship(self, decks):
        while True:
            ship = self.random_ship(decks)
            if self.is_valid_ship(ship):
                return ship

    # Размещение всех кораблей
    def disposition(self):
        self.board = [[Board.water] * self.width for _ in range(self.height)]
        for deck in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            ship = self.random_valid_ship(deck)
            for x, y in ship:
                self.board[y][x] = Board.ship

    # Проверяет допустим ли выстрел
    def is_valid_shot(self, shot):
        x, y = shot
        return self.board[y][x] in [Board.water, Board.ship]

    # Случайное не проверенный выстрел
    def random_shot(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)        
        return x, y

    # Восстанавливает корабль по клетке
    def get_ship(self, cell):
        ship = []
        queue = [cell]
        while len(queue) != 0:
            x, y = queue.pop(0)
            if self.is_out(x, y):
                continue
            if self.board[y][x] in [Board.water, Board.miss]:
                continue
            if (x, y) in ship:
                continue
            ship.append((x, y))
            queue.append((x, y - 1))
            queue.append((x + 1, y))
            queue.append((x, y + 1))
            queue.append((x - 1, y))
        return ship

    # Проверяет мёртв ли корабль
    def is_ship_dead(self, ship):
        for x, y in ship:
            if self.board[y][x] == Board.ship:
                return False
        return True

    # Помечает корабль мёртвым и соседние клетки
    def set_ship_dead(self, ship):
        for x, y in ship:
            self.board[y][x] = Board.dead
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if not self.is_out(x + dx, y + dy) and self.board[y + dy][x + dx] == Board.water:
                    self.board[y + dy][x + dx] = Board.miss

    # Выстрел по клетке
    def on_shot(self, shot):
        x, y = shot
        if self.board[y][x] == Board.water:
            self.board[y][x] = Board.miss
            return False
        if self.board[y][x] == Board.ship:
            self.board[y][x] = Board.injured
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                if not self.is_out(x + dx, y + dy):
                    self.board[y + dy][x + dx] = Board.miss
            ship = self.get_ship(shot)
            if self.is_ship_dead(ship):
                self.set_ship_dead(ship)
            return True


    # Случайный допустимый выстрел
    def random_valid_shot(self):
        while True:
            shot = self.random_shot()
            if self.is_valid_shot(shot):
                return shot

    # Рисование
    def render(self):
        radius = self.cell_size // 2
        for y in range(self.height):
            for x in range(self.width):
                left = self.left + x * self.cell_size
                top = self.top + y * self.cell_size
                rect = (left, top, self.cell_size, self.cell_size)
                color = self.board[y][x]
                if self.hidden and color in [Board.water, Board.ship]:
                    color = pygame.Color('black')
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, pygame.Color('white'), rect, 2)

    # Мертва ли доска
    def is_dead(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == Board.ship:
                    return False
        return True

# Надпись в центре экрана
def draw_text(txt):
    font = pygame.font.Font(None, 50)
    text = font.render(txt, True, (100, 255, 100))
    text_x = screen.get_width() // 2 - text.get_width() // 2
    text_y = screen.get_height() // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

player = Board(False)
enemy = Board(True)
player.set_view(20, 20, 30)
enemy.set_view(340, 20, 30)
clock = pygame.time.Clock()
enemy_turn = False
running = True
while running:
    if enemy_turn:
        cell = player.random_valid_shot()
        enemy_turn = player.on_shot(cell)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell = enemy.get_cell(event.pos)
            if cell != None and enemy.is_valid_shot(cell):
                enemy_turn = not enemy.on_shot(cell)
    screen.fill(pygame.Color('black'))
    player.render()
    enemy.render()
    pygame.display.flip()
    if player.is_dead() or enemy.is_dead():
        running = False
    clock.tick(5)

if player.is_dead():
    txt = 'You losе'
if enemy.is_dead():
    txt = 'You win!'

running = True
while running:
    for event in pygame.event.get():
        if event.type in [pygame.QUIT, pygame.KEYDOWN]:
            running = False
    screen.fill(pygame.Color('black'))
    draw_text(txt)
    pygame.display.flip()
