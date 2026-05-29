import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        '''Creates a Point Instance using cartesian coordinates'''
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
        """Implements Addition of two points"""
        if not isinstance(other, Point):
            return NotImplemented
        # Vector addition: add X components together, and Y components together
        return Point(x=self._x + other._x, y=self._y + other._y)

    def __sub__(self, other):
        """Implements Subtraction of two Points"""
        if not isinstance(other, Point):
            return NotImplemented
        # Vector subtraction: subtract other components from self
        return Point(x=self._x - other._x, y=self._y - other._y)
    
    def __mul__(self, other):
        '''implements point multiplication with an int or float'''
        if isinstance(other, int | float):
            return Point(x=self._x * other, y=self._y * other)
        else:
            return NotImplemented

    
    def distance(self, other):
        '''calculates distance between two point objects'''
        if not isinstance(other, Point):
            return NotImplemented
        return ((self._x - other._x)**2 + (self._y - other._y)**2)**0.5
    
    def __str__(self):
        return f"Point: {(round(self._x,2), round(self._y, 2))}"
    
    def __repr__(self):
        return f"{(round(self._x,2), round(self._y, 2))}"
    
    # --- Getters (Properties) ---
    @property
    def cartesian(self):
        '''returns the cartesian coordinates as a tuple'''
        return (round(self._x, 10), round(self._y, 10))

    @property
    def polar(self):
        '''returns the polar coordinates as a tuple'''
        angle = math.degrees(math.atan2(self._y, self._x)) % 360
        distance = math.hypot(self._x, self._y) # Cleaner way to do (x^2 + y^2)^0.5
        return (round(angle, 10), round(distance, 10))
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y


    


if __name__ == '__main__':
    p = Point(1,1)

    print(p.cartesian)
    print(p.polar)

    p1 = Point.from_polar(angle_degrees=45, distance=2**0.5)

    print(p1.cartesian)
    print(p1.polar)

    p2 = p + p1

    print(p2.cartesian)

    print(p2)
    p2 *= 3
    print(p2)