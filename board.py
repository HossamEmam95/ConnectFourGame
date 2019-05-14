class BoardGame(object):
    def __init__(self, height=6, width=7):
        self.board = [["NAN" for y in range(height)] for x in range(width)]
        self.last_move = {"player": "NAN", "position": (10, 10)}
        self.Num_moves = 0
        return

    def move(self, row, col, player):
        self.board[row][col] = player
        self.last_move["player"] = player
        self.last_move["position"] = (row, col)
        self.Num_moves += 1

    def check_winner(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                try:
                    if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
                        return self.board[row][col]

                    if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
                        return self.board[row][col]

                    if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                        return self.board[row][col]

                    if self.board[row][col] == self.board[row + 3][col + 1] == self.board[row + 3][col + 2] == self.board[row + 3][col + 3]:
                        return self.board[row][col]
                except IndexError:
                    pass

        flag = 0
        for i in range(len(self.board)):
            if "NAN" in self.board[i]:
                flag = 1
                break

        if flag == 0:
            return 0

        return -1

    def is_valid_move(self, raw, col):
        pass

    def valid_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                try:
                    if self.board[row][col] == "NAN":
                        if not self.board[row - 1][col] == "NAN" or row == 0:
                            moves.append((row, col))
                except IndexError:
                    pass
        return moves



b = BoardGame()
for i in range(5):
    for j in range(3):
        t = 1
        b.move(i, j, t)


print(b.board)
print(b.valid_moves())
print(b.check_winner())