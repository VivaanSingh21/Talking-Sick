from vector2d import Vector2D
from agent import Agent
from boundary import Boundary
import random
import math


class Simulation:
    """Manages the multi-agent simulation"""
    
    def __init__(self, boundary_width=800, boundary_height=600, 
                 interaction_radius=50.0, time_step=0.1, random_std_dev=0.1):
        """
        Initialize simulation
        
        Args:
            boundary_width: float - width of simulation area
            boundary_height: float - height of simulation area
            interaction_radius: float - radius for agent interactions
            time_step: float - time step for updates
            random_std_dev: float - standard deviation for velocity randomness
        """
        self.boundary = Boundary(boundary_width, boundary_height)
        self.agents = []
        self.interaction_radius = interaction_radius
        self.time_step = time_step
        self.random_std_dev = random_std_dev
        self.current_time = 0.0
    
    def initialize_agents(self, num_agents, energy_range=(5.0, 20.0), 
                         speed_range=(10.0, 30.0)):
        """
        Create agents with random positions, velocities, and varying energy
        
        Args:
            num_agents: int - number of agents to create
            energy_range: tuple - (min_energy, max_energy)
            speed_range: tuple - (min_speed, max_speed)
        """
        self.agents = []
        
        for i in range(num_agents):
            # Random position within boundary (with margin)
            margin = 20
            pos_x = random.uniform(margin, self.boundary.width - margin)
            pos_y = random.uniform(margin, self.boundary.height - margin)
            position = Vector2D(pos_x, pos_y)
            
            # Random velocity direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            velocity = Vector2D(math.cos(angle) * speed, math.sin(angle) * speed)
            
            # Random energy within range
            energy = random.uniform(energy_range[0], energy_range[1])
            
            # Create agent
            agent = Agent(position, velocity, energy)
            self.agents.append(agent)
        
        print(f"Initialized {num_agents} agents")
    
    def check_interactions(self):
        """Check and handle agent-agent interactions"""
        # Check all pairs of agents
        for i in range(len(self.agents)):
            for j in range(i + 1, len(self.agents)):
                agent1 = self.agents[i]
                agent2 = self.agents[j]
                
                # Skip if both agents are not moving
                if not agent1.can_move() and not agent2.can_move():
                    continue
                
                # Check if agents are within interaction radius
                if agent1.detect_collision(agent2, self.interaction_radius):
                    # Both agents move tangentially to each other
                    if agent1.can_move():
                        agent1.interact_with_agent(agent2)
                    if agent2.can_move():
                        agent2.interact_with_agent(agent1)
    
    def check_boundary_collisions(self):
        """Check and handle agent-boundary interactions"""
        for agent in self.agents:
            if agent.can_move():
                agent.interact_with_boundary(self.boundary)
    
    def update(self):
        """Main simulation update - updates all agents and checks interactions"""
        # Update all agents
        for agent in self.agents:
            if agent.can_move():
                agent.update(self.time_step, self.random_std_dev)
        
        # Check agent-agent interactions
        self.check_interactions()
        
        # Check boundary interactions
        self.check_boundary_collisions()
        
        # Update time
        self.current_time += self.time_step
    
    def run(self, duration):
        """
        Run simulation for specified duration
        
        Args:
            duration: float - how long to run simulation
        """
        num_steps = int(duration / self.time_step)
        
        print(f"Running simulation for {duration} seconds ({num_steps} steps)")
        print(f"Time step: {self.time_step}, Interaction radius: {self.interaction_radius}")
        print(f"Randomness std dev: {self.random_std_dev}")
        print("-" * 60)
        
        for step in range(num_steps):
            self.update()
            
            # Print progress every 10% of steps
            if (step + 1) % max(1, num_steps // 10) == 0:
                moving_agents = sum(1 for agent in self.agents if agent.can_move())
                print(f"Step {step + 1}/{num_steps} - Time: {self.current_time:.2f}s - "
                      f"Moving agents: {moving_agents}/{len(self.agents)}")
        
        print("-" * 60)
        print("Simulation complete!")
        self.print_statistics()
    
    def print_statistics(self):
        """Print final statistics about the simulation"""
        print("\nFinal Statistics:")
        print(f"Total agents: {len(self.agents)}")
        
        moving = sum(1 for agent in self.agents if agent.can_move())
        print(f"Still moving: {moving}")
        print(f"Stopped: {len(self.agents) - moving}")
        
        # Energy distribution
        energies = [agent.energy for agent in self.agents]
        print(f"\nEnergy - Min: {min(energies):.2f}, Max: {max(energies):.2f}, "
              f"Avg: {sum(energies)/len(energies):.2f}")
        
        # Movement times
        movement_times = [agent.movement_time for agent in self.agents]
        print(f"Movement time - Min: {min(movement_times):.2f}, "
              f"Max: {max(movement_times):.2f}, "
              f"Avg: {sum(movement_times)/len(movement_times):.2f}")
    
    def get_agent_positions(self):
        """
        Get current positions of all agents
        
        Returns:
            list of tuples - [(x, y), ...] positions
        """
        return [(agent.position.x, agent.position.y) for agent in self.agents]
    
    def get_agent_states(self):
        """
        Get current state of all agents
        
        Returns:
            list of dicts - agent states
        """
        states = []
        for i, agent in enumerate(self.agents):
            states.append({
                'id': i,
                'position': (agent.position.x, agent.position.y),
                'velocity': (agent.velocity.x, agent.velocity.y),
                'energy': agent.energy,
                'is_moving': agent.is_moving,
                'movement_time': agent.movement_time
            })
        return states
    
    def __repr__(self):
        return (f"Simulation(agents={len(self.agents)}, "
                f"boundary={self.boundary.width}x{self.boundary.height}, "
                f"time={self.current_time:.2f})")
