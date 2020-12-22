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
    ship = pygame.Color((51, 51, 51))
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

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

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
enemy = Board()
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