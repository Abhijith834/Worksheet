import numpy as np
import random
import time

class Ant:
    def __init__(self, position):
        self.position = position

    def move(self, direction):
        # Move ant based on the given direction
        row, col = self.position
        if direction == "north" and row > 0:
            self.position = (row - 1, col)
        elif direction == "south" and row < 3:
            self.position = (row + 1, col)
        elif direction == "east" and col > 0:
            self.position = (row, col - 1)
        elif direction == "west" and col < 5:
            self.position = (row, col + 1)

class GridWorld:
    def __init__(self, pheromons):
        self.grid = np.full((4, 6), "")
        self.food = [(3, 5), (3, 0)]
        self.grid[0, 0] = "H"
        self.ant = Ant((0, 0))
        self.pheromon_list = []
        self.MaxPheromons = pheromons

    def leave_pheromon(self, position):
        self.pheromon_list.append(position)
        if len(self.pheromon_list) > self.MaxPheromons:
            del self.pheromon_list[0]

    def move_ant(self, direction): # Move the ant in the specified direction
        self.ant.move(direction)
        self.leave_pheromon(self.ant.position)

    def find_food(self):
        if self.ant.position in self.food:
            print("Found food!!!")
            return True
        return False

    def go_home(self): # Move the ant back home by following the pheromone trail in reverse
        print("Returning home...")
        for position in reversed(self.pheromon_list):
            self.ant.position = position
            self.display_grid()
            time.sleep(0.17)
            if self.ant.position == (0, 0):  # Check if ant has reached home
                print("Ant has returned home.")
                return True
        print("Ant ran out of pheromones while returning home.")
        return False

    def display_grid(self): # Display the grid with the ant's position marked as "A"
        for r in range(self.grid.shape[0]):
            row_display = []
            for c in range(self.grid.shape[1]):
                if (r, c) == self.ant.position:
                    row_display.append(" A ")
                elif (r, c) in self.food:
                    row_display.append(" F ")
                elif (r, c) in self.pheromon_list:
                    row_display.append(" P ")
                else:
                    row_display.append(f"{self.grid[r, c]:^3}")
            print("[" + "|".join(row_display) + "]")
        print()


initial_pheromons = 1
found_home = False

while not found_home:
    print(f"Starting episode with MaxPheromons = {initial_pheromons}")
    gridworld = GridWorld(initial_pheromons)
    step_count = 0

    while True:
        step_count += 1
        L = ["north", "south", "east", "west"]
        direction = random.choice(L)
        gridworld.move_ant(direction)
        print(f"Step {step_count}")
        gridworld.display_grid()
        time.sleep(0.17)
        
        if gridworld.find_food():
            # Try to return home if food is found
            if gridworld.go_home():
                print(f"Ant successfully returned home with MaxPheromons = {initial_pheromons}")
                found_home = True
                break
            else:
                # If ant ran out of pheromones while returning, stop this episode
                print(f"Ant ran out of pheromones with MaxPheromons = {initial_pheromons}. Restarting with more pheromones.")
                initial_pheromons += 1
                break  # Exit the inner loop and start a new episode

    time.sleep(2)
