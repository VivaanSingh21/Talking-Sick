import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from simulation import Simulation


class SimulationVisualizer:
    """Visualizes the multi-agent simulation using matplotlib animation"""
    
    def __init__(self, simulation, figsize=(8, 8)):
        """
        Initialize visualizer
        
        Args:
            simulation: Simulation object
            figsize: tuple - figure size
        """
        self.sim = simulation
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Get initial positions
        positions = np.array(self.sim.get_agent_positions())
        
        # Create unique colors for each agent
        num_agents = len(self.sim.agents)
        self.colors = plt.cm.tab20(np.linspace(0, 1, num_agents))
        
        # Create scatter plot
        self.scat = self.ax.scatter(
            positions[:, 0], 
            positions[:, 1], 
            s=100, 
            c=self.colors,
            alpha=0.7,
            edgecolors='black',
            linewidths=1
        )
        
        # Set up plot
        self.ax.set_xlim(0, self.sim.boundary.width)
        self.ax.set_ylim(0, self.sim.boundary.height)
        self.ax.set_xlabel("X position", fontsize=12)
        self.ax.set_ylabel("Y position", fontsize=12)
        self.ax.set_title("Multi-Agent Simulation", fontsize=14)
        self.ax.set_aspect('equal')
        
        # Add grid
        self.ax.grid(True, alpha=0.3)
        
        # Draw boundary box
        self.ax.add_patch(plt.Rectangle(
            (0, 0), 
            self.sim.boundary.width, 
            self.sim.boundary.height,
            fill=False, 
            edgecolor='red', 
            linewidth=2
        ))
        
        # Text for statistics
        self.info_text = self.ax.text(
            0.02, 0.98, '', 
            transform=self.ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10
        )
    
    def update(self, frame):
        """
        Update function for animation
        
        Args:
            frame: int - frame number
        """
        # Update simulation
        self.sim.update()
        
        # Get new positions
        positions = np.array(self.sim.get_agent_positions())
        
        # Update scatter plot
        self.scat.set_offsets(positions)
        
        # Update colors based on movement state
        colors_with_alpha = []
        for i, agent in enumerate(self.sim.agents):
            color = list(self.colors[i])
            if not agent.is_moving:
                color[3] = 0.3  # Fade out stopped agents
            else:
                color[3] = 0.8
            colors_with_alpha.append(color)
        
        self.scat.set_facecolors(colors_with_alpha)
        
        # Update statistics
        moving_count = sum(1 for agent in self.sim.agents if agent.is_moving)
        info = (f"Step: {frame}\n"
                f"Time: {self.sim.current_time:.2f}s\n"
                f"Moving: {moving_count}/{len(self.sim.agents)}")
        self.info_text.set_text(info)
    
    def animate(self, num_frames=500, interval=20, save_as=None):
        """
        Run animation
        
        Args:
            num_frames: int - number of frames to animate
            interval: int - milliseconds between frames
            save_as: str - filename to save animation (optional)
        """
        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames=num_frames, 
            interval=interval,
            blit=False
        )
        
        if save_as:
            print(f"Saving animation to {save_as}...")
            ani.save(save_as, writer='pillow', fps=30)
            print("Animation saved!")
        
        plt.show()
        
        return ani


def run_visual_simulation():
    """Main function to run simulation with visualization"""
    
    print("=" * 60)
    print("Multi-Agent Simulation - Visual Mode")
    print("=" * 60)
    
    # Create simulation
    sim = Simulation(
        boundary_width=800,
        boundary_height=600,
        interaction_radius=50.0,
        time_step=0.1,
        random_std_dev=0.5
    )
    
    # Initialize agents
    sim.initialize_agents(
        num_agents=20,
        energy_range=(5.0, 25.0),
        speed_range=(15.0, 30.0)
    )
    
    print(f"\nSimulation setup:")
    print(f"  Boundary: {sim.boundary.width} x {sim.boundary.height}")
    print(f"  Agents: {len(sim.agents)}")
    print(f"  Interaction radius: {sim.interaction_radius}")
    print(f"  Time step: {sim.time_step}")
    print(f"  Randomness: {sim.random_std_dev}")
    print("\nStarting animation...")
    print("Close the window to end the simulation.\n")
    
    # Create visualizer and run
    viz = SimulationVisualizer(sim)
    viz.animate(num_frames=500, interval=20)


if __name__ == "__main__":
    run_visual_simulation()
