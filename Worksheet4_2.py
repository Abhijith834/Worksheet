import random
import time
import itertools
import numpy as np

# Define possible actions and their effects on position
ACTIONS = {
    "north": (-1, 0),  # Move up
    "south": (1, 0),   # Move down
    "west":  (0, -1),  # Move left
    "east":  (0, 1)    # Move right
}

# Generate all possible 3-step action sequences (64 in total)
ACTION_SEQUENCES = list(itertools.product(ACTIONS.keys(), repeat=3))

class Agent:
    def __init__(self, name, position, behavior):
        self.name = name                # Agent's name (e.g., "V" for VIP, "A1" for annoying agent 1)
        self.position = position        # Agent's current position on the grid as (row, column)
        self.behavior = behavior        # Function defining the agent's movement policy

    def move(self, grid_size, agents_positions):
        # Positions occupied by other agents
        occupied_positions = {pos for agent_name, pos in agents_positions.items() if agent_name != self.name}

        # Decide on a move based on the agent's behavior
        intended_position, action_taken = self.behavior(self.position, grid_size, occupied_positions, agents_positions)

        # Check if the intended move is within grid bounds
        if not (0 <= intended_position[0] < grid_size and 0 <= intended_position[1] < grid_size):
            print(f"{self.name} tried to move {action_taken} but hit a wall")
            new_position = self.position  # Stay in the same position
        # Check if the intended position is occupied by another agent
        elif intended_position in occupied_positions:
            print(f"{self.name} tried to move {action_taken} but was blocked by another agent")
            new_position = self.position  # Stay in the same position
        else:
            # Move is successful
            new_position = intended_position
            print(f"{self.name} moves {action_taken} to {new_position[0]+1}x{new_position[1]+1}")

        # Update the agent's position
        self.position = new_position
        return new_position

class GridWorld:
    def __init__(self, size, agents):
        self.size = size        # Size of the grid (e.g., 5 for a 5x5 grid)
        self.agents = agents    # List of Agent instances

    def get_agents_positions(self):
        # Returns a dictionary of agent names to their positions
        return {agent.name: agent.position for agent in self.agents}

    def update_world(self):
        agents_positions = self.get_agents_positions()

        # Agents take turns to move: VIP agent moves first
        for agent in self.agents:
            new_position = agent.move(self.size, agents_positions)
            # Update the positions after each agent moves
            agents_positions[agent.name] = new_position

            if agent.name == "V":
                # Calculate and display empowerment for the VIP agent
                other_agents_positions = {pos for name, pos in agents_positions.items() if name != "V"}
                empowerment = calculate_empowerment(agent.position, self.size, other_agents_positions)
                print(f"3-step empowerment for {agent.name} at position {agent.position[0]+1}x{agent.position[1]+1}: {empowerment:.2f}")

    def display_grid(self):
        # Create an empty grid
        grid = [["  " for _ in range(self.size)] for _ in range(self.size)]
        # Place agents on the grid
        for agent in self.agents:
            row, col = agent.position
            grid[row][col] = agent.name
        # Display the grid
        print("\nGrid State:")
        for row in grid:
            print("[" + "|".join(row) + "]")

def apply_action(position, action):
    """Applies an action to a position and returns the new position."""
    delta_row, delta_col = ACTIONS[action]
    return position[0] + delta_row, position[1] + delta_col

def simulate_sequence(start_position, sequence, grid_size, occupied_positions):
    """Simulates a sequence of actions from a starting position."""
    position = start_position
    for action in sequence:
        next_position = apply_action(position, action)
        # Check for walls and occupied positions
        if (0 <= next_position[0] < grid_size and
            0 <= next_position[1] < grid_size and
            next_position not in occupied_positions):
            position = next_position  # Move to the new position
        # If move is invalid, stay in the current position
    return position

def calculate_empowerment(position, grid_size, occupied_positions):
    """Calculates the empowerment value from a given position."""
    reachable_positions = set()
    for sequence in ACTION_SEQUENCES:
        final_position = simulate_sequence(position, sequence, grid_size, occupied_positions)
        reachable_positions.add(final_position)
    # Empowerment is the log base 2 of the number of unique reachable positions
    return np.log2(len(reachable_positions)) if reachable_positions else 0

def vip_empowerment_policy(position, grid_size, occupied_positions, agents_positions):
    """Determines the VIP agent's next move to maximize empowerment."""
    max_empowerment = -1
    best_moves = []

    for action in ACTIONS.keys():
        intended_position = apply_action(position, action)
        # Check for walls and occupied positions
        if (0 <= intended_position[0] < grid_size and
            0 <= intended_position[1] < grid_size and
            intended_position not in occupied_positions):
            new_position = intended_position
        else:
            new_position = position  # Invalid move; stay in the same position

        # Calculate empowerment after the move
        empowerment = calculate_empowerment(new_position, grid_size, occupied_positions)
        if empowerment > max_empowerment:
            max_empowerment = empowerment
            best_moves = [(intended_position, action)]
        elif empowerment == max_empowerment:
            best_moves.append((intended_position, action))

    # Randomly choose among the best moves
    return random.choice(best_moves)

def antagonistic_policy(position, grid_size, occupied_positions, agents_positions):
    """Determines an annoying agent's next move to minimize the VIP agent's empowerment."""
    min_empowerment = float('inf')
    best_moves = []
    vip_position = agents_positions["V"]

    for action in ACTIONS.keys():
        intended_position = apply_action(position, action)
        # Check for walls and occupied positions
        if (0 <= intended_position[0] < grid_size and
            0 <= intended_position[1] < grid_size and
            intended_position not in occupied_positions):
            new_position = intended_position
        else:
            new_position = position  # Invalid move; stay in the same position

        # Simulate the new occupied positions after this agent's move
        temp_occupied_positions = occupied_positions.copy()
        temp_occupied_positions.add(new_position)
        # Calculate the VIP's empowerment after this move
        empowerment = calculate_empowerment(vip_position, grid_size, temp_occupied_positions)
        if empowerment < min_empowerment:
            min_empowerment = empowerment
            best_moves = [(intended_position, action)]
        elif empowerment == min_empowerment:
            best_moves.append((intended_position, action))

    # Randomly choose among the best moves
    return random.choice(best_moves)

def initialize_world():
    """Initializes the grid world with agents placed randomly."""
    grid_size = 5
    agent_positions = set()

    # Initialize the VIP agent at a random position
    while True:
        vip_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if vip_pos not in agent_positions:
            agent_positions.add(vip_pos)
            vip_agent = Agent(name="V", position=vip_pos, behavior=vip_empowerment_policy)
            break

    # Initialize 5 annoying agents at random positions
    annoying_agents = []
    for i in range(5):
        while True:
            agent_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if agent_pos not in agent_positions:
                agent_positions.add(agent_pos)
                agent_name = f"A{i+1}"
                annoying_agent = Agent(name=agent_name, position=agent_pos, behavior=antagonistic_policy)
                annoying_agents.append(annoying_agent)
                break

    # Create the grid world with all agents
    agents = [vip_agent] + annoying_agents  # VIP agent moves first
    return GridWorld(size=grid_size, agents=agents)

def run_simulation(steps=30, delay=0.25):
    """Runs the simulation for a specified number of steps."""
    world = initialize_world()
    for step in range(steps):
        print(f"\nStep {step + 1}")
        world.update_world()
        world.display_grid()
        time.sleep(delay)  # Delay between steps for readability

if __name__ == "__main__":
    run_simulation()
