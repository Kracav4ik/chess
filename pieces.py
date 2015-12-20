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
