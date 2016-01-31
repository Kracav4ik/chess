# encoding: utf-8

from __future__ import division
import pygame

KING = 'king'
QUEEN = 'queen'
ROOK = 'rook'
BISHOP = 'bishop'
KNIGHT = 'knight'
PAWN = 'pawn'

TEXT = {
    KING: 'K',
    QUEEN: 'Q',
    ROOK: 'R',
    BISHOP: 'B',
    KNIGHT: 'N',
    PAWN: 'P',
}
PIECE_SIZE = 48


class ChessPiece:
    """Шахматная фигура
    kind - Тип фигуры (Ферзь, король и т.д)
    x, y - Ячейковые коорд-ты (0 .. 7)
    is_white - True если фигура белая иначе False
    """
    def __init__(self, kind, x, y, is_white):
        self.kind = kind
        self.x = x
        self.y = y
        self.is_white = is_white

        self.font = pygame.font.SysFont('Arial', 46)

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
        screen.draw_text(TEXT[self.kind], self.font, text_color, pix_x, pix_y, pix_size, pix_size)

    def clone(self):
        """Создает идентичную копию фигуры
        """
        return ChessPiece(self.kind, self.x, self.y, self.is_white)

    def get_cells_to_move(self, grid):
        if self.kind == PAWN:
            # Пешка
            dy = -1 if self.is_white else 1
            pawn_row = 6 if self.is_white else 1
            cells = [[self.x, self.y + dy]]
            if self.y == pawn_row and not grid.get_piece(self.x, self.y + dy):
                cells.append([self.x, self.y + 2 * dy])
            return cells
        else:
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
        diagonal_moves = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        knight_moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]]
        hor_vert_moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        result = []
        if self.kind == PAWN:
            # Пешка
            # TODO сделать взятие на проходе
            dy = -1 if self.is_white else 1
            result = [[self.x - 1, self.y + dy], [self.x + 1, self.y + dy]]
        elif self.kind == BISHOP:
            # Слон
            result = self.trace_directions(diagonal_moves, grid)
        elif self.kind == ROOK:
            # Ладья
            result = self.trace_directions(hor_vert_moves, grid)
        elif self.kind == QUEEN:
            # Ферзь
            result = self.trace_directions(hor_vert_moves + diagonal_moves, grid)
        elif self.kind == KING:
            # Король
            result = self.trace_directions(hor_vert_moves + diagonal_moves, grid, 1)
        elif self.kind == KNIGHT:
            # Конь
            result = self.trace_directions(knight_moves, grid, 1)
        return result
