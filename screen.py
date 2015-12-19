# encoding: utf-8

from __future__ import division
import pygame


class Screen:
    """Экран, на котором можно рисовать
    surface - Объект класса pygame.Surface, на котором и происходит рисование
    """
    def __init__(self, surface):
        self.surface = surface

    def get_size(self):
        """Размер области, на которой мы рисуем
        """
        width, height = self.surface.get_size()
        return width, height

    def draw_rect(self, color, pix_x, pix_y, pix_w, pix_h):
        """Рисуем закрашенный прямоугольник
        color - Цвет, список из 3-х чисел 0..255
        pix_x, pix_y - координаты левого верхнего угла в пикселях
        pix_w - Ширина в пикселях
        pix_h - Высота в пикселях
        """
        pygame.draw.rect(self.surface, color, (pix_x, pix_y, pix_w, pix_h))

    def draw_text(self, text, font, color, pix_x, pix_y, pix_w, pix_h):
        """Рисуем текст так, чтобы центр нарисованного текста был в центре заданного прямоугольника
        text - Текст
        font - Шрифт
        color - Цвет, список из 3-х чисел 0..255
        pix_x, pix_y - координаты левого верхнего угла прямоугольника в пикселях
        pix_w - Ширина прямоугольника в пикселях
        pix_h - Высота прямоугольника в пикселях
        """
        text_surface = font.render(text, False, color)
        text_x = pix_x + pix_w // 2 - text_surface.get_width() // 2
        text_y = pix_y + pix_h // 2 - text_surface.get_height() // 2
        self.surface.blit(text_surface, (text_x, text_y))

    def draw_frame(self, color, pix_x, pix_y, pix_w, pix_h, thickness):
        """Рисуем прямоугольную рамку
        color - Цвет, список из 3-х чисел 0..255
        pix_x, pix_y - координаты левого верхнего угла в пикселях
        pix_w - Ширина в пикселях
        pix_h - Высота в пикселях
        thickness - Толщина рамки в пикселях
        """
        pygame.draw.rect(self.surface, color, (pix_x, pix_y, pix_w, pix_h), thickness)

    def draw_texture(self, texture, pix_x, pix_y, pix_w, pix_h):
        """Рисуем текстуру так, чтобы ее центр был в центре заданного прямоугольника
        texture - текстура в виде объекта pygame.Surface
        pix_x, pix_y - координаты левого верхнего угла прямоугольника в пикселях
        pix_w - Ширина прямоугольника в пикселях
        pix_h - Высота прямоугольника в пикселях
        """
        tex_x = pix_x + pix_w // 2 - texture.get_width() // 2
        tex_y = pix_y + pix_h // 2 - texture.get_height() // 2
        self.surface.blit(texture, (tex_x, tex_y))
