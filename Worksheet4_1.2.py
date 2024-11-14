import random
import time
import itertools
import numpy as np

class Agent:
    def __init__(self, name, position, behaviour):
        self.name = name
        self.position = position
        self.behaviour = behaviour
        self.history = []  # Track recent positions

    def move(self, grid_size, occupied_positions):
        if self.behaviour == "annoying":
            return None
        else:
            new_position, action_taken = self.behaviour(self.position, grid_size, occupied_positions, self.history)
            # Update history
            self.history.append(self.position)
            if len(self.history) > 10:  # Increase history length
                self.history.pop(0)
            # Movement checks
            if not (0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size):
                return f"{self.name} tried to move to {new_position[0]+1}x{new_position[1]+1} but got hit by a wall"
            elif new_position in occupied_positions:
                return f"{self.name} tried to move to {new_position[0]+1}x{new_position[1]+1} but was blocked by an annoying agent"
            self.position = new_position
            return f"{self.name} moves {action_taken} to {self.position[0]+1}x{self.position[1]+1}"

class GridWorld:
    def __init__(self, size, agents):
        self.size = size
        self.agents = agents

    def get_occupied_positions(self):
        return {agent.position for agent in self.agents if agent.behaviour == "annoying"}

    def update_world(self):
        occupied_positions = self.get_occupied_positions()
        for agent in self.agents:
            if agent.behaviour != "annoying":  # Only process movement for the VIP agent
                move_result = agent.move(self.size, occupied_positions)
                if move_result:
                    print(move_result)
                # Calculate and display empowerment after each move
                empowerment = calculate_empowerment(agent.position, self.size, occupied_positions)
                print(f"3-step empowerment for {agent.name} at {agent.position[0]+1}x{agent.position[1]+1}: {empowerment}")

    def display_grid(self):
        grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
        for agent in self.agents:
            x, y = agent.position
            grid[x][y] = agent.name
        print("\nGrid State:")
        for row in grid:
            print("[" + "|".join(row) + "]")

# Define possible actions
actions = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1)
}

# Generate all 3-step action sequences
action_sequences = list(itertools.product(actions.keys(), repeat=3))

# Define a function to apply an action, considering walls and annoying agents
def apply_action(position, action, grid_size, occupied_positions):
    dx, dy = actions[action]
    new_x = position[0] + dx
    new_y = position[1] + dy

    # Check if the move is out of bounds
    if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
        return position

    # Check if the new position is occupied by an annoying agent
    if (new_x, new_y) in occupied_positions:
        return position

    return (new_x, new_y)

# Define a function to simulate a 3-step sequence from a starting position
def simulate_sequence(start_position, sequence, grid_size, occupied_positions):
    position = start_position
    for action in sequence:
        position = apply_action(position, action, grid_size, occupied_positions)
    return position

# Calculate empowerment for a given starting position
def calculate_empowerment(start_position, grid_size, occupied_positions):
    reachable_states = set()
    for sequence in action_sequences:
        final_position = simulate_sequence(start_position, sequence, grid_size, occupied_positions)
        reachable_states.add(final_position)
    return np.log2(len(reachable_states)) if reachable_states else 0

# Define VIP agent's behavior with exploration strategy
def vip_empowerment_policy(position, grid_size, occupied_positions, agent_history):
    epsilon = 0.1  # Exploration rate (10% chance to explore)
    if random.random() < epsilon:
        # Exploration: choose a random valid move
        possible_moves = []
        for action in actions.keys():
            new_position = apply_action(position, action, grid_size, occupied_positions)
            if new_position != position:
                possible_moves.append((new_position, action))
        if possible_moves:
            chosen_move = random.choice(possible_moves)
            return chosen_move
        else:
            # No valid moves, stay in place
            return (position, "stays")
    else:
        # Exploitation: choose move that maximizes empowerment
        max_empowerment = -float('inf')
        best_moves = []
        for action in actions.keys():
            new_position = apply_action(position, action, grid_size, occupied_positions)
            empowerment = calculate_empowerment(new_position, grid_size, occupied_positions)
            # Apply penalty if revisiting
            if new_position in agent_history:
                empowerment -= 1.0  # Increased penalty
            if empowerment > max_empowerment:
                max_empowerment = empowerment
                best_moves = [(new_position, action)]
            elif empowerment == max_empowerment:
                best_moves.append((new_position, action))
        if best_moves:
            chosen_move = random.choice(best_moves)
            return chosen_move
        else:
            # If all moves are equally bad, stay in place
            return (position, "stays")

# Create a 5x5 world with 5 annoying agents and 1 VIP agent
grid_size = 5
agent_positions = set()

# Initialize 5 annoying agents
annoying_agents = []
for i in range(5):
    while True:
        position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if position not in agent_positions:
            agent_positions.add(position)
            annoying_agents.append(Agent(name="A", position=position, behaviour="annoying"))
            break

# Initialize the VIP agent
while True:
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    if position not in agent_positions:
        agent_positions.add(position)
        vip_agent = Agent(name="V", position=position, behaviour=vip_empowerment_policy)
        break

# Add all agents to the grid world
agents = annoying_agents + [vip_agent]
world = GridWorld(size=grid_size, agents=agents)

# Run the world updates for 50 steps and display the grid state
for step in range(500):
    print(f"\nStep {step + 1}")
    world.update_world()
    world.display_grid()
    time.sleep(0.025)
