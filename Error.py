from Point import Point

class Error():
    '''Implements various Functions to sarch and Find errors in the Pattern calculations'''
    def __init__(self, center):
        self.center = center

    def dist_to_center(self, *args):
        '''calculates and prints the length of variuos points to a centerpoint'''
        for count, p in enumerate(args):
            radius = (self.center.distance(p))
            print(f"Point {count + 1}: {radius}")

if __name__ == '__main__':
    e = Error(Point(0,0))
    e.dist_to_center(Point(1,1), Point.from_polar(45, 2**0.5))