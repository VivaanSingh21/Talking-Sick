from vector2d import Vector2D
import math


class Boundary:
    """Represents the simulation boundary (rectangular)"""
    
    def __init__(self, width, height):
        """
        Initialize a rectangular boundary
        
        Args:
            width: float - boundary width
            height: float - boundary height
        """
        self.width = width
        self.height = height
        self.min_x = 0
        self.max_x = width
        self.min_y = 0
        self.max_y = height
    
    def is_within_bounds(self, position):
        """
        Check if position is within boundary
        
        Args:
            position: Vector2D - position to check
            
        Returns:
            bool - True if within bounds
        """
        return (self.min_x <= position.x <= self.max_x and 
                self.min_y <= position.y <= self.max_y)
    
    def is_near_boundary(self, position, threshold):
        """
        Check if position is near boundary within threshold distance
        
        Args:
            position: Vector2D - position to check
            threshold: float - distance threshold
            
        Returns:
            bool - True if near boundary
        """
        return (position.x <= self.min_x + threshold or 
                position.x >= self.max_x - threshold or
                position.y <= self.min_y + threshold or 
                position.y >= self.max_y - threshold)
    
    def get_tangent_at_point(self, position):
        """
        Get tangent vector at boundary point
        
        Args:
            position: Vector2D - position near boundary
            
        Returns:
            Vector2D - normalized tangent vector
        """
        # Determine which boundary is closest
        dist_left = abs(position.x - self.min_x)
        dist_right = abs(position.x - self.max_x)
        dist_bottom = abs(position.y - self.min_y)
        dist_top = abs(position.y - self.max_y)
        
        min_dist = min(dist_left, dist_right, dist_bottom, dist_top)
        
        # Return tangent based on closest boundary
        if min_dist == dist_left or min_dist == dist_right:
            # Left or right wall - tangent is vertical
            return Vector2D(0, 1)
        else:
            # Top or bottom wall - tangent is horizontal
            return Vector2D(1, 0)
    
    def get_normal_at_point(self, position):
        """
        Get normal (outward) vector at boundary point
        
        Args:
            position: Vector2D - position near boundary
            
        Returns:
            Vector2D - normalized normal vector pointing inward
        """
        # Determine which boundary is closest
        dist_left = abs(position.x - self.min_x)
        dist_right = abs(position.x - self.max_x)
        dist_bottom = abs(position.y - self.min_y)
        dist_top = abs(position.y - self.max_y)
        
        min_dist = min(dist_left, dist_right, dist_bottom, dist_top)
        
        # Return inward normal based on closest boundary
        if min_dist == dist_left:
            return Vector2D(1, 0)  # Push right
        elif min_dist == dist_right:
            return Vector2D(-1, 0)  # Push left
        elif min_dist == dist_bottom:
            return Vector2D(0, 1)  # Push up
        else:
            return Vector2D(0, -1)  # Push down
    
    def clamp_position(self, position):
        """
        Clamp position to stay within boundary
        
        Args:
            position: Vector2D - position to clamp
            
        Returns:
            Vector2D - clamped position
        """
        clamped_x = max(self.min_x, min(position.x, self.max_x))
        clamped_y = max(self.min_y, min(position.y, self.max_y))
        return Vector2D(clamped_x, clamped_y)
    
    def __repr__(self):
        return f"Boundary(width={self.width}, height={self.height})"
