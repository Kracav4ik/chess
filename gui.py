# encoding: utf-8

from __future__ import division
import pygame


class Button:
    """Кнопка
    x, y - левый верхний угол кнопки в пикселях
    width, height - ширена и высота кнопки
    text - текст
    click - функция, которая зовётся при клике на кнопку
    font - шрифт
    """
    def __init__(self, x, y, width, height, text, click_function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.click = click_function
        self.color = (0, 0, 255)

    def render(self, screen):
        screen.draw_rect(self.color, self.x, self.y, self.width, self.height)
        font = screen.get_font('Arial', 30)
        screen.draw_text(self.text, font, (255, 170, 170), self.x, self.y, self.width, self.height)

    def is_inside(self, pos):
        """Возвращает True, если точка pos находится внутри
        """
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def on_mouse_move(self, pos):
        if self.is_inside(pos):
            self.color = [128, 128, 255]
        else:
            self.color = (0, 0, 255)
