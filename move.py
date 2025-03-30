from abc import ABC, abstractmethod


class Command:
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class MoveCommand(Command):

    def __init__(self, board, piece, position, player, fake_move=False):
        self.board = board
        self.piece = piece
        self.player = player
        self.position = position
        self.fake_move = fake_move
        self.piece_position = piece.get_position()
        self.captured_piece = board.board[position[0]][position[1]]

    def execute(self):
        if not self.is_valid_move():
            if not self.fake_move:
                print("Move outside of chess board")
            return False

        if self.piece.is_valid_move(board=self.board, position=self.position):
            self.board.board[self.piece_position[0]][self.piece_position[1]] = None
            r, c = self.position
            self.board.board[r][c] = self.piece
            self.piece.update_position(self.position[0], self.position[1])

            self.print_move("Move")

            return True
        else:
            if not self.fake_move:
                print(f"{self.piece_position} -> {self.position} Not a valid move")
            return False

    def undo(self):
        self.board.board[self.position[0]][self.position[1]] = None
        self.board.board[self.piece_position[0]][self.piece_position[1]] = self.piece
        self.piece.update_position(self.piece_position[0], self.piece_position[1])
        if self.captured_piece:
            self.board.place_piece(self.captured_piece, self.position[0], self.position[1])

        self.print_move("UNDO Move")

        return True

    def print_move(self, move_type):
        if not self.fake_move:
            print("==========================================")
            print(f"-----> {self.player} {move_type} {type(self.piece)} - {self.piece_position} , {self.position}")
            self.board.print_board()

    def is_valid_move(self):
        if 0 <= self.position[0] < 8 and 0 <= self.position[1] < 8:
            return True
        return False
