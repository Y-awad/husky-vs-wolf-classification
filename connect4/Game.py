import random
from Board import Board
from Player import Player

class Game:
    def __init__(self, algorithm):
        self.board = Board()
        self.player1 = Player("Player 1", 1)
        self.player2 = Player("Player 2", 2, is_ai=True, algorithm=algorithm)  # Choose algorithm
        self.players = [self.player1, self.player2]
        random.shuffle(self.players)  # Randomly shuffle players
        self.current_player = self.players[0]  # Randomly select the starting player
        self.game_over = False

    def play(self):
        print(f"{self.current_player.name} will start the game!\n")

        while not self.game_over:
            self.board.print_board()
            self.current_player.make_move(self.board)

            # Update scores after every move
            p1_score = self.board.count_connected_fours(self.player1.symbol)
            p2_score = self.board.count_connected_fours(self.player2.symbol)

            print(f"Scores -> {self.player1.name}: {p1_score}, {self.player2.name}: {p2_score}")

            if self.board.is_full():
                self.game_over = True
                self.board.print_board()
                print("Game Over!")
                if p1_score > p2_score:
                    print(f"{self.player1.name} wins!")
                elif p1_score < p2_score:
                    print(f"{self.player2.name} wins!")
                else:
                    print("It's a draw!")
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1




#if __name__ == "__main__":
   # game = Game(algorithm="alphabeta")  # Choose between "minimax" or "alphabeta"
    #game.play()
