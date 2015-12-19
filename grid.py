# encoding: utf-8

from __future__ import division
import os.path
import pygame


class Grid:
    """Игровое поле,
    bg_x, bg_y - Координаты левого верхнего угла фона игрового поля
    bg_size - Размер фона игрового поля в пикселах
    offset_x, offset_y - Координаты левого верхнего угла игрового поля на экране в пикселах относительно фона
    cell_size - Размер клетки в пикселах
    """
    def __init__(self, bg_x, bg_y, bg_size, offset_x, offset_y, cell_size):
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.bg_size = bg_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cell_size = cell_size

        self.bg_texture = pygame.image.load(os.path.join('data', 'chessboard.png'))

    def render(self, screen):
        """ Отрисовка игрового поля
        :type screen: screen.Screen
        """
        screen.draw_texture(self.bg_texture, self.bg_x, self.bg_y, self.bg_size, self.bg_size)
