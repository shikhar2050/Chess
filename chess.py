from itertools import cycle

import constants
from move import MoveCommand
from piece import PieceFactory, King


class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.moves = []
        self.curr_player = cycle([constants.WHITE, constants.BLACK])
        self.winner = None

    def place_piece(self, piece, row=None, col=None):
        if not row:
            self.board[piece.row][piece.col] = piece
        else:
            self.board[row][col] = piece
        return self

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end="\t")
            print()

    def is_empty(self, row, col):
        return False if self.board[row][col] else True

    def has_enemy_piece(self, row, col, color):
        return True if self.board[row][col] and self.board[row][col].get_color() != color else False

    @staticmethod
    def get_enemy_color(player_color):
        return constants.WHITE if player_color == constants.BLACK else constants.BLACK

    def move_piece(self, start, end):
        curr_player = next(self.curr_player)
        row, col = start
        piece = self.board[row][col]
        if not piece:
            raise Exception(f"Piece at position {start} not found")

        move = MoveCommand(self, piece, end, curr_player)
        status = move.execute()
        if not status:
            return

        self.moves.append(move)

        enemy_color = self.get_enemy_color(curr_player)
        if self.is_checkmate(enemy_color) or self.is_stalemate(enemy_color):
            print(f"Winner is {curr_player}")
            return

        self.is_king_in_check(Board.get_enemy_color(curr_player))

    def undo_move(self):
        last_move = self.moves.pop()
        last_move.undo()

    def is_king_in_check(self, color):
        king_piece = None

        for row in self.board:
            for piece in row:
                if piece and piece.get_color() == color and isinstance(piece, King):
                    king_piece = piece
                    break
            if king_piece:
                break

        if not king_piece:
            return False

        position = (king_piece.row, king_piece.col)

        for row in self.board:
            for piece in row:
                if piece and piece.get_color() != color and piece.is_valid_move(self, position):
                    print(f"[{color.upper()} king {str(king_piece)} is in CHECK !!!]")
                    return True

        print(f"[{color.upper()} king {str(king_piece)} is SAFE :)]")
        return False

    def is_checkmate(self, color):
        if not self.is_king_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.get_color() == color:
                    for n_row in range(8):
                        for n_col in range(8):
                            end = (n_row, n_col)
                            move = MoveCommand(self, piece, end, color, fake_move=True)
                            status = move.execute()
                            if not status:
                                continue

                            is_check = self.is_king_in_check(color)
                            move.undo()

                            if not is_check:
                                return False

        print(f"{color} is Checkmate")
        return True

    def is_stalemate(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.get_color() == color:
                    for n_row in range(8):
                        for n_col in range(8):
                            end = (n_row, n_col)
                            move = MoveCommand(self, piece, end, color, fake_move=True)
                            status = move.execute()
                            if status:
                                move.undo()
                                return False

        print(f"{color} is Stalemate")
        return True


def setup_board():
    chess_board = Board()

    # black
    color = "Black"
    chess_board. \
        place_piece(PieceFactory.create('Pawn', color, 6, 0)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 1)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 2)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 3)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 4)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 5)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 6)). \
        place_piece(PieceFactory.create('Pawn', color, 6, 7)). \
        place_piece(PieceFactory.create('Rook', color, 7, 0)). \
        place_piece(PieceFactory.create('Rook', color, 7, 7)). \
        place_piece(PieceFactory.create('Knight', color, 7, 1)). \
        place_piece(PieceFactory.create('Knight', color, 7, 6)). \
        place_piece(PieceFactory.create('Bishop', color, 7, 2)). \
        place_piece(PieceFactory.create('Bishop', color, 7, 5)). \
        place_piece(PieceFactory.create('King', color, 7, 3)). \
        place_piece(PieceFactory.create('Queen', color, 7, 4))

    # White
    color = "White"
    chess_board. \
        place_piece(PieceFactory.create('Pawn', color, 1, 0)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 1)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 2)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 3)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 4)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 5)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 6)). \
        place_piece(PieceFactory.create('Pawn', color, 1, 7)). \
        place_piece(PieceFactory.create('Rook', color, 0, 0)). \
        place_piece(PieceFactory.create('Rook', color, 0, 7)). \
        place_piece(PieceFactory.create('Knight', color, 0, 1)). \
        place_piece(PieceFactory.create('Knight', color, 0, 6)). \
        place_piece(PieceFactory.create('Bishop', color, 0, 2)). \
        place_piece(PieceFactory.create('Bishop', color, 0, 5)). \
        place_piece(PieceFactory.create('King', color, 0, 3)). \
        place_piece(PieceFactory.create('Queen', color, 0, 4))

    return chess_board


def simple_setup():
    chess_board = Board()

    # black
    color = "Black"
    chess_board. \
        place_piece(PieceFactory.create('Pawn', color, 5, 0)). \
        place_piece(PieceFactory.create('Pawn', color, 3, 2)). \
        place_piece(PieceFactory.create('Rook', color, 7, 4)). \
        place_piece(PieceFactory.create('King', color, 6, 0))

    # White
    color = "White"
    chess_board. \
        place_piece(PieceFactory.create('Pawn', color, 2, 0)). \
        place_piece(PieceFactory.create('Pawn', color, 4, 1)). \
        place_piece(PieceFactory.create('Pawn', color, 2, 6)). \
        place_piece(PieceFactory.create('Rook', color, 3, 0)). \
        place_piece(PieceFactory.create('King', color, 1, 0))

    return chess_board


def test_setup():
    chess_board = Board()

    # White
    color = "White"
    chess_board. \
        place_piece(PieceFactory.create('Queen', color, 3, 3))

    return chess_board


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board = setup_board()
    board.print_board()

    # Checkmate move
    board.move_piece((1, 1), (2, 1))
    board.move_piece((6, 3), (5, 3))
    board.move_piece((2, 1), (3, 1))
    board.move_piece((6, 4), (5, 4))
    board.move_piece((1, 2), (2, 2))
    board.move_piece((7, 4), (3, 0))

    # Normal moves
    # board.move_piece((1, 0), (2, 0))
    # board.move_piece((6, 1), (5, 1))
    # board.move_piece((2, 0), (3, 0))
    # board.move_piece((5, 1), (4, 1))
    # board.move_piece((0, 0), (2, 0))
    # board.move_piece((6, 0), (5, 0))
    # board.move_piece((2, 0), (2, 1))
    # board.move_piece((5, 0), (4, 0))
    # board.move_piece((2, 1), (4, 1))
    # board.undo_move()
    # board.undo_move()

    # board = simple_setup()
    # board.print_board()
    # board.move_piece((2, 6), (3, 6))
    # board.move_piece((7, 4), (1, 4))

    # board = test_setup()
    # board.print_board()
    # board.move_piece((3, 3), (5, 5))
    # board.move_piece((5, 5), (3, 3))
    #
    # board.move_piece((3, 3), (1, 1))
    # board.move_piece((1, 1), (3, 3))
    #
    # board.move_piece((3, 3), (5, 1))
    # board.move_piece((5, 1), (3, 3))
    #
    # board.move_piece((3, 3), (1, 5))
    # board.move_piece((1, 5), (3, 3))
    #
    # board.move_piece((3, 3), (5, 3))
    # board.move_piece((5, 3), (3, 3))
    #
    # board.move_piece((3, 3), (3, 5))
    # board.move_piece((3, 5), (3, 3))
