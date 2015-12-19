# encoding: utf-8

from __future__ import division


class Grid:
    """Игровое поле,
    pix_size - Кол-во пикселей одной ячейки по вертикали или горизонтали
    screen_x, screen_y - Координаты левого верхнего угла игрового поля на экране в пикселах
    screen_size - Размер игрового поля в пикселах
    """
    def __init__(self, screen_x, screen_y, screen_size):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_size = screen_size
        self.pix_size = screen_size // 8

    def render(self, screen):
        """ Отрисовка игрового поля
        :type screen: screen.Screen
        """
        screen.draw_rect([250, 123, 50], self.screen_x, self.screen_y, self.screen_size, self.screen_size)
