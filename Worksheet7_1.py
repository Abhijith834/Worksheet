import matplotlib.pyplot as plt

# Function to apply Euler's method for solving ODEs
def solve_euler(f, y_init, t_range, step):
    t_values = []
    y_values = []

    t = t_range[0]
    y = y_init
    while t <= t_range[1]:
        t_values.append(t)
        y_values.append(y)
        y += f(t, y) * step  # Euler update for y
        t += step  # Increment time
    return t_values, y_values

# Define the ODE dy/dt = -2y
def model(t, y):
    return -2 * y

# Simulation setup
initial_y = 1  # Initial condition y(0)
time_interval = (0, 5)  # Time range [start, end]
time_step = 0.1  # Step size

# Solve the equation
time_series, solution = solve_euler(model, initial_y, time_interval, time_step)

# Visualization
plt.figure(figsize=(8, 5))
plt.plot(time_series, solution, label=f"Euler ∆t={time_step}")
plt.xlabel("Time (t)")
plt.ylabel("y(t)")
plt.title("Euler's Method Applied to dy/dt = -2y")
plt.legend(loc="upper right")
plt.grid(True)
plt.show()
