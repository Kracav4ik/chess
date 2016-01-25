# encoding: utf-8

from __future__ import division


class CellInfo:
    def __init__(self, x, y, attacked_by_white):
        self.x = x
        self.y = y
        self.attacked_by_white = attacked_by_white


class AttackGrid:
    """Поля, которые атакованы фигурами
    pix_x, pix_y - левый верхний угол
    cell_size - Размер клетки в пикселах
    attacked_cells - список атакуемых ячеек-объектов CellInfo
    """
    def __init__(self, pix_x, pix_y, cell_size):
        self.pix_x = pix_x
        self.pix_y = pix_y
        self.cell_size = cell_size
        self.attacked_cells = []

    def render(self, screen, grid):
        """ Отрисовка атакованных клеток
        :type screen: screen.Screen
        :type grid: grid.Grid
        """
        enemy_color = [255, 0, 0, 32]
        friend_color = [0, 255, 0, 32]
        for cell_info in self.attacked_cells:
            is_white = cell_info.attacked_by_white
            x = cell_info.x
            y = cell_info.y
            if not grid.good_coords(x, y):
                continue
            pix_x = x * self.cell_size + self.pix_x
            pix_y = y * self.cell_size + self.pix_y
            attacked_by_enemy = grid.is_whites_turn != is_white
            color = enemy_color if attacked_by_enemy else friend_color
            gap = 4
            border = 6
            triangle_leg = self.cell_size - border
            if is_white:
                points = [
                    (pix_x + border,             pix_y + border + gap),
                    (pix_x + border,             pix_y + triangle_leg),
                    (pix_x + triangle_leg - gap, pix_y + triangle_leg)
                ]
            else:
                points = [
                    (pix_x + border + gap, pix_y + border),
                    (pix_x + triangle_leg, pix_y + border),
                    (pix_x + triangle_leg, pix_y + triangle_leg - gap)
                ]
            screen.draw_polygon(color, points)

    def add_cells(self, cells, is_white):
        """Добавляет список коор-т ячеек к атакуемым ячейкам
        cells - список коор-т ячеек
        is_white - является ли атакующая фигура белой
        """
        for x, y in cells:
            self.attacked_cells.append(CellInfo(x, y, is_white))

    def reset_cells(self):
        """Обнуляет список атакуемых ячеек
        """
        self.attacked_cells = []
