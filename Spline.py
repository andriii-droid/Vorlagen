import math
from Point import Point

class Spline():
    '''calculates a spline and can draw points on that spline'''
    def __init__(self, pattern):
        '''creates a spline object and links parent pattern'''
        self.pattern = pattern

    def generate_spline(self, spline=False, num_points=2, start_point=None,
                        control_point=None, end_point=None):
        '''generates spline and points, given the parameters they get get drawn'''
        self.spline = spline
        self.num_points = num_points
    
        #calculates the startpoint in relation to the centerpoint
        self.start_point = start_point + self.pattern.center
        self.control_point = control_point + self.pattern.center
        self.end_point = end_point + self.pattern.center

        #dcalculates and draws the spline
        path = self.pattern.c.beginPath()
        path.moveTo(*self.start_point.cartesian)
        path.curveTo(*self.start_point.cartesian, *self.control_point.cartesian, *self.end_point.cartesian)
        if spline:
            self.pattern.c.drawPath(path, stroke=1)

        #calculates and draws the points on the spline
        even_points = self.get_even_points_on_curve(num_points=num_points)
        self.pattern.draw_points(even_points)
        
    def get_even_points_on_curve(self, num_points=10):
        """
        Calculates physically evenly spaced points along a Cubic Bézier curve.
        """
        # 1. Standard Cubic Bézier mathematical formula
        def bezier_point(t, p0, p1, p2, p3):
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
            return (x, y)

        # 2. High-resolution sampling to map out the curve's actual shape
        high_res_steps = 200
        points_pool = []
        distances = [0.0]
        total_length = 0.0

        # Generate a massive pool of points
        for i in range(high_res_steps + 1):
            t = i / high_res_steps
            pt = bezier_point(t, self.start_point.cartesian, 
                              self.start_point.cartesian,
                              self.control_point.cartesian, 
                              self.end_point.cartesian)
            points_pool.append(pt)
            
            if i > 0:
                # Calculate distance from the previous point
                prev = points_pool[i-1]
                dist = math.hypot(pt[0] - prev[0], pt[1] - prev[1])
                total_length += dist
                distances.append(total_length)

        # 3. Linearly interpolate to find perfectly spaced steps
        even_points = []
        step_distance = total_length / (num_points - 1)

        for i in range(num_points):
            target_dist = i * step_distance
            
            # Find where this distance fits in our distance map
            # (A quick linear scan; can be optimized with binary search if high_res_steps is massive)
            idx = 0
            while idx < len(distances) - 1 and distances[idx+1] < target_dist:
                idx += 1
                
            # Interpolate between points_pool[idx] and points_pool[idx+1]
            dist_start = distances[idx]
            dist_end = distances[idx+1]
            
            if dist_end == dist_start:
                ratio = 0.0
            else:
                ratio = (target_dist - dist_start) / (dist_end - dist_start)
                
            pt_start = points_pool[idx]
            pt_end = points_pool[idx+1]
            
            # Calculate final clean coordinate
            even_x = pt_start[0] + ratio * (pt_end[0] - pt_start[0])
            even_y = pt_start[1] + ratio * (pt_end[1] - pt_start[1])
            even_points.append(Point(even_x, even_y))

        return even_points