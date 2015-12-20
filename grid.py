# encoding: utf-8

from __future__ import division
import os.path
import pygame

HOVER_COLOR = [255, 255, 255]
CHESS_GRID = 8


class Grid:
    """Игровое поле,
    bg_x, bg_y - Координаты левого верхнего угла фона игрового поля
    bg_size - Размер фона игрового поля в пикселах
    offset_x, offset_y - Координаты левого верхнего угла игрового поля на экране в пикселах относительно фона
    cell_size - Размер клетки в пикселах
    active_cell - Коор-ты активной ячейки т.е. коор-ты ячейки где находится курсор мыши
    """
    def __init__(self, bg_x, bg_y, bg_size, offset_x, offset_y, cell_size):
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.bg_size = bg_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cell_size = cell_size
        self.active_cell = (0, 0)

        self.bg_texture = pygame.image.load(os.path.join('data', 'chessboard.png'))

    def render(self, screen):
        """ Отрисовка игрового поля
        :type screen: screen.Screen
        """
        screen.draw_texture(self.bg_texture, self.bg_x, self.bg_y, self.bg_size, self.bg_size)

        # Рисуем рамку поверх активной ячейки
        x, y = self.active_cell
        bg_x = x * self.cell_size + self.offset_x + self.bg_x
        bg_y = y * self.cell_size + self.offset_y + self.bg_y
        screen.draw_frame(HOVER_COLOR, bg_x, bg_y, self.cell_size, self.cell_size, 2)

    def cell_hover(self, pos):
        """Активирует клетку, на которую наведён курсор мыши
        """
        x, y = self.pixels_to_grid(pos)
        if not self.good_coords(x, y):
            return
        self.active_cell = (x, y)

    def convert_to_local(self, pos):
        """Получаем на вход пиксельные коор-ты относительно окна,
        возвращаем пиксельные коор-ты относительно игрового поля
        pos - координаты, список из двух чисел
        """
        x, y = pos
        return [x - self.bg_x - self.offset_x, y - self.bg_y - self.offset_y]

    def pixels_to_grid(self, pos):
        """Возвращает коор-ты в клетках из переданных коор-т в пикселах
        """
        pix_x, pix_y = pos
        x = pix_x // self.cell_size
        y = pix_y // self.cell_size
        return [x, y]

    @staticmethod
    def good_coords(x, y):
        """Возвращает True, если коор-ты х, у принадлежат ячейкам
        """
        return 0 <= x < CHESS_GRID and 0 <= y < CHESS_GRID
