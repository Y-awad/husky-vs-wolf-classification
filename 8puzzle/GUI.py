
import tkinter as tk
from tkinter import messagebox
from State import State, a_star_with_metrics, eclidean_heuristic, manhattan_heuristic, bfs_with_metrics, dfs_with_metrics, ids_with_metrics, generate_initial_board

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Solver")
        
        self.current_state = None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Create the grid for the puzzle
        self.create_grid()
        self.create_buttons()
        self.generate_new_board()
        #self.generate_initial_state()


    def generate_initial_state(self):
        initial_board = generate_initial_board()
        self.current_state = State(initial_board)
        self.update_grid()
        print("Initial Board:")
        for row in initial_board:
            print(row)

    def create_grid(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text="", width=4, height=2, font=('Arial', 24))
                self.buttons[i][j].grid(row=i, column=j)

    def create_buttons(self):
        # Buttons for solving algorithms
        tk.Button(self.master, text="Solve with A* (Manhattan)", command=self.solve_a_star_manhattan).grid(row=3, column=0, columnspan=3)
        tk.Button(self.master, text="Solve with A* (Euclidean)", command=self.solve_a_star_euclidean).grid(row=4, column=0, columnspan=3)
        tk.Button(self.master, text="Solve with BFS", command=self.solve_bfs).grid(row=5, column=0, columnspan=3)
        tk.Button(self.master, text="Solve with DFS", command=self.solve_dfs).grid(row=6, column=0, columnspan=3)
        tk.Button(self.master, text="Solve with IDFS", command=self.solve_ids).grid(row=7, column=0, columnspan=3)
        tk.Button(self.master, text="Generate New Board", command=self.generate_new_board).grid(row=8, column=0, columnspan=3)
        tk.Button(self.master, text="Exit", command=self.master.quit).grid(row=9, column=0, columnspan=3)
    

    def generate_new_board(self):
        self.generate_initial_state()

    def update_grid(self):
        for i in range(3):
            for j in range(3):
                value = self.current_state.board[i][j]
                self.buttons[i][j].config(text=str(value) if value != 0 else "")
    
    


    def display_solution(self, path, algorithm_name):
        if path is not None:
           # print(f"Solution Path using {algorithm_name}: {path}")
            print(f"Number of Moves: {len(path)}")
            
            # Reset the current state to the initial state for displaying the solution
            current_state = self.current_state
            
            for action in path:
                # Apply each move to the current state and update the grid
                if(action=="up"):
                    move= ((-1, 0), action)
                elif(action=="down"):
                   move=((1, 0), action)
                elif(action=="right"):
                   move=((0, 1), action)
                elif(action=="left"):
                   move=((0, -1), action)

                self.current_state, _ =current_state.apply_move(move)
                current_state = self.current_state
                self.update_grid()  # Update the GUI grid with the current state
                self.master.update()  # Refresh the GUI
                self.master.after(500)  # Delay for 500 ms between moves
                
            print("Final State:")
            print(current_state.board)
            messagebox.showinfo("Result", "Solution found!")
        else:
            messagebox.showinfo("Result", "No solution found!")


    def solve_a_star_manhattan(self):
        path, cost = a_star_with_metrics(self.current_state, manhattan_heuristic)
        self.display_solution(path, "A* (Manhattan)")

    def solve_a_star_euclidean(self):
        path, cost = a_star_with_metrics(self.current_state, eclidean_heuristic)
        self.display_solution(path, "A* (Euclidean)")

    def solve_bfs(self):
        path, cost = bfs_with_metrics(self.current_state)
        self.display_solution(path, "BFS")

    def solve_dfs(self):
        path, cost = dfs_with_metrics(self.current_state)
        self.display_solution(path, "DFS")

    def solve_ids(self):
        path, cost = ids_with_metrics(self.current_state)
        self.display_solution(path, "IDFS")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
