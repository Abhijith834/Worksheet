import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Define the TreasureHunter class
class TreasureHunter:
    def __init__(self, n_locations=10):
        self.n_locations = n_locations
        self.beliefs = np.full(n_locations, 1 / n_locations)

    def reset(self):
        self.beliefs = np.full(self.n_locations, 1 / self.n_locations)

    def where_to_go(self):
        max_belief = np.max(self.beliefs)
        candidates = np.where(self.beliefs == max_belief)[0]
        chosen_location = random.choice(candidates)
        print(f"Agent deciding to visit location {chosen_location} with probability {max_belief:.2f}")
        return chosen_location

    def update_location_empty(self, location):
        self.beliefs[location] = 0.0
        remaining_sum = np.sum(self.beliefs)
        if remaining_sum > 0:
            self.beliefs /= remaining_sum
        formatted_beliefs = [f"{prob:.4f}" for prob in self.beliefs]
        print(f"Updated probabilities after finding location {location} empty: {formatted_beliefs}")


# Define the World class
class World:
    def __init__(self, n_locations=10, n_turns=1000):
        self.n_locations = n_locations
        self.n_turns = n_turns
        self.treasure_location = random.randint(0, n_locations - 1)
        self.visits = np.zeros(n_locations, dtype=int)

    def run_simulation(self, max_runs=None, delay=None):
        for turn in range(self.n_turns if max_runs is None else max_runs):
            print(f"\n--- Turn {turn + 1} ---")
            agent = TreasureHunter(self.n_locations)
            found_treasure = False

            while not found_treasure:
                location = agent.where_to_go()
                self.visits[location] += 1

                if location == self.treasure_location:
                    print(f"Agent found the treasure at location {location} and retires!")
                    found_treasure = True
                else:
                    print(f"Agent visited location {location}, found it empty.")
                    agent.update_location_empty(location)
                
                # Introduce delay if required
                if delay:
                    time.sleep(delay / 1000)

# Ask the user for simulation mode
print("Choose an option:\n1. Run with time delay for each agent (with customizable max runs)\n2. Run 1000 turns fast without delay")
choice = int(input("Enter 1 or 2: "))

if choice == 1:
    max_runs = int(input("Enter the maximum number of agent runs: "))
    world = World(n_locations=10)
    world.run_simulation(max_runs=max_runs, delay=400)
elif choice == 2:
    world = World(n_locations=10, n_turns=1000)
    world.run_simulation()

# Display the results in a bar chart
plt.figure(figsize=(10, 6))
plt.bar(range(world.n_locations), world.visits, color="skyblue")
plt.xlabel("Location")
plt.ylabel("Number of Visits")
plt.title("Number of Visits to Each Location by Treasure Hunters")
plt.xticks(range(world.n_locations))
plt.show()
