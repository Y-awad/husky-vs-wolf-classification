import tkinter as tk
from tkinter import messagebox
import time  # Import the time module
import numpy as np
from Game import Game


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.game = None  # Initialize as None; will be set after algorithm selection
        self.board = None
        self.current_player = None
        self.buttons = []
        self.algorithm = None
        self.start_time = None  # Track the start time of a move
        self.move_time_label = None  # Label for move time display
        self.turn_label = None  # Label for displaying current turn
        self.setup_algorithm_selection()

    def setup_algorithm_selection(self):
        """Setup initial screen for algorithm selection."""
        label = tk.Label(self.root, text="Select AI Algorithm", font=("Arial", 16))
        label.pack(pady=10)

        for algo in ["minimax", "alphabeta", "expected_minimax"]:
            btn = tk.Button(
                self.root, text=algo.capitalize(),
                command=lambda a=algo: self.start_game(a),
                height=2, width=15
            )
            btn.pack(pady=5)

    def start_game(self, algorithm):
        """Start the game with the chosen algorithm."""
        self.algorithm = algorithm
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the algorithm selection screen

        self.game = Game(algorithm=algorithm)
        self.board = self.game.board
        self.current_player = self.game.current_player
        self.create_widgets()
        self.update_turn_label()  # Set initial turn display

        if self.current_player.is_ai:
            self.start_time = time.time()  # Start timing the AI move
            self.ai_move()

    def create_widgets(self):
        # Configure uniform column weights for equal-sized columns
        for col in range(self.board.cols):
            self.root.grid_columnconfigure(col, weight=1, uniform="col")

        for row in range(self.board.rows + 4):  # +4 for buttons, scores, move time, and turn display
            self.root.grid_rowconfigure(row, weight=1, uniform="row")

        # Create buttons for column selection
        for col in range(self.board.cols):
            btn = tk.Button(
                self.root, text="↓",
                command=lambda c=col: self.drop_disc(c),
                height=2, width=4
            )
            btn.grid(row=0, column=col, sticky="nsew")
            self.buttons.append(btn)

        # Create board cells
        self.cell_labels = []
        for row in range(self.board.rows):
            row_labels = []
            for col in range(self.board.cols):
                lbl = tk.Label(self.root, text="⚪", font=("Arial", 20), width=4, height=2,
                               bg="blue", fg="white", relief="ridge", borderwidth=1)
                lbl.grid(row=row + 1, column=col, sticky="nsew")
                row_labels.append(lbl)
            self.cell_labels.append(row_labels)

        # Add a reset button
        reset_btn = tk.Button(self.root, text="Reset", command=self.reset_game, height=2, width=8)
        reset_btn.grid(row=self.board.rows + 1, columnspan=self.board.cols, sticky="nsew")

        # Add score labels
        self.human_score_label = tk.Label(self.root, text="Human Score: 0", font=("Arial", 14))
        self.human_score_label.grid(row=self.board.rows + 2, column=0, columnspan=self.board.cols // 2, sticky="w")
        self.ai_score_label = tk.Label(self.root, text="AI Score: 0", font=("Arial", 14))
        self.ai_score_label.grid(row=self.board.rows + 2, column=self.board.cols // 2, columnspan=self.board.cols // 2, sticky="e")

        # Add move time label
        self.move_time_label = tk.Label(self.root, text="Move Time: 0.00s", font=("Arial", 14))
        self.move_time_label.grid(row=self.board.rows + 3, column=0, columnspan=self.board.cols, sticky="ew")

        # Add turn label
        self.turn_label = tk.Label(self.root, text="Turn: ", font=("Arial", 14))
        self.turn_label.grid(row=self.board.rows + 4, column=0, columnspan=self.board.cols, sticky="ew")

    def update_turn_label(self):
     """Update the current turn label with clear Human/AI designation."""
     if self.current_player.is_ai:
        self.turn_label.config(text="Turn: AI")
     else:
        self.turn_label.config(text="Turn: Human")

    def drop_disc(self, col):
        self.start_time = time.time()  # Start timing the move

        if self.board.valid_move(col):
            self.board.play_disc(self.current_player, col)
            self.update_board()
            self.update_score_labels()

            end_time = time.time()  # End timing the move
            move_time = end_time - self.start_time
            self.move_time_label.config(text=f"Move Time: {move_time:.2f}s")

            if self.check_winner():
                return

            self.current_player = self.game.player2 if self.current_player == self.game.player1 else self.game.player1
            self.update_turn_label()  # Update turn display

            if self.current_player.is_ai:
                self.root.after(500, self.ai_move)
        else:
            messagebox.showinfo("Invalid Move", f"Column {col} is full. Try a different one!")

    def ai_move(self):
        self.start_time = time.time()  # Start timing the AI move

        self.current_player.make_move(self.board)
        self.update_board()
        self.update_score_labels()

        end_time = time.time()  # End timing the AI move
        move_time = end_time - self.start_time
        self.move_time_label.config(text=f"Move Time: {move_time:.2f}s")

        if not self.check_winner():
            self.current_player = self.game.player2 if self.current_player == self.game.player1 else self.game.player1
            self.update_turn_label()

    def update_board(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell_value = self.board.board[row][col]
                if cell_value == 0:
                    self.cell_labels[row][col].config(text="⚪", fg="white")  # Empty cell
                elif cell_value == 1:
                    self.cell_labels[row][col].config(text="●", fg="red")  # Player 1's disc
                elif cell_value == 2:
                    self.cell_labels[row][col].config(text="●", fg="yellow")  # Player 2's disc

    def check_winner(self):
     p1_score = self.board.count_connected_fours(self.game.player1.symbol)
     p2_score = self.board.count_connected_fours(self.game.player2.symbol)

     if self.board.is_full():
        if p1_score > p2_score:
            winner = self.game.player1.name
            message = f"Game Over! Winner: {winner}"
        elif p2_score > p1_score:
            winner = self.game.player2.name
            message = f"Game Over! Winner: {winner}"
        else:
            message = "Game Over! It's a draw!"
        messagebox.showinfo("Game Over", message)
        self.disable_buttons()
        self.show_back_button()  # Show the back button after the game ends
        return True
     return False
    
    def show_back_button(self):
     back_btn = tk.Button(
        self.root, text="Back to Menu",
        command=self.return_to_menu,
        font=("Arial", 14), bg="#ff6f61", fg="white",
        height=2, width=15, relief="raised"
     )
     back_btn.grid(row=self.board.rows + 4, column=0, columnspan=self.board.cols, pady=10, sticky="nsew")

    def return_to_menu(self):
     for widget in self.root.winfo_children():
        widget.destroy()  # Clear all widgets
     self.setup_algorithm_selection()  # Return to the algorithm selection menu




    def update_score_labels(self):
        self.human_score_label.config(
            text=f"Human Score: {self.board.count_connected_fours(self.game.player1.symbol)}")
        self.ai_score_label.config(
            text=f"AI Score: {self.board.count_connected_fours(self.game.player2.symbol)}")

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self):
        self.board.board = np.zeros((self.board.rows, self.board.cols), dtype=int)
        self.current_player = self.game.player1
        self.update_board()
        self.update_score_labels()
        self.move_time_label.config(text="Move Time: 0.00s")
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect 4")
    app = Connect4GUI(root)
    root.mainloop()
