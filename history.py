# encoding: utf-8

from __future__ import division


class PieceMove:
    def __init__(self, piece_id, to_x, to_y):
        self.piece_id = piece_id
        self.to_x = to_x
        self.to_y = to_y


class GameHistory:
    """
    История ходов
    """
    def __init__(self):
        self.white_moves = []
        self.black_moves = []

    def add_move(self, piece, x, y):
        """
        :type piece: pieces.ChessPieceBase
        """
        moves_list = self.white_moves if piece.is_white else self.black_moves
        moves_list.append(PieceMove(piece.id, x, y))

    def is_piece_moved(self, piece):
        """ Получает на вход фигуру вовзращает True если фигура есть в истории ходов, иначе False
        :type piece: pieces.ChessPieceBase
        """
        moves_list = self.white_moves if piece.is_white else self.black_moves
        for move in moves_list:
            if piece.id == move.piece_id:
                return True
        return False
