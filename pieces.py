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

        self.font = pygame.font.SysFont('Arial', 70)

    def render_at(self, screen, pix_x, pix_y, pix_size):
        """Рисует фигуру в указанной ячейке
        screen - Экран
        pix_x, pix_y - коор-ты левого верхнего угла в пикселах
        pix_size - Размер ячейки в пикселях
        """
        color = [255, 255, 255] if self.is_white else [0, 0, 0]
        text_color = [0, 0, 0] if self.is_white else [255, 255, 255]
        screen.draw_rect(color, pix_x + 2, pix_y + 2, pix_size - 4, pix_size - 4)
        screen.draw_text(TEXT[self.kind], self.font, text_color, pix_x, pix_y, pix_size, pix_size)

    def can_move(self, x, y, grid):
        """Возвращает True, если фигуру можно переместить в эту пустую ячейку
        x, y - Координата ячейки
        grid - Игровое поле
        """
        if self.kind == PAWN:
            # Пешка
            if self.x == x:
                dy = -1 if self.is_white else 1
                pawn_row = 6 if self.is_white else 1
                return self.y + dy == y or self.y == pawn_row and not grid.get_piece(x, self.y + dy) and self.y + 2 * dy == y
            else:
                return False
        elif self.kind == KNIGHT:
            # Конь
            return abs(self.x - x) == 1 and abs(self.y - y) == 2 or abs(self.x - x) == 2 and abs(self.y - y) == 1
        elif self.kind == BISHOP:
            # Слон
            return abs(self.x - x) == abs(self.y - y)
        elif self.kind == ROOK:
            # Ладья
            if self.x == x:
                step = 1 if self.y < y else -1
                for cell_y in range(self.y + step, y, step):
                    if grid.get_piece(x, cell_y):
                        return False
                return True
            elif self.y == y:
                step = 1 if self.x < x else -1
                for cell_x in range(self.x + step, x, step):
                    if grid.get_piece(cell_x, y):
                        return False
                return True
        elif self.kind == QUEEN:
            # Ферзь
            return abs(self.x - x) == abs(self.y - y) or self.x == x or self.y == y
        else:
            # Король
            # TODO сделать рокировки
            return abs(self.x - x) <= 1 and abs(self.y - y) <= 1

    def can_attack(self, x, y, grid):
        """Возвращает True, если фигура может атаковать данную ячейку
        х, у - Координата ячейки
        grid - Игровое поле
        """
        if self.kind == PAWN:
            # Пешка
            dy = -1 if self.is_white else 1
            return self.y + dy == y and abs(self.x - x) == 1
            # TODO сделать взятие на проходе
        else:
            return self.can_move(x, y, grid)
