import random # importing random libraty to modify agent spawning to random positions for each episode

class Agent: # Agent class is created, Agent name, position and behavior is initiated
    def __init__(self, name, position, movement_behavior):
        self.name = name
        self.position = position
        self.movement_behavior = movement_behavior
        self.in_game = True
    
    def move(self, grid_size, occupied_positions):
        #Moves the agent according to its specific movement behavior. Cancels the move if the target cell is occupied.
        if not self.in_game:
            return f"{self.name} has already left the game"
        
        new_position = self.movement_behavior(self.position, grid_size)
        
        # Check if the new position is outside the grid
        if new_position[0] < 0 or new_position[0] >= grid_size or new_position[1] < 0 or new_position[1] >= grid_size:
            self.in_game = False
            return f"{self.name} leaves the game"
        
        # Push other agent if the new position is occupied
        if new_position in occupied_positions:
            return f"{self.name} pushes an agent from {new_position[0]+1}x{new_position[1]+1}"
        
        # Otherwise, move the agent
        self.position = new_position
        return f"{self.name} moves to {self.position[0]+1}x{self.position[1]+1}"


class GridWorld: # Agent gridworld is created
    def __init__(self, size, agents, start_delays):
        self.size = size
        self.agents = agents
        self.start_delays = start_delays
        self.current_step = 0
    
    def update_world(self): # Updated the agent positions
        messages = []
        occupied_positions = [agent.position for agent in self.agents if agent.in_game]
        
        for i, agent in enumerate(self.agents):
            if self.current_step >= self.start_delays[i] and agent.in_game:
                move_message = agent.move(self.size, occupied_positions)
                messages.append(move_message)
                # Update occupied positions after move
                occupied_positions = [agent.position for agent in self.agents if agent.in_game]
        
        self.current_step += 1
        return messages
    
    def count_active_agents(self):
        """Counts how many agents are still in the game."""
        return sum(agent.in_game for agent in self.agents)


# Define movement behaviors for the new agents
def move_clockwise(position, grid_size): # Moves the agent C clockwise around the grid. 
    x, y = position
    if x == 0 and y < grid_size - 1:
        y += 1
    elif y == grid_size - 1 and x < grid_size - 1:
        x += 1
    elif x == grid_size - 1 and y > 0:
        y -= 1
    elif y == 0 and x > 0:
        x -= 1
    return (x, y)

def move_counterclockwise_diagonal(position, grid_size): # Moves the agent D diagonally in a counter-clockwise diamond shape.
    x, y = position
    if x == y and x != grid_size - 1:
        x += 1
    elif x == grid_size - 1 - y and x != 0:
        y += 1
    elif x > y and x != 0:
        x -= 1
    else:
        y -= 1
    return (x, y)

def move_left(position, grid_size): # Moves the agent L always to the left.
    x, y = position
    y -= 1
    return (x, y)

def move_up(position, grid_size): # Moves the agent U always up.
    x, y = position
    x -= 1
    return (x, y)


# Initialize agents with their movement behaviors and starting positions
def create_agents_random(grid_size=5): # Creates the agents with random starting positions and movement behaviors.
    start_positions = set()  # To avoid duplicate starting positions
    
    while len(start_positions) < 4:
        start_positions.add((random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)))
    
    start_positions = list(start_positions) 
    
    agent_clockwise = Agent("C", start_positions[0], move_clockwise)
    agent_diagonal = Agent("D", start_positions[1], move_counterclockwise_diagonal)
    agent_left = Agent("L", start_positions[2], move_left)
    agent_up = Agent("U", start_positions[3], move_up)
    
    agents = [agent_clockwise, agent_diagonal, agent_left, agent_up]
    return agents


# Simulate the grid world with random starting positions for 100 steps
def simulate_world_with_random_start(grid_size=5, num_steps=100):
    agents = create_agents_random(grid_size)
    grid_world = GridWorld(grid_size, agents, [0, 0, 0, 0])  # All agents start immediately

    for step in range(num_steps):
        print(f"Step {step + 1}:")
        messages = grid_world.update_world()
        for message in messages:
            print(message)
        print("\n")

    return grid_world.count_active_agents()

# Run the simulations with random start states
print("Simulation 1:")
agents_remaining_1 = simulate_world_with_random_start()
print(f"Agents remaining after 100 steps: {agents_remaining_1}\n")

print("Simulation 2:")
agents_remaining_2 = simulate_world_with_random_start()
print(f"Agents remaining after 100 steps: {agents_remaining_2}\n")

print("Simulation 3:")
agents_remaining_3 = simulate_world_with_random_start()
print(f"Agents remaining after 100 steps: {agents_remaining_3}\n")

# Print final results
print(f"Results after 100 time-steps for all simulations:")
print(f"Simulation 1: {agents_remaining_1} agents remained")
print(f"Simulation 2: {agents_remaining_2} agents remained")
print(f"Simulation 3: {agents_remaining_3} agents remained")
