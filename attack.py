# encoding: utf-8

from __future__ import division


class AttackGrid:
    """Поля, которые атакованы фигурами
    pix_x, pix_y - левый верхний угол
    cell_size - Размер клетки в пикселах
    attacked_cells - список атакуемых ячеек
    """
    def __init__(self, pix_x, pix_y, cell_size):
        self.pix_x = pix_x
        self.pix_y = pix_y
        self.cell_size = cell_size
        self.attacked_cells = []

    def render(self, screen, grid):
        color = [255, 0, 0, 32]
        for x, y in self.attacked_cells:
            if not grid.good_coords(x, y):
                continue
            pix_x = x * self.cell_size + self.pix_x
            pix_y = y * self.cell_size + self.pix_y
            screen.draw_rect(color, pix_x + 2, pix_y + 2, self.cell_size - 4, self.cell_size - 4)

    def add_cells(self, cells):
        """Добавляет список коор-т ячеек к атакуемым ячейкам
        cells - список коор-т ячеек
        """
        self.attacked_cells += cells

    def reset_cells(self):
        """Обнуляет список атакуемых ячеек
        """
        self.attacked_cells = []
