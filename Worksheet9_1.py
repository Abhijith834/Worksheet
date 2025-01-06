import numpy as np
import matplotlib.pyplot as plt

# Constants
GRID_SIZE = 4
NUM_STATES = 7
NUM_UPDATES = 4

def initialize_grid(grid_size, num_states, seed=42):
    """Initialize the grid with random states."""
    np.random.seed(seed)
    return np.random.choice(num_states, size=(grid_size, grid_size))

def print_grid(grid, title=None):
    """Print the current grid state."""
    if title:
        print(f"\n{title}")
    for row in grid:
        print(" ".join(map(str, row)))

def apply_diffusion(grid):
    """Apply diffusion by averaging states with neighbors."""
    new_grid = grid.astype(float).copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = [
                grid[i-1, j] if i > 0 else None,               # Top
                grid[i+1, j] if i < grid.shape[0] - 1 else None,  # Bottom
                grid[i, j-1] if j > 0 else None,               # Left
                grid[i, j+1] if j < grid.shape[1] - 1 else None  # Right
            ]
            neighbors = [n for n in neighbors if n is not None]  # Exclude None
            new_grid[i, j] = np.mean(neighbors)
    return np.round(new_grid).astype(int)

def calculate_probabilities(grid, num_states):
    """Calculate probabilities of each site state."""
    probabilities = np.zeros(num_states)
    flat_grid = grid.flatten()
    for state in range(num_states):
        probabilities[state] = np.sum(flat_grid == state) / flat_grid.size
    return probabilities

def display_probabilities(probabilities, update_num):
    """Display the probabilities of each state."""
    print(f"\nProbabilities After Update {update_num}:")
    for state, prob in enumerate(probabilities):
        print(f"State {state}: {prob:.2f}")

def visualize_grid(grid, title="Grid State"):
    """Visualize the grid state."""
    plt.imshow(grid, cmap='viridis', interpolation='nearest', vmin=0, vmax=NUM_STATES-1)
    plt.title(title)
    plt.colorbar(label="Site State")
    plt.show()

def main():
    # Initialize grid
    grid = initialize_grid(GRID_SIZE, NUM_STATES)
    print_grid(grid, title="Initial Grid")
    
    probabilities_over_time = []

    # Perform updates
    for update in range(1, NUM_UPDATES + 1):
        grid = apply_diffusion(grid)
        probabilities = calculate_probabilities(grid, NUM_STATES)
        probabilities_over_time.append(probabilities)
        
        print_grid(grid, title=f"Grid After Update {update}")
        display_probabilities(probabilities, update)

    # Visualize final grid state
    visualize_grid(grid, title="Final Grid State")

if __name__ == "__main__":
    main()
