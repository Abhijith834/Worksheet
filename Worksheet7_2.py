import matplotlib.pyplot as plt

# Function to simulate an SIR model
def simulate_sir(initial_conditions, parameters, time_step, duration):
    S, I, R = [initial_conditions['S']], [initial_conditions['I']], [initial_conditions['R']]
    beta, gamma = parameters['beta'], parameters['gamma']
    time_steps = int(duration / time_step)

    for _ in range(time_steps):
        dS = -beta * S[-1] * I[-1] * time_step
        dI = (beta * S[-1] * I[-1] - gamma * I[-1]) * time_step
        dR = gamma * I[-1] * time_step

        S.append(S[-1] + dS)
        I.append(I[-1] + dI)
        R.append(R[-1] + dR)

    return S, I, R

# Model parameters and initial conditions
initial_conditions = {'S': 0.99, 'I': 0.01, 'R': 0}
parameters = {'beta': 0.3, 'gamma': 0.1}
time_step = 0.1
duration = 160

# Run the simulation
S, I, R = simulate_sir(initial_conditions, parameters, time_step, duration)

# Generate time points
time_points = [i * time_step for i in range(len(S))]

# Visualization
plt.figure(figsize=(10, 6))
plt.plot(time_points, S, label="Susceptible", linewidth=2)
plt.plot(time_points, I, label="Infected", linewidth=2)
plt.plot(time_points, R, label="Recovered", linewidth=2)
plt.xlabel("Time (days)", fontsize=12)
plt.ylabel("Proportion of Population", fontsize=12)
plt.title("SIR Model Dynamics", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
