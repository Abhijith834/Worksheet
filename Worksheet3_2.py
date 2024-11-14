import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Define the TreasureHunter class with Bayesian Updating capability
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
        return chosen_location

    def update_location_empty(self, location):
        self.beliefs[location] = 0.0
        remaining_sum = np.sum(self.beliefs)
        if remaining_sum > 0:
            self.beliefs /= remaining_sum

    def social_bayesian_update(self, observed_location, p_a_given_t=0.18):
        # Bayesian update based on another hunter's observed action
        p_a_given_not_t = (1 - p_a_given_t) / (self.n_locations - 1)
        
        # Updating probabilities using Bayes' rule
        for i in range(self.n_locations):
            if i == observed_location:
                self.beliefs[i] *= p_a_given_t
            else:
                self.beliefs[i] *= p_a_given_not_t
        
        # Normalize to ensure they sum to 1
        self.beliefs /= np.sum(self.beliefs)

# Define the MultiAgentWorld class
class MultiAgentWorld:
    def __init__(self, n_locations=10, k_hunters=10, n_turns=100):
        self.n_locations = n_locations
        self.k_hunters = k_hunters
        self.n_turns = n_turns
        self.treasure_location = random.randint(0, n_locations - 1)
        self.hunters = [TreasureHunter(n_locations) for _ in range(k_hunters)]
        self.findings_with_update = 0
        self.findings_without_update = 0

    def run_simulation(self, social_update=True):
        for turn in range(self.n_turns):
            hunter_index = turn % self.k_hunters  # Determine which hunter's turn it is
            current_hunter = self.hunters[hunter_index]
            location = current_hunter.where_to_go()

            # Check if the current hunter finds the treasure
            if location == self.treasure_location:
                if social_update:
                    self.findings_with_update += 1
                else:
                    self.findings_without_update += 1
                current_hunter.reset()  # Replace the hunter with a new one
            else:
                current_hunter.update_location_empty(location)

            # Social Bayesian Update for other hunters if enabled
            if social_update:
                for i, hunter in enumerate(self.hunters):
                    if i != hunter_index:
                        hunter.social_bayesian_update(location)

    def run_comparison(self):
        # Run simulation with social Bayesian updates
        self.run_simulation(social_update=True)
        with_update_results = self.findings_with_update
        
        # Reset counts and hunters, run simulation without social Bayesian updates
        self.findings_with_update = 0
        self.hunters = [TreasureHunter(self.n_locations) for _ in range(self.k_hunters)]
        self.run_simulation(social_update=False)
        without_update_results = self.findings_without_update
        
        return with_update_results, without_update_results

# Run the multi-agent world simulation and compare findings
world = MultiAgentWorld(n_locations=10, k_hunters=10, n_turns=1000)
with_update, without_update = world.run_comparison()

# Display results
print(f"Findings with Social Bayesian Update: {with_update}")
print(f"Findings without Social Bayesian Update: {without_update}")
