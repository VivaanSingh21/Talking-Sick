import math
import random


class Vector2D:
    """2D vector class for position and velocity calculations"""
    
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        """Add two vectors"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtract two vectors"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiply vector by scalar"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        """Right multiplication by scalar"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        """Divide vector by scalar"""
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def magnitude(self):
        """Calculate vector magnitude"""
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        """Return normalized vector (unit vector)"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def distance_to(self, other):
        """Calculate distance to another vector"""
        return (self - other).magnitude()
    
    def dot(self, other):
        """Dot product with another vector"""
        return self.x * other.x + self.y * other.y
    
    def angle(self):
        """Get angle of vector in radians"""
        return math.atan2(self.y, self.x)
    
    def rotate(self, angle):
        """Rotate vector by angle (radians)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def add_randomness(self, std_dev):
        """Add Gaussian noise to vector components"""
        self.x += random.gauss(0, std_dev)
        self.y += random.gauss(0, std_dev)
    
    def copy(self):
        """Return a copy of this vector"""
        return Vector2D(self.x, self.y)
    
    def __repr__(self):
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"
