import math
import matplotlib.pyplot as plt
import argparse
import numpy as np

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

    def __gt__(self, other):
        if self.angle is None or other.angle is None:
            if self.y > other.y:
                return True
            elif self.y == other.y:
                return self.x > other.x
            return False
        return self.angle > other.angle

    # Set angle between 2 points (as degrees)
    def find_angle(self, point):
        if type(point) is not Point:
            return
        if self == point:
            self.__angle = 0
        else:
            self.__angle = math.degrees(math.atan2(self.y-point.y, self.x-point.x)) % 360

    def find_3pt_angle(self, a, b):
        self.__angle = get_3pt_angle(a, b, self)

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
            pt = Point(x, next(it))
            points.append(pt)
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
        hulls.append(graham_scan(points[i:end].copy()))
        i = end
    return hulls

def get_3pt_angle(a, b, c):
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return ang + 360 if ang < 0 else ang

def smart_angle_set(point, llast_pt, last_pt):
    if point == last_pt:
        point.set_angle(0)
    else:
        point.find_3pt_angle(llast_pt, last_pt)

def is_local_max(hull, llast_pt, last_pt, index):
    n = len(hull)
    pt = hull[index]
    l_pt = hull[index-1] # If this is -1, its okay
    r_pt = hull[(index+1) % n] # But if this is n, that is bad
    smart_angle_set(pt, llast_pt, last_pt)
    smart_angle_set(l_pt, llast_pt, last_pt)
    smart_angle_set(r_pt, llast_pt, last_pt)
    max_pt = max(pt, l_pt, r_pt)
    return max_pt == pt

# This is a testing method to perform finding the tangency in O(m) instead of O(log m)
# However, if m is small, this method will be faster.
def find_tan(hull, llast_pt, last_pt):
    for point in hull:
        smart_angle_set(point, llast_pt, last_pt)
    return max(hull)

def bin_roated(hull, low, high, llast_pt, last_pt):
    smart_angle_set(hull[low], llast_pt, last_pt)
    # If there is only one element left
    if high == low:
        return hull[low]
    # Find mid index
    mid = low + ((high - low) // 2)
    # Check if mid is local max
    if is_local_max(hull, llast_pt, last_pt, mid):
        return hull[mid]
    # Decide whether we need to go to the left half or the right half
    l_max = max(hull[low], hull[mid-1])
    smart_angle_set(hull[high], llast_pt, last_pt)
    r_max = max(hull[mid+1], hull[high])
    if l_max > r_max:
        return bin_roated(hull, low, mid - 1, llast_pt, last_pt) # Left
    else:
        return bin_roated(hull, mid + 1, high, llast_pt, last_pt) # Right

# Find the tangency point with binary search in O(log m) to each group CH
# Set the angle of this point, as we will compare
def bin_search_hull(hull, llast_pt, last_pt):
    n = len(hull)
    return bin_roated(hull, 0, n-1, llast_pt, last_pt)
    ''' # Testing code to verify angle is correct 
    bin_p = bin_roated(hull, 0, n-1, llast_pt, last_pt)
    lin_p = find_tan(hull, llast_pt, last_pt)
    if bin_p != lin_p:
        print("PANIC")
    return bin_p
    # Testing code to try and optimize
    if 5 * math.log(n, 2) > n: # Will be more checks than linear method
        return find_tan(hull, llast_pt, last_pt)
    if is_local_max(hull, llast_pt, last_pt, 0):
        return hull[0]
    elif is_local_max(hull, llast_pt, last_pt, n-1):
        return hull[n-1]
    else:
        #bin_p = bin_find_max(hull, 0, n-1, llast_pt, last_pt)
        #angles.append(bin_p.angle)
        return bin_roated(hull, 0, n-1, llast_pt, last_pt)
    '''

def try_hull(points, m, pt, fast):
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
            plt.plot([c_hull[-1].x, new_pt.x], [c_hull[-1].y, new_pt.y], zorder=3, color="k")
            plt.draw()
            plt.pause(1)
        if new_pt == v_low:
            if fast:
                return [True, c_hull]
            return c_hull
        else:
            c_hull.append(new_pt)
    if fast:
        flat_list = partial_hulls[0]
        for i in range(1, len(partial_hulls)):
            flat_list += partial_hulls[i]
        return [False, flat_list]
    return None

def chan_hull(points):
    m = 4
    n = len(points)
    pt = None
    if do_graph:
        pt = get_coords(points)
    while True:
        res = try_hull(points, m, pt, False)
        if res is None:
            m = min(m**2, n)
        else:
            return res

# This is a slight modification of Chan's algorithm. After each try_hull, if we do not complete, then we will discard
# the points which were inside of the smaller convex hulls. We are able to do this as if a point is not a local extrema,
# it cannot be a global extrema.
def fast_chan_hull(points):
    m = 4
    pt = None
    if do_graph:
        pt = get_coords(points)
    while True:
        res = try_hull(points, m, pt, True)
        if res[0]:
            return res[1]
        else:
            points = res[1]
            n = len(points)
            m = min(m**2, n)

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
        print(str(points[i]) + ", ", end="")
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

def generate_random_points(num_points):
    high = num_points * 1000
    low = -high
    num_points *= 2
    points = np.random.randint(low, high, size=num_points)
    return Point.from_coordinates(points)

def plot_hull(hull, style = "dashed"):
    if len(hull) > 1: # Nothing to plot if its a single point
        hull_plot = hull.copy()
        hull_plot.append(hull[0]) # Add first to end to get full lines
        hl = get_coords(hull_plot)
        plt.plot(hl[0], hl[1], zorder=2, linestyle=style)
        plt.draw()
        plt.pause(1)

do_graph = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Show a graphic display of Chan\'s convex hull algorithm')
    parser.add_argument('-f', '--fast', action='store_true', help="use fast_chan_hull() instead of chan_hull()")
    parser.add_argument('-p', '--points', help="number of points to use, default: 100", type=int, default=100)
    parser.add_argument('-i', '--input', help="input file of points to use instead of randomly generated points")
    args = parser.parse_args()
    do_fast = args.fast
    num_points = args.points
    in_file = args.input
    # Get or generate points
    if in_file is not None:
        try:
            points = get_points(in_file)
            if len(points) <= 3:
                print("Need more than 3 points")
                exit(1)
        except:
            print("Error opening or parsing file")
            exit(1)
    else:
        points = generate_random_points(num_points)
    # Show graph
    do_graph = True
    if do_fast:
        chans_hull = fast_chan_hull(points)
    else:
        chans_hull = chan_hull(points)
    print_points(chans_hull)
    plt.clf() # Clear figure
    pt = get_coords(points)
    plt.scatter(pt[0], pt[1], zorder=1, color="k") # Add points
    plot_hull(chans_hull, "solid")
    plt.show()
