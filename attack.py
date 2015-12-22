# encoding: utf-8

from __future__ import division


class AttackGrid:
    """Поля, которые атакованы фигурами
    pix_x, pix_y - левый верхний угол
    cell_size - Размер клетки в пикселах
    """
    def __init__(self, pix_x, pix_y, cell_size):
        self.pix_x = pix_x
        self.pix_y = pix_y
        self.cell_size = cell_size

    def render(self, screen):
        color = [255, 0, 0, 32]
        for x in range(8):
            pix_x = x * self.cell_size + self.pix_x
            pix_y = 2 * self.cell_size + self.pix_y
            screen.draw_rect(color, pix_x + 2, pix_y + 2, self.cell_size - 4, self.cell_size - 4)
            pix_y = 5 * self.cell_size + self.pix_y
            screen.draw_rect(color, pix_x + 2, pix_y + 2, self.cell_size - 4, self.cell_size - 4)

