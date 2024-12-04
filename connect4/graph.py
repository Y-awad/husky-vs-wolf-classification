import matplotlib.pyplot as plt
from Game import Game  
from Player import Player 

def run_tests():
    depths = [1, 2, 3, 4, 5]  
    algorithms = ["minimax", "alphabeta", "expected_minimax"]
    times = {algo: [] for algo in algorithms}  
    nodes={algo: [] for algo in algorithms}

    for algorithm in algorithms:
        print(f"Testing {algorithm} algorithm...")
        for depth in depths:
            board = Game(algorithm).board  
            player = Player(name="AI", symbol=2,depth=depth, is_ai=True, algorithm=algorithm)
           
            time_taken = player.make_move(board)

            if time_taken is not None:
                times[algorithm].append(time_taken)
                nodes[algorithm].append(player.nodes_expanded)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    for algorithm in algorithms:
        plt.plot(depths, times[algorithm], marker='o', label=algorithm)

    plt.title("Time Taken by Different Algorithms at Various Depths")
    plt.xlabel("Depth")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True)
    plt.show()


    plt.figure(figsize=(10, 6))
    for algorithm in algorithms:
        plt.plot(depths, nodes[algorithm], marker='o', label=algorithm)
    
    plt.title('Nodes Expanded at Different Depths', fontsize=16)
    plt.xlabel('Depth', fontsize=14)
    plt.ylabel('Nodes Expanded', fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=12)
    plt.show()

if __name__ == "__main__":
    run_tests()
