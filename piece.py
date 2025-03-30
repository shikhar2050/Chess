from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.dis_name = f'\033[4m{self.color[0].upper()}{type(self).__name__[:2].upper()}{self.row}{self.col}\033[0m'

    def is_valid_move(self, board, position):
        raise NotImplementedError

    def update_position(self, row, col):
        self.row = row
        self.col = col

    def get_position(self):
        return self.row, self.col

    def get_color(self):
        return self.color

    def __str__(self):
        return f'{self.dis_name}'


class Pawn(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position
        dir = -1 if self.color == "Black" else 1

        # Move Front (if no other piece is present)
        if self.col == n_col and n_row == self.row + dir:
            return board.is_empty(n_row, n_col)

        # Move diagonal (if enemy present)
        if (self.col - 1 == n_col or self.col + 1 == n_col) and n_row == self.row + dir:
            return board.has_enemy_piece(n_row, n_col, self.color)

        return False


class Rook(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position

        if n_row == self.row or n_col == self.col:
            row_inc, col_inc = 0, 0
            if self.col == n_col:
                row_inc = 1 if (n_row - self.row) > 0 else -1
            else:
                col_inc = 1 if (n_col - self.col) > 0 else -1

            row = self.row + row_inc
            col = self.col + col_inc

            while (row, col) != (n_row, n_col):
                if not board.is_empty(row, col):
                    return False
                row += row_inc
                col += col_inc

            return board.is_empty(row, col) or board.has_enemy_piece(row, col, self.color)

        return False


class Knight(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position
        possible_position_changes = [
            (2, 1), (1, 2),
            (-2, 1), (-1, 2),
            (2, -1), (1, -2),
            (-2, -1), (-1, -2)
        ]

        for x, y in possible_position_changes:
            if self.row + x == n_row and self.col + y == n_col:
                return board.is_empty(n_row, n_col) or board.has_enemy_piece(n_row, n_col, self.color)

        return False


class Bishop(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position
        if not abs(self.row - n_row) == abs(self.col - n_col):
            return False

        row_inc = 1 if (n_row - self.row) > 0 else -1
        col_inc = 1 if (n_col - self.col) > 0 else -1

        row = self.row + row_inc
        col = self.col + col_inc

        while (row, col) != (n_row, n_col):
            if not board.is_empty(row, col):
                return False
            row += row_inc
            col += col_inc

        return board.is_empty(row, col) or board.has_enemy_piece(row, col, self.color)


class King(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position
        abs_row = abs(n_row - self.row)
        abs_col = abs(n_col - self.col)

        if 0 <= abs_row <= 1 and 0 <= abs_col <= 1 and abs_row + abs_col != 0:
            return board.is_empty(n_row, n_col) or board.has_enemy_piece(n_row, n_col, self.color)

        return False


class Queen(Piece):
    def is_valid_move(self, board, position):
        n_row, n_col = position

        # Straight Path
        if n_row == self.row or n_col == self.col:
            row_inc, col_inc = 0, 0
            if self.col == n_col:
                row_inc = 1 if (n_row - self.row) > 0 else -1
            else:
                col_inc = 1 if (n_col - self.col) > 0 else -1

            row = self.row + row_inc
            col = self.col + col_inc

            while (row, col) != (n_row, n_col):
                if not board.is_empty(row, col):
                    return False
                row += row_inc
                col += col_inc

            return board.is_empty(row, col) or board.has_enemy_piece(row, col, self.color)

        # Diagonal Path
        if abs(self.row - n_row) == abs(self.col - n_col):
            row_inc = 1 if (n_row - self.row) > 0 else -1
            col_inc = 1 if (n_col - self.col) > 0 else -1

            row = self.row + row_inc
            col = self.col + col_inc

            while (row, col) != (n_row, n_col):
                if not board.is_empty(row, col):
                    return False
                row += row_inc
                col += col_inc

            return board.is_empty(row, col) or board.has_enemy_piece(row, col, self.color)

        return False


class PieceFactory:

    @staticmethod
    def create(ptype, color, row, col):
        if ptype == 'Pawn':
            return Pawn(color, row, col)
        elif ptype == 'Rook':
            return Rook(color, row, col)
        elif ptype == 'Knight':
            return Knight(color, row, col)
        elif ptype == 'Bishop':
            return Bishop(color, row, col)
        elif ptype == 'King':
            return King(color, row, col)
        else:
            return Queen(color, row, col)
