import numpy as np
import matplotlib.pyplot as plt
import random

class Sugarscape:
    def __init__(self, size=10, num_agents=20):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)  # Sugar levels grid
        self.agents = []  # List to hold agents
        self.initialize_sugar_levels()
        self.place_agents(num_agents)

    def initialize_sugar_levels(self):
        """
        Populate the grid with sugar levels randomly between 1 and 4 for each cell.
        """
        for row in range(self.size):
            for col in range(self.size):
                self.grid[row, col] = random.randint(1, 4)

    def place_agents(self, num_agents):
        """
        Place agents at random positions on the grid, ensuring no two agents start at the same cell.
        """
        for _ in range(num_agents):
            while True:
                row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                # Ensure no two agents start in the same cell
                if not any(agent.row == row and agent.col == col for agent in self.agents):
                    metabolism = random.randint(1, 3)  # Random metabolism rate
                    self.agents.append(Agent(row, col, metabolism))
                    break

    def update_world(self):
        """
        Advance the simulation by one step, where each agent moves, consumes sugar, and metabolizes.
        """
        for agent in self.agents:
            if agent.is_alive():
                agent.find_and_move_to_sugar(self)
                agent.consume_sugar(self)
                agent.process_metabolism()

    def run_simulation(self, steps=20):
        """
        Run the Sugarscape simulation for a set number of steps and display each step on a grid.
        """
        fig, axes = plt.subplots(4, 5, figsize=(15, 12))  # 4x5 grid of subplots
        axes = axes.flatten()
        
        for step in range(steps):
            self.display_grid(axes[step], step)
            self.update_world()
        
        plt.tight_layout()
        plt.show()

    def display_grid(self, ax, step):
        """
        Display the current state of the Sugarscape grid, showing sugar levels and agent positions.
        """
        # Create a grid copy to display agent positions on top of sugar levels
        visual_grid = self.grid.copy()
        
        for agent in self.agents:
            if agent.is_alive():
                visual_grid[agent.row, agent.col] = 5  # Use 5 to mark agent positions
        
        ax.clear()
        ax.imshow(visual_grid, cmap='coolwarm', interpolation='nearest')
        ax.set_title(f'Step {step + 1}')
        ax.axis('off')

class Agent:
    def __init__(self, row, col, metabolism):
        self.row = row
        self.col = col
        self.metabolism = metabolism
        self.sugar = 5  # Initial sugar level
        self.alive = True

    def is_alive(self):
        """
        Check if the agent has enough sugar to remain alive.
        """
        return self.alive

    def find_and_move_to_sugar(self, sugarscape):
        """
        Move to the adjacent cell with the highest sugar concentration.
        """
        best_position = (self.row, self.col)
        max_sugar = sugarscape.grid[self.row, self.col]

        # Explore neighboring cells to find the best spot for sugar
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                new_row, new_col = self.row + d_row, self.col + d_col
                # Ensure new position is within grid boundaries
                if 0 <= new_row < sugarscape.size and 0 <= new_col < sugarscape.size:
                    if sugarscape.grid[new_row, new_col] > max_sugar:
                        best_position = (new_row, new_col)
                        max_sugar = sugarscape.grid[new_row, new_col]

        # Update agent's position to the chosen cell
        self.row, self.col = best_position

    def consume_sugar(self, sugarscape):
        """
        Consume sugar at the agent's current location, adding it to their sugar reserve.
        """
        self.sugar += sugarscape.grid[self.row, self.col]
        sugarscape.grid[self.row, self.col] = 0  # Reset sugar level after consumption

    def process_metabolism(self):
        """
        Reduce agent's sugar by metabolism rate. If sugar runs out, the agent dies.
        """
        self.sugar -= self.metabolism
        if self.sugar <= 0:
            self.alive = False

# Run the Sugarscape simulation
sugarscape = Sugarscape(size=10, num_agents=20)
sugarscape.run_simulation(steps=20)
