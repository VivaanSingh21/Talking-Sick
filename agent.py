from vector2d import Vector2D
import random
import math


class Agent:
    """Represents an individual agent in the simulation"""
    
    def __init__(self, position, velocity, energy, agent_radius=5.0):
        """
        Initialize an agent
        
        Args:
            position: Vector2D - starting position
            velocity: Vector2D - initial velocity
            energy: float - energy level (determines movement behavior)
            agent_radius: float - radius for collision detection
        """
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.energy = energy
        self.radius = agent_radius
        
        # Track movement state
        self.is_moving = True
        self.movement_time = 0.0
        
        # Store initial velocity magnitude for reference
        self.base_speed = velocity.magnitude()
    
    def update(self, delta_time, std_dev=0.0):
        """
        Update agent position based on velocity
        
        Args:
            delta_time: float - time step
            std_dev: float - standard deviation for velocity randomness
        """
        if not self.is_moving:
            return
        
        # Add randomness to velocity if specified
        if std_dev > 0:
            random_vel = self.velocity.copy()
            random_vel.add_randomness(std_dev)
            self.position = self.position + random_vel * delta_time
        else:
            self.position = self.position + self.velocity * delta_time
        
        # Update movement time
        self.movement_time += delta_time
        
        # Check if agent should stop (based on energy)
        # Assumption: energy determines how long agent can move
        # Higher energy = longer movement time
        if self.movement_time >= self.energy:
            self.is_moving = False
            self.velocity = Vector2D(0, 0)
    
    def can_move(self):
        """Check if agent has energy left to move"""
        return self.is_moving
    
    def detect_collision(self, other_agent, interaction_radius):
        """
        Check if this agent is within interaction radius of another agent
        
        Args:
            other_agent: Agent - the other agent
            interaction_radius: float - radius for interaction
            
        Returns:
            bool - True if within interaction radius
        """
        distance = self.position.distance_to(other_agent.position)
        return distance <= interaction_radius
    
    def interact_with_agent(self, other_agent):
        """
        Handle interaction with another agent (move tangentially)
        
        Args:
            other_agent: Agent - the other agent to interact with
        """
        if not self.is_moving:
            return
        
        # Calculate vector from other agent to this agent
        direction = self.position - other_agent.position
        
        if direction.magnitude() == 0:
            return  # Agents at same position, skip
        
        # Calculate tangent (perpendicular to radial direction)
        # Rotate direction by 90 degrees
        tangent = direction.rotate(math.pi / 2).normalize()
        
        # Set velocity to tangent direction, maintaining speed
        speed = self.velocity.magnitude()
        if speed > 0:
            self.velocity = tangent * speed
    
    def interact_with_boundary(self, boundary):
        """
        Handle interaction with boundary
        
        Args:
            boundary: Boundary - the boundary object
        """
        if not self.is_moving:
            return
        
        # Check if agent is near boundary
        if boundary.is_near_boundary(self.position, self.radius):
            # Get tangent at boundary
            tangent = boundary.get_tangent_at_point(self.position)
            
            # Set velocity to tangent direction
            speed = self.velocity.magnitude()
            if speed > 0:
                self.velocity = tangent * speed
            
            # Push agent slightly away from boundary to prevent getting stuck
            normal = boundary.get_normal_at_point(self.position)
            self.position = self.position + normal * 2.0
    
    def __repr__(self):
        return f"Agent(pos={self.position}, vel={self.velocity}, energy={self.energy:.2f}, moving={self.is_moving})"
