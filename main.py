import pygame
import random
import pygame_menu
import sys

player1 = False
pygame.init()
cell_size = 30
size = 660, 340
screen = pygame.display.set_mode(size)
images = {
    (1, 1): 'seabattle_1_90.jpg',
    (1, 2): 'seabattle_2_0.jpg',
    (2, 1): 'seabattle_2_90.jpg',
    (1, 3): 'seabattle_3_0.jpg',
    (3, 1): 'seabattle_3_90.jpg',
    (1, 4): 'seabattle_4_0.jpg',
    (4, 1): 'seabattle_4_90.jpg'
}
all_sprites = pygame.sprite.Group()

# Загрузка звуков
pygame.mixer.music.load('data/Fon.mp3')
win_sound = pygame.mixer.Sound('data/pobeda.mp3')
lose_sound = pygame.mixer.Sound('data/lose.mp3')
podbil_sound = pygame.mixer.Sound('data/hits.mp3')
ybil_sound = pygame.mixer.Sound('data/Ybil.mp3')
promah_sound = pygame.mixer.Sound('data/miss.mp3')


# Подготовка картинки
def prepare_image(size):
    img = pygame.image.load('./data/' + images[size])
    width, heigt = size
    img = pygame.transform.scale(img, (width * cell_size, heigt * cell_size))
    img.set_alpha(128)
    return img


# Новый спрайт
def add_sprite(size, pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = prepare_image(size)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x, sprite.rect.y = pos
    all_sprites.add(sprite)


# Игровая доска
class Board:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    water = pygame.Color('blue')
    miss = pygame.Color((0, 0, 153))
    ship = pygame.Color('green')
    injured = pygame.Color('orange')
    dead = pygame.Color('red')

    def __init__(self, hidden):
        self.hidden = hidden
        self.width = 10
        self.height = 10
        self.left = 0
        self.top = 0

    # Задаёт положение доски на экране
    def set_view(self, left, top):
        self.left = left
        self.top = top

    # Проверяет координаты клетки на выход за доску
    def is_out(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    # Получает координаты клетки из позиции мыши
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // cell_size
        cell_y = (mouse_pos[1] - self.top) // cell_size
        if self.is_out(cell_x, cell_y):
            return None
        return cell_x, cell_y

    # Получает координаты левого верхнего пикселя клетки
    def get_left_top(self, x, y):
        return (self.left + x * cell_size, self.top + y * cell_size)

    # Проверят есть ли место для корабля в данной клетке
    def is_free(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.is_out(x + dx, y + dy):
                    continue
                if self.board[y + dy][x + dx] != Board.water:
                    return False
        return True

    # Проверяет можно ли разместить корабль в клетке
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
            if not self.hidden:
                width = ship[-1][0] - ship[0][0] + 1
                height = ship[-1][1] - ship[0][1] + 1
                size = (width, height)
                add_sprite(size, self.get_left_top(*ship[0]))

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
            pygame.mixer.Sound.set_volume(ybil_sound, 0.15)
            pygame.mixer.Sound.play(ybil_sound)
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if not self.is_out(x + dx, y + dy) and self.board[y + dy][x + dx] == Board.water:
                    self.board[y + dy][x + dx] = Board.miss

    # Выстрел по клетке
    def on_shot(self, shot):
        x, y = shot
        if self.board[y][x] == Board.water:
            self.board[y][x] = Board.miss
            pygame.mixer.Sound.set_volume(promah_sound, 0.4)
            pygame.mixer.Sound.play(promah_sound)
            return False
        if self.board[y][x] == Board.ship:
            self.board[y][x] = Board.injured
            self.last_injured_shot = shot
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                if not self.is_out(x + dx, y + dy):
                    self.board[y + dy][x + dx] = Board.miss
            ship = self.get_ship(shot)
            if self.is_ship_dead(ship):
                self.set_ship_dead(ship)
            pygame.mixer.Sound.set_volume(podbil_sound, 0.6)
            pygame.mixer.Sound.play(podbil_sound)
            return True

    # Попытка добить корабль
    def near_injured_shot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != Board.injured:
                    continue
                for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    shot = x + dx, y + dy
                    if not self.is_out(*shot) and self.is_valid_shot(shot):
                        return shot
        return None

    # Случайный допустимый выстрел
    def random_valid_shot(self):
        while True:
            shot = self.random_shot()
            if self.is_valid_shot(shot):
                return shot
        return None

    # Рисование
    def render(self):
        radius = cell_size // 2
        for y in range(self.height):
            for x in range(self.width):
                left, top = self.get_left_top(x, y)
                rect = (left, top, cell_size, cell_size)
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
    if player1:
        text = font.render(txt, True, (0, 255, 0))
    else:
        text = font.render(txt, True, (255, 0, 0))
    text_x = screen.get_width() // 2 - text.get_width() // 2
    text_y = screen.get_height() // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    if player1:
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
    else:
        pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


def start_the_game():
    txt = None
    player = Board(False)
    enemy = Board(True)
    player.set_view(20, 20)
    enemy.set_view(340, 20)
    player.disposition()
    enemy.disposition()
    clock = pygame.time.Clock()
    enemy_turn = False

    # игровой цикл
    running = True
    while running:
        if enemy_turn:
            cell = player.near_injured_shot()
            if cell is None:
                cell = player.random_valid_shot()
            enemy_turn = player.on_shot(cell)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not enemy_turn:
                cell = enemy.get_cell(event.pos)
                if cell != None and enemy.is_valid_shot(cell):
                    enemy_turn = not enemy.on_shot(cell)
        screen.fill(pygame.Color('black'))
        player.render()
        enemy.render()
        all_sprites.draw(screen)
        pygame.display.flip()
        if player.is_dead() or enemy.is_dead():
            pygame.mixer.music.stop()
            running = False
        clock.tick(2)

    if player.is_dead():
        pygame.mixer.Sound.play(lose_sound)
        txt = 'Вы проиграли!'
    elif enemy.is_dead():
        pygame.mixer.Sound.play(win_sound)
        txt = 'Вы выиграли!'
        global player1
        player1 = True
    else:
        txt = None

    # финальное окно
    running = (txt != None)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                running = False
                sys.exit()
        screen.fill(pygame.Color('black'))
        draw_text(txt)
        pygame.display.flip()


menu = pygame_menu.Menu(340, 660, 'МОРСКОЙ БОЙ',
                        theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_button('Играть', start_the_game)
menu.add_button('Выйти', pygame_menu.events.EXIT)
menu.mainloop(screen)