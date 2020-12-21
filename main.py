import pygame
import random

pygame.init()
size = 400, 600
screen = pygame.display.set_mode(size)

def draw_n(n, pos, size):
    font = pygame.font.Font(None, size)
    text = font.render(str(n), 1, (100, 255, 100))
    screen.blit(text, pos)

class Board:
    # создание поля
    def __init__(self, width, height, value):
        self.width = width
        self.height = height
        self.board = [[value] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
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



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    screen.fill((0, 0, 0))
    pygame.display.flip()