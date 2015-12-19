# encoding: utf-8
from __future__ import division

import pygame
import sys
from grid import Grid
from screen import Screen


WINDOW_SIZE = (740, 740)  # размер окна в пикселах
WINDOW_BG_COLOR = (150, 50, 250)  # цвет окна

# инициализация
pygame.init()

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)

grid = Grid(10, 10, 720, 20, 20, 80)


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()


def process_game():
    pass


def render():
    """ Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)  # Закрашиваем фон

    grid.render(screen)

    pygame.display.flip()  # Переключаем буфер

# игровой цикл
while True:
    handle_input()
    process_game()
    render()
