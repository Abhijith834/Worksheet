import random
import time
import itertools
import numpy as np

# Define the Agent class
class Agent:
    def __init__(self, name, position, behavior):
        self.name = name
        self.position = position
        self.behavior = behavior  # Can be "annoying" or a movement function

    def move(self, grid_size, occupied_positions):
        if self.behavior == "annoying":
            # Annoying agents do not move
            return None
        else:
            # VIP agent decides on a move based on its policy
            new_position, action_taken = self.behavior(self.position, grid_size, occupied_positions)
            move_message = f"{self.name} moves {action_taken} to {new_position[0] + 1}x{new_position[1] + 1}"

            # Check for walls
            if not (0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size):
                move_message = f"{self.name} tried to move {action_taken} to {new_position[0] + 1}x{new_position[1] + 1} but hit a wall"
                new_position = self.position  # Stay in the same position

            # Check for other agents
            elif new_position in occupied_positions:
                move_message = f"{self.name} tried to move {action_taken} to {new_position[0] + 1}x{new_position[1] + 1} but was blocked by an annoying agent"
                new_position = self.position  # Stay in the same position

            # Update position
            self.position = new_position
            return move_message

# Define the GridWorld class
class GridWorld:
    def __init__(self, size, agents):
        self.size = size
        self.agents = agents

    def get_occupied_positions(self):
        # Get positions occupied by annoying agents
        return {agent.position for agent in self.agents if agent.behavior == "annoying"}

    def update_world(self):
        occupied_positions = self.get_occupied_positions()
        for agent in self.agents:
            if agent.behavior != "annoying":
                # VIP agent moves according to its policy
                move_result = agent.move(self.size, occupied_positions)
                if move_result:
                    print(move_result)
                # Calculate and display empowerment after the move
                empowerment = calculate_empowerment(agent.position, self.size, occupied_positions)
                print(f"3-step empowerment for {agent.name} at position {agent.position[0] + 1}x{agent.position[1] + 1}: {empowerment:.2f}")

    def display_grid(self):
        # Initialize an empty grid
        grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
        # Place agents on the grid
        for agent in self.agents:
            x, y = agent.position
            grid[x][y] = agent.name
        # Display the grid
        print("\nGrid State:")
        for row in grid:
            print("[" + "|".join(row) + "]")

# Define all possible actions
actions = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1)
}

# Generate all possible 3-step action sequences
action_sequences = list(itertools.product(actions.keys(), repeat=3))

# Function to apply an action
def apply_action(position, action):
    dx, dy = actions[action]
    return (position[0] + dx, position[1] + dy)

# Function to simulate a 3-step action sequence
def simulate_sequence(start_position, sequence, grid_size, occupied_positions):
    position = start_position
    for action in sequence:
        proposed_position = apply_action(position, action)
        # Check for walls and obstacles
        if 0 <= proposed_position[0] < grid_size and 0 <= proposed_position[1] < grid_size:
            if proposed_position not in occupied_positions:
                position = proposed_position  # Move to the new position
    return position

# Function to calculate empowerment
def calculate_empowerment(position, grid_size, occupied_positions):
    reachable_positions = set()
    for sequence in action_sequences:
        final_position = simulate_sequence(position, sequence, grid_size, occupied_positions)
        reachable_positions.add(final_position)
    # Empowerment is the log base 2 of the number of unique reachable positions
    return np.log2(len(reachable_positions)) if reachable_positions else 0

# Empowerment-driven movement policy for the VIP agent
def vip_empowerment_policy(position, grid_size, occupied_positions):
    max_empowerment = -1
    best_moves = []

    # Evaluate all possible moves
    for action in actions.keys():
        proposed_position = apply_action(position, action)
        # Simulate the move
        if 0 <= proposed_position[0] < grid_size and 0 <= proposed_position[1] < grid_size:
            if proposed_position not in occupied_positions:
                new_position = proposed_position
            else:
                new_position = position  # Blocked by an agent
        else:
            new_position = position  # Hit a wall
        # Calculate empowerment from the new position
        empowerment = calculate_empowerment(new_position, grid_size, occupied_positions)
        if empowerment > max_empowerment:
            max_empowerment = empowerment
            best_moves = [(new_position, action)]
        elif empowerment == max_empowerment:
            best_moves.append((new_position, action))
    # Randomly choose among the best moves
    chosen_move = random.choice(best_moves)
    return chosen_move

# Initialize the grid and agents
def initialize_world():
    grid_size = 5
    agent_positions = set()

    # Initialize 5 annoying agents at random positions
    annoying_agents = []
    for _ in range(5):
        while True:
            pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if pos not in agent_positions:
                agent_positions.add(pos)
                annoying_agents.append(Agent(name="A", position=pos, behavior="annoying"))
                break

    # Initialize the VIP agent at a random position
    while True:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos not in agent_positions:
            agent_positions.add(pos)
            vip_agent = Agent(name="V", position=pos, behavior=vip_empowerment_policy)
            break

    # Create the grid world with all agents
    agents = annoying_agents + [vip_agent]
    world = GridWorld(size=grid_size, agents=agents)
    return world

# Run the simulation
def run_simulation(steps=50, delay=0.25):
    world = initialize_world()
    for step in range(steps):
        print(f"\nStep {step + 1}")
        world.update_world()
        world.display_grid()
        time.sleep(delay)

# Start the simulation
if __name__ == "__main__":
    run_simulation()
