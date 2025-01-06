import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Constants
NUM_SPECIES = 6
SIMULATION_TIME = 50  # Total simulation time
TIME_STEPS = 1000  # Number of time steps
REACTION_RATES = np.ones(NUM_SPECIES)  # Reaction rates for each species

def hypercycle_dynamics(x, t):
    """Compute the rate of change for each molecular species."""
    dxdt = np.zeros(NUM_SPECIES)
    total_interaction = np.sum(REACTION_RATES * x)
    
    for i in range(NUM_SPECIES):
        prev_species = x[i-1] if i > 0 else x[-1]  # Circular dependency
        dxdt[i] = x[i] * (REACTION_RATES[i] * prev_species - total_interaction)
    
    return dxdt

def check_normalization(results):
    """Check if concentrations sum to 1 at every time step."""
    for i, step in enumerate(results):
        total = np.sum(step)
        if not np.isclose(total, 1.0, atol=1e-6):
            print(f"Normalization issue at time step {i}: Total = {total:.6f}")
            return
    print("All time steps are normalized (sum to 1).")

def plot_combined_results(time, results_list, titles):
    """Plot the concentration dynamics of molecular species in a single window."""
    fig, axes = plt.subplots(len(results_list), 1, figsize=(8, 10), sharex=True)  # Reduced size by 20%
    for i, (results, title) in enumerate(zip(results_list, titles)):
        for species in range(NUM_SPECIES):
            axes[i].plot(time, results[:, species], label=f"Species {species + 1}")
        axes[i].set_title(title)
        axes[i].set_ylabel("Concentration")
        axes[i].grid()
        axes[i].legend()
    axes[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

def main():
    # Initial conditions
    initial_conditions = {
        "Case 1: All Concentrations Equal": np.full(NUM_SPECIES, 1.0 / NUM_SPECIES),
        "Case 2: Concentrations in a Range": np.array([0.15, 0.10, 0.12, 0.08, 0.20, 0.15]),
        "Case 3: x1 = 0, Others Set": np.array([0.0, 0.2, 0.2, 0.2, 0.2, 0.2])
    }

    # Time vector
    time = np.linspace(0, SIMULATION_TIME, TIME_STEPS)

    # Run simulations and collect results
    results_list = []
    for case, initial_condition in initial_conditions.items():
        results = odeint(hypercycle_dynamics, initial_condition, time)
        print(f"\n{case}:")
        check_normalization(results)
        results_list.append((results, case))

    # Plot all cases in a single window
    plot_combined_results(time, [res[0] for res in results_list], [res[1] for res in results_list])

if __name__ == "__main__":
    main()
