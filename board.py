class BoardGame(object):
    def __init__(self, height=6, width=7):
        self.height = height
        self.width = width
        self.board = [[0 for y in range(width)] for x in range(height)]
        self.last_move = {"player": "NAN", "position": (10, 10)}
        self.Num_moves = 0
        self.game_over = False
        self.turn = 0
        return

    def drop_piece(self, row, col, player):
        self.board[row][col] = player
        self.last_move["player"] = player
        self.last_move["position"] = (row, col)
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

    def play(self):
        while not self.game_over:
            for i in reversed(self.board):
                print(i)
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
                col = int(input("player 2 selection: "))
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
