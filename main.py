# encoding: utf-8
from __future__ import division

import pygame
import sys


WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (150, 50, 250)  # цвет окна

# инициализация
pygame.init()

window_surface = pygame.display.set_mode(WINDOW_SIZE)


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

    pygame.display.flip()  # Переключаем буфер

# игровой цикл
while True:
    handle_input()
    process_game()
    render()
