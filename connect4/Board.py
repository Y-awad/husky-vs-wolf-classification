import numpy as np
class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)

    def play_disc(self, player, column):
        if self.valid_move(column):
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = player.symbol
                    break

    def valid_move(self, column):
        return self.board[0][column] == 0

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.valid_move(col)]

    def undo_move(self, column):
        for row in range(self.rows):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                break

    def print_board(self):
        for row in self.board:
            print(" ".join(str(int(cell)) if cell != 0 else '.' for cell in row))

    def is_full(self):
        return np.all(self.board != 0)

    def check_line(self, start_row, start_col, delta_row, delta_col, player_symbol):
        count = 0
        for i in range(4):
            row = start_row + i * delta_row
            col = start_col + i * delta_col
            if 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] == player_symbol:
                count += 1
            else:
                break
        return count == 4

    def count_connected_fours(self, player_symbol):
        """Count all connected fours for the given player symbol."""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == player_symbol:
                    # Check all directions
                    if self.check_line(row, col, 0, 1, player_symbol):  # Horizontal
                        count += 1
                    if self.check_line(row, col, 1, 0, player_symbol):  # Vertical
                        count += 1
                    if self.check_line(row, col, 1, 1, player_symbol):  # Diagonal /
                        count += 1
                    if self.check_line(row, col, 1, -1, player_symbol):  # Diagonal \
                        count += 1
        return count

    def evaluate_board(self, ai_symbol, opponent_symbol):
        """Evaluate the board with a more detailed heuristic."""
        score = 0

        # Center column control
        center_column = self.board[:, self.cols // 2]
        center_count_ai = np.count_nonzero(center_column == ai_symbol)
        score += center_count_ai * 3  # Weighted bonus for center discs

        center_count_opponent = np.count_nonzero(center_column == opponent_symbol)
        score -= center_count_opponent * 3  # Penalize opponent's center control

        # Evaluate rows, columns, and diagonals
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == ai_symbol:
                    # Horizontal
                    if self.check_line(row, col, 0, 1, ai_symbol):
                        score += 100  # AI's winning line
                    elif self.check_open_three(row, col, 0, 1, ai_symbol):
                        score += 5  # AI's open 3

                    # Vertical
                    if self.check_line(row, col, 1, 0, ai_symbol):
                        score += 100
                    elif self.check_open_three(row, col, 1, 0, ai_symbol):
                        score += 5

                    # Diagonal / (up-right)
                    if self.check_line(row, col, 1, 1, ai_symbol):
                        score += 100
                    elif self.check_open_three(row, col, 1, 1, ai_symbol):
                        score += 5

                    # Diagonal \ (up-left)
                    if self.check_line(row, col, 1, -1, ai_symbol):
                        score += 100
                    elif self.check_open_three(row, col, 1, -1, ai_symbol):
                        score += 5

                elif self.board[row][col] == opponent_symbol:
                    # Horizontal
                    if self.check_line(row, col, 0, 1, opponent_symbol):
                        score -= 100  # Opponent's winning line
                    elif self.check_open_three(row, col, 0, 1, opponent_symbol):
                        score -= 50  # Opponent's open 3

                    # Vertical
                    if self.check_line(row, col, 1, 0, opponent_symbol):
                        score -= 100
                    elif self.check_open_three(row, col, 1, 0, opponent_symbol):
                        score -= 50

                    # Diagonal / (up-right)
                    if self.check_line(row, col, 1, 1, opponent_symbol):
                        score -= 100
                    elif self.check_open_three(row, col, 1, 1, opponent_symbol):
                        score -= 50

                    # Diagonal \ (up-left)
                    if self.check_line(row, col, 1, -1, opponent_symbol):
                        score -= 100
                    elif self.check_open_three(row, col, 1, -1, opponent_symbol):
                        score -= 50

        return score

    def check_open_three(self, start_row, start_col, delta_row, delta_col, player_symbol):
        """Check if there's an open three-in-a-row for the given player."""
        count = 0
        empty_count = 0
        for i in range(4):
            row = start_row + i * delta_row
            col = start_col + i * delta_col
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if self.board[row][col] == player_symbol:
                    count += 1
                elif self.board[row][col] == 0:
                    empty_count += 1
            else:
                break
        return count == 3 and empty_count == 1

    def get_scores(self, ai_symbol, opponent_symbol):
        ai_score = self.count_connected_fours(ai_symbol)
        opponent_score = self.count_connected_fours(opponent_symbol)
        return ai_score , opponent_score