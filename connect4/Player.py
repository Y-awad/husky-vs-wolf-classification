import time 
class Player:
    def __init__(self, name, symbol,depth=4, is_ai=False, algorithm="minimax",):
        self.name = name
        self.symbol = symbol
        self.is_ai = is_ai
        self.algorithm = algorithm
        self.depth = depth  

    def make_move(self, board):
        if self.is_ai:
            print(f"{self.name} (AI) is making a move...\n")

            start_time = time.time()
            # Choose the algorithm
            if self.algorithm == "minimax":
                score, col, self.nodes_expanded = self.minimax(board, self.depth, maximizing=True, indent=0)
            elif self.algorithm == "alphabeta":
                score, col, self.nodes_expanded = self.minimax_with_alphabeta(board,self.depth, maximizing=True, alpha=float('-inf'), beta=float('inf'), indent=0)
            elif self.algorithm == "expected_minimax":
                score, col, self.nodes_expanded = self.expected_minimax(board,self.depth, maximizing=True, indent=0)

            end_time = time.time()

            print(f"\n{self.name} chooses column {col} with score {score}\n")
            board.play_disc(self, col)
            return end_time - start_time
        else:
            col = self.get_human_move(board)
            board.play_disc(self, col)

    def get_human_move(self, board):
        while True:
            try:
                col = int(input(f"{self.name} ({self.symbol}), choose a column (0-{board.cols - 1}): "))
                if board.valid_move(col):
                    return col
                else:
                    print("Invalid column. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def minimax(self, board, depth, maximizing, indent=0 , nodes_expanded=None):
        """Minimax (No Alpha-Beta pruning)"""

        if nodes_expanded is None:
             nodes_expanded = [0]  

        nodes_expanded[0] += 1
        prefix = "    " * indent
        print(f"{prefix}{'Maximizing' if maximizing else 'Minimizing'} at depth {depth}")
        board.print_board()
        print()

        if depth == 0 or board.is_full():
            score = board.evaluate_board(self.symbol, 3 - self.symbol)
            print(f"{prefix}Leaf node reached with score: {score}")
            return score, None, nodes_expanded

        valid_moves = board.get_valid_moves()

        # Reorder moves to prioritize center columns
        center = board.cols // 2
        valid_moves.sort(key=lambda col: abs(center - col))

        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                board.play_disc(self, col)
                print(f"{prefix}Exploring move at column {col}")
                eval_score, _, nodes_expanded = self.minimax(board, depth - 1, False, indent + 1, nodes_expanded)
                board.undo_move(col)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

            print(f"{prefix}Best score for maximizing: {max_eval}, Move: {best_move}\n")
            return max_eval, best_move, nodes_expanded
        else:
            min_eval = float('inf')
            for col in valid_moves:
                opponent = Player("Opponent", 3 - self.symbol)
                board.play_disc(opponent, col)
                print(f"{prefix}Exploring move at column {col}")
                eval_score, _ , nodes_expanded = self.minimax(board, depth - 1, True, indent + 1, nodes_expanded)
                board.undo_move(col)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col

            print(f"{prefix}Best score for minimizing: {min_eval}, Move: {best_move}\n")
            return min_eval, best_move, nodes_expanded

    def minimax_with_alphabeta(self, board, depth, maximizing, alpha, beta, indent=0, nodes_expanded=None):
        """Minimax with Alpha-Beta pruning, prioritizing the center column"""

        if nodes_expanded is None:  
            nodes_expanded = [0]    

        nodes_expanded[0] += 1
        prefix = "    " * indent
        print(f"{prefix}{'Maximizing' if maximizing else 'Minimizing'} at depth {depth}")
        board.print_board()
        print()

        if depth == 0 or board.is_full():
            score = board.evaluate_board(self.symbol, 3 - self.symbol)
            print(f"{prefix}Leaf node reached with score: {score}")
            return score, None, nodes_expanded

        valid_moves = board.get_valid_moves()
        center_col = board.cols // 2
        valid_moves.sort(key=lambda x: abs(x - center_col))  # Prioritize center column

        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                board.play_disc(self, col)
                print(f"{prefix}Exploring move at column {col}")
                eval_score, _, nodes_expanded = self.minimax_with_alphabeta(board, depth - 1, False, alpha, beta, indent + 1, nodes_expanded)
                board.undo_move(col)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

                # Alpha-Beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    print(f"{prefix}Pruning branch at column {col}")
                    break

            print(f"{prefix}Best score for maximizing: {max_eval}, Move: {best_move}\n")
            return max_eval, best_move, nodes_expanded
        else:
            min_eval = float('inf')
            for col in valid_moves:
                opponent = Player("Opponent", 3 - self.symbol)
                board.play_disc(opponent, col)
                print(f"{prefix}Exploring move at column {col}")
                eval_score, _ , nodes_expanded = self.minimax_with_alphabeta(board, depth - 1, True, alpha, beta, indent + 1, nodes_expanded)
                board.undo_move(col)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col

                # Alpha-Beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    print(f"{prefix}Pruning branch at column {col}")
                    break

            print(f"{prefix}Best score for minimizing: {min_eval}, Move: {best_move}\n")
            return min_eval, best_move, nodes_expanded
            
    def expected_minimax(self, board, depth, maximizing, indent=0, nodes_expanded=None):
        """Expected Minimax (Probabilistic) with Center Column Priority"""

        if nodes_expanded is None:  
            nodes_expanded = [0]    

        nodes_expanded[0] += 1
        prefix = "    " * indent
        print(f"{prefix}{'Maximizing' if maximizing else 'Minimizing'} at depth {depth}")
        board.print_board()
        print()

        if depth == 0 or board.is_full():
            score = board.evaluate_board(self.symbol, 3 - self.symbol)
            print(f"{prefix}Leaf node reached with score: {score}")
            return score, None, nodes_expanded

        valid_moves = board.get_valid_moves()
        center_col = board.cols // 2
        valid_moves.sort(key=lambda x: abs(x - center_col))  # Prioritize center column

        best_move = None
        best_score = float('-inf') if maximizing else float('inf')

        for col in valid_moves:
            # Calculate expected score considering the probabilities
            expected_score = 0
            # Probabilities: 0.6 for the chosen column, 0.2 for left or right
            for i, prob in zip([0, -1, 1], [0.6, 0.2, 0.2]):  # current, left, right
                target_col = col + i
                if 0 <= target_col < board.cols and board.valid_move(target_col):
                    # Simulate the move for the current column and its neighbors
                    board.play_disc(self, target_col)
                    eval_score, _ , nodes_expanded = self.minimax(board, depth - 1, not maximizing, indent + 1, nodes_expanded)
                    board.undo_move(target_col)
                    expected_score += prob * eval_score

            # Choose the best column based on the expected score
            if maximizing:
                if expected_score > best_score:
                    best_score = expected_score
                    best_move = col
            else:
                if expected_score < best_score:
                    best_score = expected_score
                    best_move = col

        print(f"{prefix}Best expected score: {best_score}, Move: {best_move}\n")
        return best_score, best_move, nodes_expanded
    
