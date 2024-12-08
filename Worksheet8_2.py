import random
import matplotlib.pyplot as plt
import numpy as np

############################
# 1. List of Agents Model
############################

def run_list_of_agents_model(initial_population, timesteps, mutation_rate=0.0):
    population = initial_population[:]
    population_history = [population]

    for _ in range(timesteps):
        new_population = []
        for agent in population:
            # Parent reproduces an identical offspring (with possible mutation)
            offspring_type = agent
            if random.random() < mutation_rate:
                offspring_type = 'a' if agent == 'b' else 'b'
            # Add both parent and offspring to the next generation
            new_population.append(agent)
            new_population.append(offspring_type)
        population = new_population
        population_history.append(population)
    return population_history

############################
# 2. Simple Grid World Model
############################

def get_neighbors(r, c, rows, cols):
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def run_simple_grid_world(rows, cols, initial_fill=0.2, reproduction_prob=0.1, timesteps=10, mutation_rate=0.0):
    # Initialize grid
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    num_to_fill = int(rows*cols*initial_fill)
    all_positions = [(r,c) for r in range(rows) for c in range(cols)]
    random.shuffle(all_positions)
    for i in range(num_to_fill):
        r, c = all_positions[i]
        grid[r][c] = random.choice(['a','b'])

    grid_history = []
    grid_history.append([row[:] for row in grid])

    for _ in range(timesteps):
        offspring_positions = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] in ['a','b']:
                    if random.random() < reproduction_prob:
                        nbrs = get_neighbors(r,c, rows, cols)
                        free_nbrs = [(nr, nc) for (nr,nc) in nbrs if grid[nr][nc] == '.']
                        if free_nbrs:
                            nr, nc = random.choice(free_nbrs)
                            new_type = grid[r][c]
                            if random.random() < mutation_rate:
                                new_type = 'b' if new_type == 'a' else 'a'
                            offspring_positions.append((nr, nc, new_type))
        # Place offspring
        for (nr, nc, tp) in offspring_positions:
            if grid[nr][nc] == '.':
                grid[nr][nc] = tp

        grid_history.append([row[:] for row in grid])

    return grid_history

############################
# Analyze & Plot Results
############################

def count_types_in_list(population):
    a_count = population.count('a')
    b_count = population.count('b')
    return a_count, b_count

def count_types_in_grid(grid):
    a_count = 0
    b_count = 0
    for row in grid:
        a_count += row.count('a')
        b_count += row.count('b')
    return a_count, b_count

# Parameters
timesteps = 20

### Run List of Agents Model
initial_population = ['a']  # start with only 'a'
mutation_rate = 0.05
loam_history = run_list_of_agents_model(initial_population, timesteps, mutation_rate)

loam_a = []
loam_b = []
loam_total = []
for pop in loam_history:
    a_count, b_count = count_types_in_list(pop)
    loam_a.append(a_count)
    loam_b.append(b_count)
    loam_total.append(a_count + b_count)

# Theoretical expectation for list of agents model:
# p_{t+1} = 2 p_t -> exponential growth.
# If starting with p_0 = 1, then p_t = 2^t
# Let's produce a theoretical curve:
t_points = np.arange(timesteps+1)
theoretical_loam = 2**t_points  # no mutation scenario

### Run Simple Grid World Model
rows, cols = 20, 20
gw_history = run_simple_grid_world(rows, cols, initial_fill=0.05, reproduction_prob=0.1, timesteps=timesteps, mutation_rate=0.05)

gw_a = []
gw_b = []
gw_total = []
for g in gw_history:
    a_count, b_count = count_types_in_grid(g)
    gw_a.append(a_count)
    gw_b.append(b_count)
    gw_total.append(a_count + b_count)

# Theoretical expectation for simple grid world:
# logistic growth: dp/dt = r p (1 - p/K), with K = rows * cols
K = rows * cols
# Approximate discrete logistic:
# p_{t+1} ~ p_t + r p_t (1 - p_t/K)
# For illustration, let's pick r ~ 0.1 (based on reproduction_prob)
r = 0.1
theoretical_gw = [gw_total[0]]
for i in range(1, timesteps+1):
    p_prev = theoretical_gw[-1]
    p_next = p_prev + r * p_prev * (1 - p_prev/K)
    theoretical_gw.append(p_next)


### Plot Results
plt.figure(figsize=(12,5))

# List of Agents Model - ABM vs Theory
plt.subplot(1,2,1)
plt.plot(t_points, loam_total, 'o-', label='ABM total')
plt.plot(t_points, theoretical_loam, 'r--', label='Theory (Exponential)')
plt.xlabel("Time")
plt.ylabel("Population Size")
plt.title("List of Agents Model")
plt.legend()

# Simple Grid World - ABM vs Theory
plt.subplot(1,2,2)
plt.plot(t_points, gw_total, 'o-', label='ABM total')
plt.plot(t_points, theoretical_gw, 'r--', label='Theory (Logistic Approx.)')
plt.xlabel("Time")
plt.ylabel("Population Size")
plt.title("Simple Grid World Model")
plt.legend()

plt.tight_layout()
plt.show()
