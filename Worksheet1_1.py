# Defining the Node classes for agents and world with delayed starts

class Agent: # Agent class is created, Agent name, position and behavior is initiated
    def __init__(self, name, position, movement_behavior):
        self.name = name
        self.position = position
        self.movement_behavior = movement_behavior
    
    def move(self, grid_size, occupied_positions):
        #Moves the agent according to its specific movement behavior. Cancels the move if the target cell is occupied.
        new_position = self.movement_behavior(self.position, grid_size)
        if new_position not in occupied_positions:
            self.position = new_position
            return f"{self.name} moves to {self.position[0]+1}x{self.position[1]+1}"
        else:
            return f"{self.name} tries to move to {new_position[0]+1}x{new_position[1]+1} but the move got cancelled"


class GridWorld: # Agent gridworld is created
    def __init__(self, size, agents, start_delays):
        self.size = size
        self.agents = agents
        self.start_delays = start_delays
        self.current_step = 0
    
    def update_world(self): #Updated the agent positions
        messages = []
        occupied_positions = [agent.position for agent in self.agents if self.current_step >= self.start_delays[self.agents.index(agent)]]
        
        for i, agent in enumerate(self.agents):
            if self.current_step == self.start_delays[i]:
                messages.append(f"{agent.name} appears in cell {agent.position[0]+1}x{agent.position[1]+1}")
            elif self.current_step >= self.start_delays[i]:
                move_message = agent.move(self.size, occupied_positions)
                messages.append(move_message)
                # Update occupied positions after move
                occupied_positions = [agent.position for agent in self.agents if self.current_step >= self.start_delays[self.agents.index(agent)]]
        
        self.current_step += 1
        return messages
    
    def display(self): # Displays the world, agent and the moves each agent has made
        grid_repr = ""
        for i in range(self.size):
            grid_repr += "["
            for j in range(self.size):
                agent_here = next((agent for agent in self.agents if agent.position == (i, j)), None)
                if agent_here:
                    grid_repr += f"{agent_here.name}"
                else:
                    grid_repr += " "
                if j < self.size - 1:
                    grid_repr += "|"
            grid_repr += "]\n"
        print(grid_repr)


# Define movement behaviors
def move_clockwise(position, grid_size): # Moves the agent C clockwise
    x, y = position
    if x == 0 and y < grid_size - 1:
        y += 1
    elif y == grid_size - 1 and x < grid_size - 1:
        x += 1
    elif x == grid_size - 1 and y > 0:
        y -= 1
    elif y == 0 and x > 0:
        x -= 1
    return (x % grid_size, y % grid_size)

def move_counterclockwise_diagonal(position, grid_size): # Moves the agent D diagonaly counterclockwise
    x, y = position
    if x == y and x != grid_size - 1:
        x += 1
    elif x == grid_size - 1 - y and x != 0:
        y += 1
    elif x > y and x != 0:
        x -= 1
    else:
        y -= 1
    return (x % grid_size, y % grid_size)

def move_left(position, grid_size): # Moves the agent L to the left
    x, y = position
    y -= 1
    return (x % grid_size, y % grid_size)


# Initialize agents with their movement behaviors and starting positions
starting_positions = [(1, 0), (1, 0), (1, 0)]  # All agents start at (2x1)
agent_clockwise = Agent("C", starting_positions[0], move_clockwise)
agent_diagonal = Agent("D", starting_positions[1], move_counterclockwise_diagonal)
agent_left = Agent("L", starting_positions[2], move_left)

# Define delays: C appears on step 1, D on step 3, L on step 5
agents = [agent_clockwise, agent_diagonal, agent_left]
start_delays = [0, 2, 4]  # 2-step delay for D and 4-step delay for L

# Create the grid world with delayed starts and same starting position
grid_world = GridWorld(3, agents, start_delays)

# Simulate and display 50 steps in the grid world to observe the staggered starts and behavior
for step in range(50):
    print(f"Step {step + 1}:")
    messages = grid_world.update_world()
    grid_world.display()
    for message in messages:
        print(message)
    print("\n")
