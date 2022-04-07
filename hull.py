import math
import random
import matplotlib.pyplot as plt

class Point:

    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)
        self.__angle = None

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def angle(self):
        return self.__angle

    def __eq__(self, other):
        if type(other) is not Point:
            return False
        return (self.x == int(other.x)) and (self.y == int(other.y))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.angle is not None:
            return '(%g, %g, %g)' % (self.__x, self.__y, self.__angle)
        else:
            return '(%g, %g)' % (self.__x, self.__y)

    # If angle exists, sort by that, else sort by y then x
    def __lt__(self, other):
        if self.angle is None or other.angle is None:
            if self.y < other.y:
                return True
            elif self.y == other.y:
                return self.x < other.x
            return False
        return self.angle < other.angle

    # Set angle between 2 points (as degrees)
    def find_angle(self, point):
        if type(point) is not Point:
            return
        if self == point:
            self.__angle = 0
        else:
            #self.__angle = math.degrees(math.atan2(point.y-self.y, point.x-self.x)) % 360
            self.__angle = math.degrees(math.atan2(self.y-point.y, self.x-point.x)) % 360

    def clear_angle(self):
        self.__angle = None

    def set_angle(self, angle):
        self.__angle = angle

    @staticmethod
    def point_copy(point):
        new_pt = Point(point.x,point.y)
        if point.angle is not None:
            new_pt.set_angle(point.angle)
        return new_pt

    @staticmethod
    def from_coordinates(coordinates):
        if len(coordinates) % 2 != 0:
            coordinates.pop() # Remove last element
        points = []
        it = iter(coordinates)
        for x in it:
            points.append(Point(x, next(it)))
        return points

def area2(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def left_on(a, b, c):
    return area2(a, b, c) >= 0

def left(a, b, c):
    return area2(a, b, c) > 0

def graham_scan(points):
    v_low = min(points) # Find min y point
    for point in points:
        point.find_angle(v_low) # Compute angle about v_low
    points.sort() # Sort by angle about v_low
    len_p = len(points)
    if len_p <= 3:
        return points
    pos = 2
    hull = points[0:2] # Initalize stack as first 2 points
    while pos < len_p:
        cur = points[pos]
        while not left_on(hull[-2], hull[-1], cur): # POP until left
            hull.pop()
        hull.append(cur)
        pos += 1
    return hull

def get_partial_hulls(points, r):
    hulls = []
    n = len(points)
    i = 0
    while i < n:
        end = i + r
        if end > n:
            end = n
        hulls.append(graham_scan(points[i:end]))
        i = end
    return hulls

def get_3pt_angle(a, b, c):
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return ang + 360 if ang < 0 else ang

# This is a testing method to perform finding the tangency in O(m) instead of O(log m)
def non_bin_search_hull(hull, llast_pt, last_pt): # TODO: This doesnt work
    for point in hull:
        if point == last_pt:
            point.set_angle(0)
        else:
            point.set_angle(get_3pt_angle(llast_pt, last_pt, point))
    return max(hull)

def bin_search_hull(hull, llast_pt, last_pt):
    return non_bin_search_hull(hull, llast_pt, last_pt) # TODO: actually implement binary search part
    # Find the tangency point with binary search in O(log m) to each group CH
    # Set the angle of this point, as we will compare

def try_hull(points, m, pt):
    n = len(points)
    r = math.ceil(n/m)
    for point in points: # Remove the angles on the points
        point.clear_angle()
    v_low = min(points) # Get lowest point before other hulls, as this will not change
    partial_hulls = get_partial_hulls(points, r)
    if do_graph:
        plt.clf() # Clear figure
        plt.scatter(pt[0], pt[1], zorder=1, color="k") # Add points
        for hull in partial_hulls:
            plot_hull(hull)
    c_hull = [v_low]
    for i in range(m):
        new_pt = None
        for hull in partial_hulls:
            if len(c_hull) == 1:
                temp_pt = bin_search_hull(hull, c_hull[-1], c_hull[-1])
            else:
                temp_pt = bin_search_hull(hull, c_hull[-2], c_hull[-1])
            if new_pt is None or temp_pt > new_pt:
                new_pt = temp_pt
        if do_graph:
            plt.plot([c_hull[-1].x, new_pt.x], [c_hull[-1].y, new_pt.y], zorder=3, color="pink")
            plt.draw()
            plt.pause(1)
        if new_pt == v_low:
            return c_hull
        else:
            c_hull.append(new_pt)
    return None

def chan_hull(points):
    m = 4
    pt = None
    if do_graph:
        pt = get_coords(points)
    while True:
        res = try_hull(points, m, pt)
        if res is None:
            m = m**2
        else:
            return res

def get_coords(points):
    x, y = [], []
    for point in points:
        x.append(point.x)
        y.append(point.y)
    return [x, y]

def print_points(points):
    len_p = len(points)
    if len_p == 0:
        print("[]")
        return
    print("[", end = "")
    for i in range(len_p-1):
        print(str(points[i]) + ", ", end = "")
    print(str(points[len_p-1]) + "]")

def get_points(filename):
    points = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        parts = line.split() # Split on whitespace
        for part in parts:
            try:
                cur = int(part)
                points.append(cur)
            except ValueError:
                continue
    return Point.from_coordinates(points)

def generate_random_points(num_points, low = -100, high = 100):
    if high < low:
        high, low = low, high
    num_points *= 2 # Generate x and y values for each point
    points = []
    for i in range(num_points):
        points.append(random.randint(low, high))
    return Point.from_coordinates(points)
    #return points

def plot_hull(hull):
    hull.append(hull[0]) # Add first to end to get full lines
    hl = get_coords(hull)
    plt.plot(hl[0], hl[1], zorder=2)
    plt.draw()
    plt.pause(1)

do_graph = True

if __name__ == "__main__":
    points = get_points("points.txt")
    points = generate_random_points(1000, -1000, 1000)
    #points = Point.from_coordinates(points)
    chans_hull = chan_hull(points)
    print_points(chans_hull)
    if do_graph:
        plt.clf() # Clear figure
        pt = get_coords(points)
        plt.scatter(pt[0], pt[1], zorder=1, color="k") # Add points
        plot_hull(chans_hull)
        plt.show()
