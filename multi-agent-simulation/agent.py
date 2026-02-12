from vector2d import Vector2D
import random
import math
import numpy as np

class Agent:
    """Represents an individual agent in the simulation"""
    
    def __init__(self, position, velocity, energy, agent_radius=5.0, nrg_decay=0.1, nrg_gain=0.01):
        """
        Initialize an agent
        
        Args:
            position: Vector2D - starting position
            velocity: Vector2D - initial velocity
            energy: float - energy level (determines movement behavior)
            agent_radius: float - radius for collision detection
            nrg_decay: rate at which energy should decay each time step
            nrg_gain: rate at which energy should be restored each time step
        """
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.energy = energy
        self.radius = agent_radius
        self.nrg_decay = nrg_decay
        self.nrg_gain = nrg_gain
        
        # Track movement state
        self.is_moving = True
        self.movement_time = 0.0
        
        # Store initial velocity magnitude for reference
        self.base_speed = velocity.magnitude()

        # Equivalent to initial energy value, agent will never gain more than this from resting
        self.max_energy = energy
    
    def update(self, delta_time, std_dev=0.0):
        """
        Update agent position based on velocity
        
        Args:
            delta_time: float - time step
            std_dev: float - standard deviation for velocity randomness
        """
        if self.is_moving:
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
            """if self.movement_time >= self.energy:
                self.is_moving = False
                self.velocity = Vector2D(0, 0)"""
        # Still need to update energy if stopped so that energy is regained
        self.energy_update(delta_time)
    
    def energy_update(self, delta_time):
        """Decays or regains energy based on self.is_moving"""
        if self.is_moving:
            # Energy decay
            # Agent should slow down overtime based on decaying energy
            self.energy *= np.exp(-self.nrg_decay * delta_time)
            self.velocity = self.velocity.__mul__(self.energy)
            #Current code will never let velo reach 0; asymptote exists. Figure out at what point it stops appearing like its moving?
            #Should this be based on velocity, or should stoppage be based on an energy threshold?
            #Right now, agents may stop based on getting too slow before energy ever reaches 0, causing quick slowdowns
            if self.velocity.magnitude() < 1:
                self.velocity = 0
                self.is_moving = False
        else:
            # Restore some of the agent's max energy
            self.energy += (self.nrg_gain * self.max_energy)
            # Agent's energy should never exceed its max energy
            self.energy = min(self.energy , self.max_energy)

            # Decide if should start moving again once max energy restored
            # Randomly decides if should move again right away or wait another timestep
            # Should agents only ever start moving again upon restoration of max energy? Or can they start moving before that?
            if (self.energy == self.max_energy) and ((np.random.uniform(0 , 1)) < 0.3):
                self.is_moving = True
                # Should this just repick a new velocity or follow original speed? should angle be repicked or continue going same direction?
                angle = random.uniform(0, 2 * math.pi)
                self.velocity = Vector2D(math.cos(angle) * self.base_speed, math.sin(angle) * self.base_speed)
    
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
        buffer = 15.0  # tune this
        if boundary.is_near_boundary(self.position, self.radius + buffer):
  
            # Get tangent at boundary
            tangent = boundary.get_tangent_at_point(self.position)

            # keep the tangent direction consistent with current motion
            if self.velocity.dot(tangent) < 0:
                tangent = tangent * -1

            speed = self.velocity.magnitude()
            self.velocity = tangent * speed
            
            # Push agent slightly away from boundary to prevent getting stuck
            normal = boundary.get_normal_at_point(self.position)
            self.position = self.position + normal * 2.0
    
    def __repr__(self):
        return f"Agent(pos={self.position}, vel={self.velocity}, energy={self.energy:.2f}, moving={self.is_moving})"
