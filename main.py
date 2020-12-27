import pygame
import random

pygame.init()
size = 660, 340
screen = pygame.display.set_mode(size)

def draw_n(n, pos, size):
    font = pygame.font.Font(None, size)
    text = font.render(str(n), 1, (100, 255, 100))
    screen.blit(text, pos)

class Board:
    water = pygame.Color('blue')
    ship = pygame.Color((166, 166, 166))
    miss = pygame.Color((0, 0, 153))
    hit = pygame.Color('red')

    def __init__(self):
        self.width = 10
        self.height = 10
        self.board = [[Board.water] * self.width for _ in range(self.height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def is_out(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if self.is_out(cell_x, cell_y):
            return None
        return cell_x, cell_y

    def is_free(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.is_out(x + dx, y + dy):
                    continue
                if self.board[y + dy][x + dx] != Board.water:
                    return False
        return True

    def is_valid(self, ship):
        for x, y in ship:
            if self.is_out(x, y) or not self.is_free(x, y):
                return False
        return True

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

    def random_valid_ship(self, decks):
        while True:
            ship = self.random_ship(decks)
            if self.is_valid(ship):
                return ship

    def disposition(self):
        for deck in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            ship = self.random_valid_ship(deck)
            for x, y in ship:
                self.board[y][x] = Board.ship

    def render(self):
        radius = self.cell_size // 2
        for y in range(self.height):
            for x in range(self.width):
                left = self.left + x * self.cell_size
                top = self.top + y * self.cell_size
                rect = (left, top, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.board[y][x], rect)
                pygame.draw.rect(screen, pygame.Color('white'), rect, 2)
                
player = Board()
player.disposition()
enemy = Board()
enemy.disposition()
player.set_view(20, 20, 30)
enemy.set_view(340, 20, 30)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    screen.fill(pygame.Color('black'))
    player.render()
    enemy.render()
    pygame.display.flip()