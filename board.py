import numpy as np
import random


class BoardGame(object):
    def __init__(self, height=6, width=7):
        self.height = height
        self.width = width
        self.board = np.zeros((self.height, self.width))
        self.last_move = {"player": "NAN", "position": (10, 10)}
        self.Num_moves = 0
        self.game_over = False
        self.turn = 0
        return

    def drop_piece(self, row, col, player, temp_board=None):
        if temp_board is None:
            self.board[row][col] = player
            self.last_move["player"] = player
            self.last_move["position"] = (row, col)
        else:
            temp_board[row][col] = player
        # self.Num_moves += 1

    def is_valid_location(self, col):
        return self.board[5][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.height):
            if self.board[r][col] == 0:
                return r

    def winning_drop(self, piece):
        """Check for the winning drop every time a player drops a piece."""
        for c in range(self.width-3):
            for r in range(self.height):
                if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == piece:
                    return True

        # check vertical location
        for c in range(self.width):
            for r in range(self.height-3):
                if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == piece:
                    return True

        # check positive sloped location
        for c in range(self.width-3):
            for r in range(self.height-3):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == piece:
                    return True

        # check positive sloped location
        for c in range(self.width-3):
            for r in range(3, self.height):
                if self.board[r][c] == self.board[r-1][c-1] == self.board[r-2][c-2] == self.board[r-3][c-3] == piece:
                    return True

    def window_score(self, window, piece):
        opp_piece = 1
        score = 0
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, temp_board, piece):
        # score horizontal
        score = 0
        for r in range(self.height):
            row_array = [int(i) for i in list(temp_board[r, :])]
            for c in range(self.width-3):
                window = row_array[c:c+4]
                score += self.window_score(window, piece)
        return score

        # score vertical
        for c in range(self.width):
            col_array = [int(i) for i in list(temp_board[:, c])]
            for r in range(self.height-3):
                window = col_array[r:r+4]
                score += self.window_score(window, piece)

        # score positive diagonal
        for r in range(self.height-3):
            for c in range(self.width-3):
                window = [temp_board[r+i][c+i] for i in range(3)]
                score += self.window_score(window, piece)

        # score negative diagonal
        for r in range(self.height-3):
            for c in range(self.width-3):
                window = [temp_board[r+3-i][c+i] for i in range(3)]
                score += self.window_score(window, piece)

        return score

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.width):
            if self.is_valid_location(col):

                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, piece):
        valid_locations = self.get_valid_locations()
        best_score = 0
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(col)
            temp_board = self.board.copy()
            self.drop_piece(row, col, piece, temp_board)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def play(self):
        while not self.game_over:
            print(np.flip(self.board, 0))
            if self.turn == 0:
                self.turn = 1
                col = int(input("player 1 selection: "))
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, 1)
                    if self.winning_drop(1):
                        self.game_over = True
                        print("player 1 wins")
            else:
                self.turn = 0
                col = self.pick_best_move(2)
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, 2)
                    if self.winning_drop(2):
                        self.game_over = True
                        print("player 2 wins")

    def valid_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                try:
                    if self.board[row][col] == 0:
                        if not self.board[row - 1][col] == 0 or row == 0:
                            moves.append((row, col))
                except IndexError:
                    pass
        return moves


b = BoardGame()
b.play()


# print(b.board)
# print(b.valid_moves())
# print(b.check_winner())
