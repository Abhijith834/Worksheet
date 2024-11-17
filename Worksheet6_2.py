import numpy as np
import matplotlib.pyplot as plt

# Define the Boid class
class Boid: # Boid setup
    def __init__(self, position, velocity, inner_radius=10, outer_radius=50):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.inner_radius = inner_radius  # Radius to avoid overcrowding
        self.outer_radius = outer_radius  # Radius to stay near the group

    def avoid_others(self, flock): #Move away from other boids that are too close.
        move_away = np.zeros(2)
        for other in flock:
            distance = np.linalg.norm(self.position - other.position)
            if 0 < distance < self.inner_radius:
                move_away -= (other.position - self.position)
        return move_away

    def stay_with_flock(self, flock): # Move closer to the center of the group.
        group_center = np.zeros(2)
        count = 0
        for other in flock:
            distance = np.linalg.norm(self.position - other.position)
            if self.inner_radius < distance < self.outer_radius:
                group_center += other.position
                count += 1
        if count > 0:
            group_center /= count
            return (group_center - self.position)
        return np.zeros(2)

    def update_position(self, flock, max_speed=5): #Update the boid's position based on its behaviors.
        
        # Calculate forces
        separation = self.avoid_others(flock)
        cohesion = self.stay_with_flock(flock)
        self.velocity += separation + cohesion # Adjust velocity
        speed = np.linalg.norm(self.velocity) # Limit speed
        if speed > max_speed:
            self.velocity = (self.velocity / speed) * max_speed

        
        self.position += self.velocity # Update position


def simulate_flock(num_boids, steps): # Function to simulate the boid flock
    """
    Create a group of boids and simulate their behavior over time.
    """
    # Initialize boids with random positions and velocities
    flock = [
        Boid(
            position=np.random.uniform(0, 100, 2),
            velocity=np.random.uniform(-2, 2, 2)
        )
        for _ in range(num_boids)
    ]

    # Track positions over time
    all_positions = []
    for _ in range(steps):
        positions = []
        for boid in flock:
            boid.update_position(flock)
            positions.append(boid.position.copy())
        all_positions.append(np.array(positions))

    return all_positions


number_of_boids = 10 # number of boids
number_of_steps = 100 # number of steps
boid_positions = simulate_flock(number_of_boids,number_of_steps) # Run the simulation

# Visualize the boid movements
for step in range(0, len(boid_positions), 10):  # Plot every 10th step
    positions = boid_positions[step]
    plt.scatter(positions[:, 0], positions[:, 1], label=f"Step {step}")

plt.title("Boid Flocking Simulation")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()
plt.show()
