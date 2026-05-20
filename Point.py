import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        # We establish Cartesian as our single internal source of truth
        self._x = float(x)
        self._y = float(y)

    # --- Alternative Constructor ---
    @classmethod
    def from_polar(cls, angle_degrees, distance):
        """Creates a Point instance using polar coordinates."""
        angle_rad = math.radians(angle_degrees)
        x = math.cos(angle_rad) * distance
        y = math.sin(angle_rad) * distance
        return cls(x, y) # Calls __init__ with the calculated x and y
    
    def __add__(self, other):
        """Allows: new_point = p1 + p2"""
        if not isinstance(other, Point):
            return NotImplemented
        # Vector addition: add X components together, and Y components together
        return Point(x=self._x + other._x, y=self._y + other._y)

    def __sub__(self, other):
        """Allows: new_point = p1 - p2"""
        if not isinstance(other, Point):
            return NotImplemented
        # Vector subtraction: subtract other components from self
        return Point(x=self._x - other._x, y=self._y - other._y)
    
    def distance(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return ((self._x - other._x)**2 + (self._y - other._y)**2)**0.5
    
    # --- Getters (Properties) ---
    @property
    def cartesian(self):
        return (round(self._x, 10), round(self._y, 10))

    @property
    def polar(self):
        angle = math.degrees(math.atan2(self._y, self._x)) % 360
        distance = math.hypot(self._x, self._y) # Cleaner way to do (x^2 + y^2)^0.5
        return (round(angle, 10), round(distance, 10))

    


if __name__ == '__main__':
    p = Point(1,1)

    print(p.cartesian)
    print(p.polar)

    p1 = Point.from_polar(angle_degrees=45, distance=2**0.5)

    print(p1.cartesian)
    print(p1.polar)

    p2 = p + p1

    print(p2.cartesian)