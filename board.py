import numpy as np
import random
import pygame
import sys
import math

COLUMN_COUNT = 7
ROW_COUNT = 6
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+2) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)


class BoardGame(object):
    def __init__(self, id=0, height=6, width=7):
        self.id = id
        self.height = height
        self.width = width
        self.board = np.zeros((self.height, self.width))
        self.last_move = {"player": "NAN", "position": (10, 10)}
        self.Num_moves = 0
        self.game_over = False
        self.turn = 0
        return

    def drop_piece(self, row, col, player, temp_board=None):
        if not temp_board:
            self.board[row][col] = player
            self.last_move["player"] = player
            self.last_move["position"] = (row, col)
        else:
            print("id", temp_board.id)
            temp_board.board[row][col] = player
            temp_board.last_move["player"] = player
            temp_board.last_move["position"] = (row, col)
        # self.Num_moves += 1

    def is_valid_location(self, col):
        return self.board[5][col] == 0

    def get_next_open_row(self, col, temp=None):
        if temp:
            for r in range(temp.height):
                if temp.board[r][col] == 0:
                    return r
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
        # check positive sloped location
        for c in range(self.width - 3):
            for r in range(3, self.height):
                if self.board[r][c] == self.board[r - 1][c + 1] == self.board[r - 2][c + 2] == self.board[r - 3][c + 3] == piece:
                    return True

    def window_score(self, window, piece):
        opp_piece = 1
        score = 0
        if window.count(piece) == 4:
            score += 10
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 6
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 3
        elif window.count(piece) == 1 and window.count(0) == 3:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 9

        if window.count(opp_piece) == 2 and window.count(0) == 2:
            score -= 5

        return score

    def score_position(self, temp_board, piece):
        # score horizontal
        score = 0
        for r in range(self.height):
            row_array = [int(i) for i in list(temp_board[r, :])]
            for c in range(self.width-3):
                window = row_array[c:c+4]
                score += self.window_score(window, piece)

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

    # def pick_best_move(self, piece):
    #     valid_locations = self.get_valid_locations()
    #     best_score = 0
    #     best_col = random.choice(valid_locations)
    #     for col in valid_locations:
    #         row = self.get_next_open_row(col)
    #         temp_board = self.copy()
    #         self.drop_piece(row, col, piece, temp_board)
    #         score = self.score_position(temp_board, piece)
    #         if score > best_score:
    #             best_score = score
    #             best_col = col
    #     return best_col

    def copy_board(self):
        b = BoardGame()
        b.board = self.board.copy()
        b.id = self.id + 1
        return b

    def rand_move(self):
        valid_locations = self.get_valid_locations()
        return random.choice(valid_locations)

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


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE +
                                            SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE//2,
                                               r*SQUARESIZE+SQUARESIZE+SQUARESIZE+SQUARESIZE//2), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE//2,
                                                 height-(r*SQUARESIZE+SQUARESIZE//2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE//2,
                                                    height-(r*SQUARESIZE+SQUARESIZE//2)), RADIUS)
    pygame.display.update()


def minimax(board, depth, alpha, beta, maximizingPlayer):
    # print(board.board, '\n')
    valid_locations = board.get_valid_locations()
    # column = random.choice(valid_locations)
    # value = 10
    if depth == 0 or board.game_over:
        if board.game_over:
            if board.winning_drop(2):
                return None, 100000000000000
            elif board.winning_drop(1):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, board.score_position(board.board, 2)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = board.copy_board()
            board.drop_piece(row, col, 2, b_copy)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            print("new_score: ", new_score, "   col:", col)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        print("min")
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            b_copy = board.copy_board()
            board.drop_piece(row, col, 1, b_copy)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
    return column, value


def play(board):
    # label = myfont.render("PLayer 1 wins!!", 1, RED)
    # screen.blit(label, (40, 10))
    flag = 0  # player input > 0 , depth input > 1, start game > 2
    depth = None
    while not board.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pygame.draw.rect(screen, BLUE, (0, 0, SQUARESIZE*7, SQUARESIZE))
            pygame.draw.circle(screen, RED, (SQUARESIZE//2,
                                             SQUARESIZE//2), RADIUS)
            pygame.draw.circle(screen, YELLOW, (SQUARESIZE+SQUARESIZE//2,
                                                SQUARESIZE//2), RADIUS)
            if flag == 1:
                pygame.draw.circle(screen, GREEN, (board.turn*SQUARESIZE+SQUARESIZE//2,
                                                   SQUARESIZE//2), RADIUS)
            for i in range(2, 7):
                pygame.draw.circle(screen, BLACK, (i*SQUARESIZE+SQUARESIZE//2,
                                                   SQUARESIZE//2), RADIUS)
                label = myfont.render(str(i-2), 1, RED)
                screen.blit(label, (i*100+15, 10))
                if depth:
                    pygame.draw.circle(screen, GREEN, ((depth+2)*SQUARESIZE+SQUARESIZE//2,
                                                       SQUARESIZE//2), RADIUS)
            pygame.display.update()

            if flag == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                # print(posx)
                col = int(math.floor(posx/SQUARESIZE))
                if col == 0:
                    board.turn = 0
                else:
                    board.turn = 1
                print(board.turn)
                flag = 1
                continue

            if flag == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 100, width, SQUARESIZE))
                posx = event.pos[0]
                depth = int(math.floor(posx/SQUARESIZE)) - 2
                if depth < 0:
                    depth = 0
                flag = 2
                continue
                print(depth)

            if flag == 2 and event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 100, width, SQUARESIZE))
                posx = event.pos[0]
                if board.turn == 0:
                    pygame.draw.circle(screen, RED, (posx, SQUARESIZE+SQUARESIZE//2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 100, width, SQUARESIZE))

                # player 1 move
                if board.turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    if board.is_valid_location(col):
                        row = board.get_next_open_row(col)
                        board.drop_piece(row, col, 1)
                        if board.winning_drop(1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 110))
                            board.game_over = True

                        board.turn = 1
                        draw_board(board.board)
        # AI move
        if flag == 2:
            if board.turn == 1 and not board.game_over:
                print("ai move")
                # col = self.pick_best_move(2)
                b = board.copy_board()
                # depth = 4
                print("depth: ", depth)
                if depth == 0:
                    col = board.rand_move()
                else:
                    col, score = minimax(b, depth, -math.inf, math.inf, True)
                    print("col:", col, "  score", score)
                if board.is_valid_location(col):
                    row = board.get_next_open_row(col)
                    board.drop_piece(row, col, 2)
                    if board.winning_drop(2):
                        label = myfont.render("Player 2 wins!!", 1, BLUE)
                        screen.blit(label, (40, 110))
                        board.game_over = True

                    board.turn = 0
                    draw_board(board.board)
                else:
                    print("not valid col")

        if board.game_over:
            pygame.time.wait(3000)


pygame.init()
b = BoardGame()
screen = pygame.display.set_mode(size)
draw_board(b.board)
pygame.display.update()
myfont = pygame.font.SysFont("Arial", 75)
play(b)


# print(b.board)
# print(b.valid_moves())
# print(b.check_winner())
