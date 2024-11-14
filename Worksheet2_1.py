import tkinter as tk # tkinter library is imported for a visual demostation of the simulation
import random # random library is imported to implement random movements of the angents

class Agent: # initiating the agent class
    def __init__(self, x, y, vx, vy):
        self.x = x  # Position in x-direction
        self.y = y  # Position in y-direction
        self.vx = vx  # Velocity in x-direction
        self.vy = vy  # Velocity in y-direction

    def move(self): # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

    def update_velocity(self, vx, vy): # Update velocity of the agent.
        self.vx = vx
        self.vy = vy

    def distance_to(self, other): # Calculate distance to another agent.
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class World: #initiating the world class
    def __init__(self, num_agents):
        self.agents = [self.create_random_agent() for _ in range(num_agents)]
        self.lead_agent = self.agents[0]

    def create_random_agent(self): # Initialize an agent with random position and velocity.
        x, y = random.uniform(-50, 50), random.uniform(-50, 50)
        vx, vy = random.uniform(-1, 1), random.uniform(-1, 1)
        return Agent(x, y, vx, vy)

    def move_agents(self): # Move all agents based on their velocities.
        for agent in self.agents:
            agent.move()

    def update_lead_velocity(self): # Change the lead agent's velocity randomly.
        self.lead_agent.update_velocity(random.uniform(-1, 1), random.uniform(-1, 1))

    def update_other_agents_velocity(self): # Update velocity of all agents based on their position relative to the lead agent.
        for agent in self.agents:
            if agent != self.lead_agent:
                dx = self.lead_agent.x - agent.x
                dy = self.lead_agent.y - agent.y
                
                # Adjust velocity towards lead agent
                agent.update_velocity(agent.vx + 0.1 * dx, agent.vy + 0.1 * dy)

    def simulate(self, steps): # Run the simulation for a given number of steps.
        for _ in range(steps):
            self.update_lead_velocity()
            self.update_other_agents_velocity()
            self.move_agents()

class SimulationApp: # makes a canver using tkinter
    def __init__(self, root, world):
        self.root = root
        self.world = world
        self.step_count = 1
        self.max_steps = 100

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.offset_x = 300
        self.offset_y = 300
        self.scale = 3  # Scale factor for converting position to screen coordinates

        self.run_simulation()

    def draw_axes(self): # Draw x and y axes with scale markers on the canvas.
        # Draw x-axis
        self.canvas.create_line(0, self.offset_y, 600, self.offset_y, fill="black")
        # Draw y-axis
        self.canvas.create_line(self.offset_x, 0, self.offset_x, 600, fill="black")

        # Draw x-axis markers and labels
        for i in range(-100, 101, 20):
            screen_x = self.offset_x + i * self.scale
            self.canvas.create_line(screen_x, self.offset_y - 5, screen_x, self.offset_y + 5, fill="black")
            self.canvas.create_text(screen_x, self.offset_y + 15, text=str(i), font=("Arial", 8))

        # Draw y-axis markers and labels
        for i in range(-100, 101, 20):
            screen_y = self.offset_y - i * self.scale
            self.canvas.create_line(self.offset_x - 5, screen_y, self.offset_x + 5, screen_y, fill="black")
            self.canvas.create_text(self.offset_x - 15, screen_y, text=str(i), font=("Arial", 8))

    def draw_agents(self): # Draw agents on the canvas.
        self.canvas.delete("all")  # Clear previous drawings
        self.draw_axes()  # Draw axes before drawing agents

        for agent in self.world.agents:
            screen_x = self.offset_x + agent.x * self.scale
            screen_y = self.offset_y - agent.y * self.scale  # Invert y-axis for graphical representation
            color = "red" if agent == self.world.lead_agent else "blue" # gives the lead agent the color red and the rest blue
            self.canvas.create_oval(
                screen_x - 5, screen_y - 5, screen_x + 5, screen_y + 5, fill=color
            )

    def print_agent_positions(self): # Print the positions of all agents.
        print(f"Step {self.step_count}:")
        for idx, agent in enumerate(self.world.agents):
            print(f"  Agent {idx}: Position ({agent.x:.2f}, {agent.y:.2f})")

    def run_simulation(self): # Run the simulation and update the display, stopping after 100 steps.
        if self.step_count <= self.max_steps:
            self.world.simulate(1)  # Run one step of the simulation
            self.draw_agents()
            self.print_agent_positions()
            self.step_count += 1
            self.root.after(100, self.run_simulation)  # Repeat every 100 ms

# Example usage
if __name__ == "__main__":
    world = World(num_agents=10)

    root = tk.Tk()
    root.title("Agent Simulation")
    app = SimulationApp(root, world)
    root.mainloop()
