import random

########################################
# 1. List of Agents Model
########################################
def run_list_of_agents_model(initial_population, timesteps, mutation_rate=0.0):
    """
    Run the list-of-agents model.

    Each agent in the population replicates itself once per timestep. By default, 
    offspring have the same genotype as the parent, but with probability `mutation_rate`,
    the offspring mutates into the other genotype.

    Parameters
    ----------
    initial_population : list
        A list of characters, e.g. ['a', 'a', 'b'].
    timesteps : int
        Number of time steps to simulate.
    mutation_rate : float
        Probability that an offspring mutates to the other genotype.

    Returns
    -------
    population_history : list of lists
        A history of the population at each timestep.
    """
    population = initial_population[:]
    population_history = [population]

    for _ in range(timesteps):
        new_population = []
        for agent in population:
            # Parent reproduces (copies) itself
            offspring_type = agent
            # Check for mutation
            if random.random() < mutation_rate:
                offspring_type = 'a' if agent == 'b' else 'b'
            
            # The next generation includes both the original and the offspring
            new_population.append(agent)
            new_population.append(offspring_type)
        
        population = new_population
        population_history.append(population)
    
    return population_history

########################################
# 2. Simple Grid World Model
########################################
def get_neighbors(r, c, rows, cols):
    # Return valid orthogonal neighbors for cell (r,c)
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def run_simple_grid_world(rows, cols, initial_fill=0.2, reproduction_prob=0.1, 
                          timesteps=10, mutation_rate=0.0, death_prob=0.0,
                          allow_multiple=False):
    """
    Run the simple grid world model.

    A 2D grid is initialized with a fraction of cells containing random agents ('a' or 'b'). 
    At each timestep, each agent may reproduce with probability `reproduction_prob`.
    The offspring is placed in a random empty neighboring cell if available. If no neighboring 
    cell is free, reproduction fails.

    Optional:
    - mutation_rate: Probability that an offspring mutates genotype.
    - death_prob: Probability that an agent dies each timestep.
    - allow_multiple: If True, multiple agents can occupy the same cell (stacked). 
      If False, only one agent per cell is allowed.

    Parameters
    ----------
    rows, cols : int
        Dimensions of the grid.
    initial_fill : float
        Fraction of cells to fill initially with random agents 'a' or 'b'.
    reproduction_prob : float
        Probability that an agent reproduces at a given timestep.
    timesteps : int
        Number of time steps to simulate.
    mutation_rate : float
        Probability of offspring mutation.
    death_prob : float
        Probability an agent dies each timestep.
    allow_multiple : bool
        If True, allow multiple agents per cell.

    Returns
    -------
    grid_history : list of 2D lists or list of 2D lists of lists
        The history of the grid configuration at each timestep.
    """

    # Initialize the grid
    # If allow_multiple = False, each cell holds a single char: '.' or 'a' or 'b'
    # If allow_multiple = True, each cell holds a list of chars (agents)
    if not allow_multiple:
        grid = [['.' for _ in range(cols)] for _ in range(rows)]
    else:
        grid = [[[] for _ in range(cols)] for _ in range(rows)]

    # Random initial placement of agents
    num_to_fill = int(rows * cols * initial_fill)
    all_positions = [(r,c) for r in range(rows) for c in range(cols)]
    random.shuffle(all_positions)
    for i in range(num_to_fill):
        r, c = all_positions[i]
        agent_type = random.choice(['a','b'])
        if not allow_multiple:
            grid[r][c] = agent_type
        else:
            grid[r][c].append(agent_type)

    # A function to count agents of each type
    def count_agents(g):
        if not allow_multiple:
            count_a = 0
            count_b = 0
            for row in g:
                count_a += row.count('a')
                count_b += row.count('b')
            return count_a, count_b
        else:
            count_a = 0
            count_b = 0
            for row in g:
                for cell in row:
                    count_a += cell.count('a')
                    count_b += cell.count('b')
            return count_a, count_b

    # Store initial state
    if not allow_multiple:
        grid_history = [ [row[:] for row in grid] ]
    else:
        grid_history = []
        snapshot = []
        for r in range(rows):
            snapshot.append([cell[:] for cell in grid[r]])
        grid_history.append(snapshot)

    # Simulation
    for _ in range(timesteps):
        # Reproduction step
        if not allow_multiple:
            # Collect offspring placements
            offspring_positions = []
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] in ['a','b']:
                        # Reproduction attempt
                        if random.random() < reproduction_prob:
                            nbrs = get_neighbors(r, c, rows, cols)
                            free_nbrs = [(nr, nc) for (nr, nc) in nbrs if grid[nr][nc] == '.']
                            if free_nbrs:
                                nr, nc = random.choice(free_nbrs)
                                new_type = grid[r][c]
                                # Mutation
                                if random.random() < mutation_rate:
                                    new_type = 'b' if new_type == 'a' else 'a'
                                offspring_positions.append((nr, nc, new_type))

            # Place all offspring
            for (nr, nc, tp) in offspring_positions:
                if grid[nr][nc] == '.':
                    grid[nr][nc] = tp

            # Death step
            if death_prob > 0.0:
                for r in range(rows):
                    for c in range(cols):
                        if grid[r][c] in ['a','b']:
                            if random.random() < death_prob:
                                grid[r][c] = '.'

            # Snapshot
            snapshot = [row[:] for row in grid]
            grid_history.append(snapshot)

        else:
            # Multiple occupancy per cell version:
            # First, identify all agents and their reproduction attempts
            new_grid = [[cell[:] for cell in row] for row in grid]

            for r in range(rows):
                for c in range(cols):
                    # Each agent in this cell attempts to reproduce
                    new_cell_agents = new_grid[r][c]
                    # Agents that die will be removed after reproduction attempts
                    alive_agents = []
                    for agent_type in new_cell_agents:
                        # Reproduction
                        if random.random() < reproduction_prob:
                            nbrs = get_neighbors(r, c, rows, cols)
                            # Since multiple occupancy is allowed, no need for checking '.' cells
                            # Just place offspring in a random neighbor cell
                            if nbrs:
                                nr, nc = random.choice(nbrs)
                                new_type = agent_type
                                # Mutation
                                if random.random() < mutation_rate:
                                    new_type = 'b' if new_type == 'a' else 'a'
                                new_grid[nr][nc].append(new_type)

                        # Death
                        if death_prob == 0.0 or random.random() > death_prob:
                            alive_agents.append(agent_type)

                    # Update cell with alive agents
                    new_grid[r][c] = alive_agents

            grid = new_grid

            # Snapshot
            snapshot = []
            for rr in range(rows):
                snapshot.append([cell[:] for cell in grid[rr]])
            grid_history.append(snapshot)

    return grid_history


########################################
# Example Usage
########################################
if __name__ == "__main__":
    # Example for List of Agents Model
    initial_population = ['a', 'a', 'b']
    history = run_list_of_agents_model(initial_population, timesteps=5, mutation_rate=0.1)
    for i, pop in enumerate(history):
        count_a = pop.count('a')
        count_b = pop.count('b')
        print(f"List Model - Time {i}: size={len(pop)}, a={count_a}, b={count_b}")

    print("\n" + "="*50 + "\n")

    # Example for Simple Grid World Model (single occupancy)
    grid_history = run_simple_grid_world(rows=10, cols=10, initial_fill=0.2, 
                                         reproduction_prob=0.1, timesteps=5,
                                         mutation_rate=0.0, death_prob=0.0, 
                                         allow_multiple=False)
    for i, g in enumerate(grid_history):
        count_a, count_b = 0, 0
        for row in g:
            count_a += row.count('a')
            count_b += row.count('b')
        print(f"Grid Model - Time {i}: a={count_a}, b={count_b}, total={count_a+count_b}")
