import random
import numpy as np
import utils
from utils import Player


class MinimaxPlayer(Player):
    def __init__(self):
        super().__init__()

    def next_move(self, board: np.ndarray):
        """
        TODO: replace the random picking with minimax
        :param board: TicTacToe board as 2D ndarray. It contains +1, -1 and 0 values.
                        +1 - player 1
                        -1 - player 2
                         0 - empty
        :return: row, col - position of the next move in board: board[row][col]
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col] == 0:
                    board[row][col] = self.MARKER  # Empty spot found, placing a marker
                    score = self.minimax(board, False, alpha, beta,5)
                    board[row][col] = 0  # Undo the move

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break  # Beta cut-off

        return best_move

    def minimax(self, board: np.ndarray, is_maximizing: bool, alpha, beta, depth):
        game_end, winner = utils.evaluate_board_state(board)

        if depth == 0 or game_end:
            if winner == self.MARKER:
                return 1  # Maximizer wins
            elif winner is None:
                return 0  # Draw
            else:
                return -1  # Minimizer wins

        if is_maximizing:
            best_score = float('-inf')
            for row in range(board.shape[0]):
                for col in range(board.shape[1]):
                    if board[row][col] == 0:
                        board[row][col] = self.MARKER
                        score = self.minimax(board, False, alpha, beta, depth - 1)
                        board[row][col] = 0  # Undo the move
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        if alpha >= beta:
                            return best_score  # Beta cut-off
            return best_score
        else:
            best_score = float('inf')
            for row in range(board.shape[0]):
                for col in range(board.shape[1]):
                    if board[row][col] == 0:
                        board[row][col] = -self.MARKER  # Other player's marker
                        score = self.minimax(board, True, alpha, beta, depth - 1)
                        board[row][col] = 0  # Undo the move
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            return best_score  # Alpha cut-off
            return best_score