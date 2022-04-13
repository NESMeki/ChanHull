import math
import random
import time
from hull import *

chan_str = "Chan"
graham_str = "Graham"

def time_hulls(points, do_fast):
    for point in points: # Remove the angles on the points
        point.clear_angle()
    n = len(points)
    start = time.time()
    if do_fast:
        c_hull = fast_chan_hull(points)
    else:
        c_hull = chan_hull(points)
    c_fin = time.time() - start
    for point in points: # Remove the angles on the points
        point.clear_angle()
    start = time.time()
    g_hull = graham_scan(points)
    g_fin = time.time() - start
    winner = chan_str if c_fin < g_fin else graham_str
    print(str(n) + ", " + str(g_fin) + ", " + str(c_fin) + ", " + winner)

def time_chan(points):
    for point in points: # Remove the angles on the points
        point.clear_angle()
    n = len(points)
    start = time.time()
    c_hull = chan_hull(points)
    c_fin = time.time() - start
    for point in points: # Remove the angles on the points
        point.clear_angle()
    start = time.time()
    f_hull = fast_chan_hull(points)
    f_fin = time.time() - start
    winner = "Normal" if c_fin < f_fin else "Fast"
    print(str(n) + ", " + str(f_fin) + ", " + str(c_fin) + ", " + winner)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Chan\'s convex hull algorithm against Graham\'s')
    parser.add_argument('-f', '--fast', action='store_true', help="use fast_chan_hull() instead of chan_hull()")
    parser.add_argument('-c', '--compare', action='store_true', help="compare fast_chan_hull() to chan_hull() instead of comparing to Grahams")
    parser.add_argument('-p', '--points', help="minimum number of points to use, default: 10000", type=int, default=10000)
    parser.add_argument('-n', '--number', help="number of hulls to compute, default: 100", type=int, default=100)
    parser.add_argument('-s', '--same', action='store_true', help="use the same number of points for each hull, default: False")
    args = parser.parse_args()
    do_fast = args.fast
    compare_chan = args.compare
    num_point_low = args.points
    num_iterations = args.number
    same_num = args.same
    if compare_chan:
        print("Number points, Fast Chan time, Normal Chan time, Faster alg")
    else:
        print("Number points, Graham time, Chan time, Faster alg")


    #Generate all points at once, then use a subset of points for each run
    points = generate_random_points(num_point_low * num_iterations)
    for i in range(1, num_iterations + 1):
        if same_num:
            points_i = points[num_point_low*(i-1):num_point_low*i]
        else:
            points_i = points[0:num_point_low*i]
        if compare_chan:
            time_chan(points_i)
        else:
            time_hulls(points_i, do_fast)
