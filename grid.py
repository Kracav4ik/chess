# encoding: utf-8

from __future__ import division
import os.path
import pygame
from attack import AttackGrid
from pieces import ChessPiece, KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN

HOVER_COLOR = [255, 255, 255]
CHESS_GRID = 8


class Grid:
    """Игровое поле,
    bg_x, bg_y - Координаты левого верхнего угла фона игрового поля
    bg_size - Размер фона игрового поля в пикселах
    offset_x, offset_y - Координаты левого верхнего угла игрового поля на экране в пикселах относительно фона
    cell_size - Размер клетки в пикселах
    active_cell - Коор-ты активной ячейки т.е. коор-ты ячейки где находится курсор мыши
    """
    def __init__(self, bg_x, bg_y, bg_size, offset_x, offset_y, cell_size):
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.bg_size = bg_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cell_size = cell_size
        self.active_cell = (0, 0)
        self.pieces = []
        self.active_piece = None
        self.mouse_pos = (0, 0)
        self.active_shift = (0, 0)
        self.is_whites_turn = True
        self.attack_grid = AttackGrid(offset_x + bg_x, offset_y + bg_y, cell_size)

        # Расставляем фигуры на доске
        for x in range(CHESS_GRID):
            self.place_mirrored(PAWN, x, 1)
        self.place_mirrored(KING, 4, 0)
        self.place_mirrored(QUEEN, 3, 0)
        for x, kind in enumerate([ROOK, KNIGHT, BISHOP]):
            self.place_mirrored(kind, x, 0)
            self.place_mirrored(kind, CHESS_GRID - 1 - x, 0)

        self.refresh_attack_cells()

        self.bg_texture = pygame.image.load(os.path.join('data', 'chessboard.png'))
        self.font = pygame.font.SysFont('Arial Black', 20)

    def place_mirrored(self, kind, black_x, black_y):
        """Ставит черную фигуру в заданную ячейку, и зеркально ей ставит такую же белую фигуру.
        Используется для расстановки фигур в начальной позиции.
        kind - Тип фигуры (Ферзь, король и т.д)
        black_x, black_y - Координаты ячейки для черной фигуры
        """
        self.pieces.append(ChessPiece(kind, black_x, black_y, False))
        self.pieces.append(ChessPiece(kind, black_x, CHESS_GRID - 1 - black_y, True))

    def render(self, screen):
        """ Отрисовка игрового поля
        :type screen: screen.Screen
        """
        # Рисуем фон
        screen.draw_texture(self.bg_texture, self.bg_x, self.bg_y, self.bg_size, self.bg_size)

        # Рисуем атакованные поля
        self.attack_grid.render(screen, self)

        # Рисуем чей ход
        if self.is_whites_turn:
            text = "White's turn"
            color = [255, 255, 255]
        else:
            text = "Black's turn"
            color = [0, 0, 0]
        screen.draw_text(text, self.font, color, self.bg_x, self.bg_y, self.bg_size, self.offset_y)

        # Рисуем фигуры на доске
        for piece in self.pieces:
            pix_x = self.offset_x + self.bg_x + piece.x * self.cell_size
            pix_y = self.offset_y + self.bg_y + piece.y * self.cell_size
            if piece == self.active_piece:
                continue
            piece.render_at(screen, pix_x, pix_y, self.cell_size)

        # Рисуем рамку поверх активной ячейки
        x, y = self.active_cell
        bg_x = x * self.cell_size + self.offset_x + self.bg_x
        bg_y = y * self.cell_size + self.offset_y + self.bg_y
        screen.draw_frame(HOVER_COLOR, bg_x, bg_y, self.cell_size, self.cell_size, 2)

        # Рисуем активную фигуру
        if self.active_piece:
            mouse_x, mouse_y = self.mouse_pos
            shift_x, shift_y = self.active_shift
            pix_x = self.offset_x + self.bg_x + mouse_x + shift_x
            pix_y = self.offset_y + self.bg_y + mouse_y + shift_y
            self.active_piece.render_at(screen, pix_x, pix_y, self.cell_size)

    def mouse_moved(self, pos):
        """Вызывается при движении мыши
        pos - координаты, список из двух чисел
        """
        self.mouse_pos = pos
        x, y = self.pixels_to_grid(pos)
        if not self.good_coords(x, y):
            return
        self.active_cell = (x, y)

    def convert_to_local(self, pos):
        """Получаем на вход пиксельные коор-ты относительно окна,
        возвращаем пиксельные коор-ты относительно игрового поля
        pos - координаты, список из двух чисел
        """
        x, y = pos
        return [x - self.bg_x - self.offset_x, y - self.bg_y - self.offset_y]

    def pixels_to_grid(self, pos):
        """Возвращает коор-ты в клетках из переданных коор-т в пикселах
        """
        pix_x, pix_y = pos
        x = pix_x // self.cell_size
        y = pix_y // self.cell_size
        return [x, y]

    @staticmethod
    def good_coords(x, y):
        """Возвращает True, если коор-ты х, у принадлежат ячейкам
        """
        return 0 <= x < CHESS_GRID and 0 <= y < CHESS_GRID

    def mouse_press(self, pos):
        """Вызывается при нажатии левой кнопки мыши
        pos - координаты, список из двух чисел
        """
        pos_x, pos_y = pos
        x, y = self.pixels_to_grid(pos)
        mouse_piece = self.get_piece(x, y)
        if not self.active_piece:
            # берем фигуру
            if mouse_piece and mouse_piece.is_white == self.is_whites_turn:
                self.active_piece = mouse_piece
                self.active_shift = [x * self.cell_size - pos_x, y * self.cell_size - pos_y]
        else:
            # ставим фигуру
            if mouse_piece == self.active_piece:
                # оставляем фигуру на своем месте
                self.active_piece = None
            elif self.good_coords(x, y):
                # нажатие было внутри игрового поля
                if mouse_piece and mouse_piece.is_white != self.active_piece.is_white and self.active_piece.can_attack(x, y, self):
                    # двигаем в клетку, занятую фигурой
                    self.pieces.remove(mouse_piece)
                    self.place_active_piece_at(x, y)
                elif not mouse_piece and self.active_piece.can_move(x, y, self):
                    # двигаем в пустую клетку
                    self.place_active_piece_at(x, y)

    def place_active_piece_at(self, x, y):
        """Ставит фигуру в ячейку и завершает ход
        x, y - ячейковые коор-ты
        """
        self.active_piece.x = x
        self.active_piece.y = y
        self.active_piece = None
        self.is_whites_turn = not self.is_whites_turn
        self.refresh_attack_cells()

    def get_piece(self, x, y):
        """Принимает ячейковые коор-ты. Возвращает фигуру, которая находися в этой коор-те, либо None если фигуры нет
        x, y - ячейковые коор-ты
        """
        for piece in self.pieces:
            if x == piece.x and y == piece.y:
                return piece

    def refresh_attack_cells(self):
        """Обновляет атакуемые клетки
        """
        self.attack_grid.reset_cells()
        for piece in self.pieces:
            self.attack_grid.add_cells(piece.get_attacked_cells(self))
