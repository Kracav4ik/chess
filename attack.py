# encoding: utf-8

from __future__ import division


class CellInfo:
    def __init__(self, x, y, attacked_by_white):
        self.x = x
        self.y = y
        self.attacked_by_white = attacked_by_white

    def __eq__(self, other):
        if not isinstance(other, CellInfo):
            return False
        return self.x == other.x and self.y == other.y and self.attacked_by_white == other.attacked_by_white

    def __ne__(self, other):
        return not self.__eq__(other)


class SimpleAttackGrid:
    """Упрощенный объект с полями, которые атакованы фигурами; используется для расчета следующей позиции
    """
    def __init__(self):
        self.attacked_cells = []

    def add_cells(self, cells, is_white):
        """Добавляет список коор-т ячеек к атакуемым ячейкам
        cells - список коор-т ячеек
        is_white - является ли атакующая фигура белой
        """
        for x, y in cells:
            self.attacked_cells.append(CellInfo(x, y, is_white))


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
        width = self.cell_size // 2
        height = self.cell_size // 2
        white_attacked = {}
        black_attacked = {}
        font = screen.get_font('Arial Black', 20)
        white_color = [255, 255, 255]
        black_color = [0, 0, 0]
        for cell_info in self.attacked_cells:
            is_white = cell_info.attacked_by_white
            x = cell_info.x
            y = cell_info.y
            if not grid.good_coords(x, y):
                continue
            pix_x = x * self.cell_size + self.pix_x
            pix_y = y * self.cell_size + self.pix_y
            if is_white:
                white_attacked[pix_x, pix_y] = white_attacked.get((pix_x, pix_y), 0) + 1
            else:
                black_attacked[pix_x, pix_y] = black_attacked.get((pix_x, pix_y), 0) + 1

        for pix_x, pix_y in white_attacked.keys():
            text = str(white_attacked[pix_x, pix_y])
            screen.draw_text(text, font, white_color, pix_x, pix_y + height, width, height)

        for pix_x, pix_y in black_attacked.keys():
            text = str(black_attacked[pix_x, pix_y])
            screen.draw_text(text, font, black_color, pix_x + width, pix_y, width, height)

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
