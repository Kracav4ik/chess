# encoding: utf-8

from __future__ import division

from attack import CellInfo

PIECE_SIZE = 48

diagonal_moves = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
knight_moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]]
hor_vert_moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]


_last_id = 0


def _new_id():
    global _last_id
    _last_id += 1
    return _last_id


class ChessPieceBase:
    """Шахматная фигура
    x, y - Ячейковые коорд-ты (0 .. 7)
    is_white - True если фигура белая иначе False
    id - уникальный идентификатор
    """
    def __init__(self, x, y, is_white, piece_id=None):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.id = piece_id if piece_id is not None else _new_id()

    def render_at(self, screen, pix_x, pix_y, pix_size):
        """Рисует фигуру в указанной ячейке
        screen - Экран
        pix_x, pix_y - коор-ты левого верхнего угла в пикселах
        pix_size - Размер ячейки в пикселях
        """
        color = [255, 255, 255, 168] if self.is_white else [0, 0, 0, 168]
        text_color = [0, 0, 0] if self.is_white else [255, 255, 255]
        pix_shift = (pix_size - PIECE_SIZE)/2
        screen.draw_rect(color, pix_x + pix_shift, pix_y + pix_shift, PIECE_SIZE, PIECE_SIZE)
        font = screen.get_font('Arial', 46)
        screen.draw_text(TEXT[self.__class__], font, text_color, pix_x, pix_y, pix_size, pix_size)

    def clone(self):
        """Создает идентичную копию фигуры
        """
        return self.__class__(self.x, self.y, self.is_white, self.id)

    def get_cells_to_move(self, grid):
        return self.get_attacked_cells(grid)
        # TODO сделать рокировки для короля

    def can_move(self, x, y, grid):
        """Возвращает True, если фигуру можно переместить в эту пустую ячейку
        x, y - Координата ячейки
        grid - Игровое поле
        """
        return [x, y] in self.get_cells_to_move(grid)

    def can_attack(self, x, y, grid):
        """Возвращает True, если фигура может атаковать данную ячейку
        х, у - Координата ячейки
        grid - Игровое поле
        """
        return [x, y] in self.get_attacked_cells(grid)

    def trace_directions(self, direction, grid, length=7):
        """Идем вдоль направлений от фигуры и возвращаем все клетки до первой встреченной фигуры
        direction - список направлений, пар [dx, dy]
            dx, dy - Шаги по осям соответствующих направлений
        grid - Игровое поле
        length - количество шагов по каждому из направлений
        """
        result = []
        for dx, dy in direction:
            for cell in range(1, length + 1):
                result.append([self.x + dx * cell, self.y + dy * cell])
                if grid.get_piece(self.x + dx * cell, self.y + dy * cell):
                    break
        return result

    def get_attacked_cells(self, grid):
        """Возвращает список атакуемых клеток
        grid - Игровое поле
        """


class King(ChessPieceBase):
    def get_cells_to_move(self, grid):
        """
        :type grid: grid.Grid
        """
        cells = ChessPieceBase.get_cells_to_move(self, grid)

        positions = [
            (0, 2),  # ладья на позиции 0, рокировка переставит короля на позицию 2
            (7, 6),  # ладья на позиции 7, рокировка переставит короля на позицию 6
        ]
        starting_row = 7 if self.is_white else 0
        if self.x == 4 and self.y == starting_row:
            for rook_x, castle_x in positions:
                castle_allowed = True
                piece = grid.get_piece(rook_x, starting_row)
                if isinstance(piece, Rook) and piece.is_white == self.is_white:
                    for x in range(min(rook_x, self.x) + 1, max(rook_x, self.x)):
                        if grid.get_piece(x, starting_row):
                            castle_allowed = False

                    if self.x > rook_x:
                        # длинная рокировка
                        begin_x = rook_x + 2
                        end_x = self.x + 1
                    else:
                        # короткая рокировка
                        begin_x = self.x
                        end_x = rook_x
                    for x in range(begin_x, end_x):
                        if CellInfo(x, starting_row, not piece.is_white) in grid.attack_grid.attacked_cells:
                            castle_allowed = False

                    if grid.game_history.is_piece_moved(self) or grid.game_history.is_piece_moved(piece):
                        castle_allowed = False

                    if castle_allowed:
                        cells += [[castle_x, starting_row]]
        return cells

    def get_attacked_cells(self, grid):
        return self.trace_directions(hor_vert_moves + diagonal_moves, grid, 1)


class Queen(ChessPieceBase):
    def get_attacked_cells(self, grid):
        return self.trace_directions(hor_vert_moves + diagonal_moves, grid)


class Rook(ChessPieceBase):
    def get_attacked_cells(self, grid):
        return self.trace_directions(hor_vert_moves, grid)


class Bishop(ChessPieceBase):
    def get_attacked_cells(self, grid):
        return self.trace_directions(diagonal_moves, grid)


class Knight(ChessPieceBase):
    def get_attacked_cells(self, grid):
        return self.trace_directions(knight_moves, grid, 1)


class Pawn(ChessPieceBase):
    def get_attacked_cells(self, grid):
        # TODO сделать взятие на проходе
        dy = -1 if self.is_white else 1
        return [[self.x - 1, self.y + dy], [self.x + 1, self.y + dy]]

    def get_cells_to_move(self, grid):
        dy = -1 if self.is_white else 1
        pawn_row = 6 if self.is_white else 1
        cells = [[self.x, self.y + dy]]
        if self.y == pawn_row and not grid.get_piece(self.x, self.y + dy):
            cells.append([self.x, self.y + 2 * dy])
        return cells


TEXT = {
    King: 'K',
    Queen: 'Q',
    Rook: 'R',
    Bishop: 'B',
    Knight: 'N',
    Pawn: 'P',
}
