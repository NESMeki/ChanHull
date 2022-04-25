import time
from hull import *

def time_hulls(points, do_modified):
    for point in points: # Remove the angles on the points
        point.clear_angle()
    n = len(points)
    start = time.time()
    if do_modified:
        c_hull = modified_chan_hull(points)
    else:
        c_hull = chan_hull(points)
    c_fin = time.time() - start
    for point in points: # Remove the angles on the points
        point.clear_angle()
    start = time.time()
    g_hull = graham_scan(points)
    g_fin = time.time() - start
    #Reverse list, they are in opposite order
    g_hull.reverse()
    p1 = g_hull.pop()
    g_hull = [p1] + g_hull
    #Verify hulls are the same
    if len(g_hull) != len(c_hull):
        print("Lengths are different")
        print_points(g_hull)
        print_points(c_hull)
        print(len(g_hull), len(c_hull))
    else:
        for p in range(len(g_hull)):
            if g_hull[p] != c_hull[p]:
                print("Point difference at index: " + str(p))
                print_points(g_hull)
                print_points(c_hull)
                print()
                print(g_hull[p])
                print(c_hull[p])
                exit(1)
    winner = "Chan" if c_fin < g_fin else "Graham"
    return str(n) + ", " + str(g_fin) + ", " + str(c_fin) + ", " + winner

def time_chan(points):
    for point in points: # Remove the angles on the points
        point.clear_angle()
    n = len(points)
    start = time.time()
    m_hull = modified_chan_hull(points)
    m_fin = time.time() - start
    for point in points: # Remove the angles on the points
        point.clear_angle()
    start = time.time()
    c_hull = chan_hull(points)
    c_fin = time.time() - start
    #Verify hulls are the same
    if len(m_hull) != len(c_hull):
        print("Lengths are different")
        print_points(m_hull)
        print_points(c_hull)
        print(len(m_hull), len(c_hull))
    else:
        for p in range(len(m_hull)):
            if m_hull[p] != c_hull[p]:
                print("Point difference at index: " + str(p))
                print_points(m_hull)
                print_points(c_hull)
                print()
                print(m_hull[p])
                print(c_hull[p])
                exit(1)
    winner = "Normal" if c_fin < m_fin else "Modified"
    return str(n) + ", " + str(m_fin) + ", " + str(c_fin) + ", " + winner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Chan\'s convex hull algorithm against Graham\'s')
    parser.add_argument('-m', '--modified', action='store_true', help="use modified_chan_hull() instead of chan_hull()")
    parser.add_argument('-c', '--compare', action='store_true', help="compare modified_chan_hull() to chan_hull() instead of comparing to Grahams")
    parser.add_argument('-p', '--points', help="minimum number of points to use, default: 10000", type=int, default=10000)
    parser.add_argument('-n', '--number', help="number of hulls to compute, default: 100", type=int, default=100)
    parser.add_argument('-s', '--same', action='store_true', help="use the same number of points for each hull, default: False")
    parser.add_argument('-i', '--input', help="input file of points to use instead of randomly generated points")
    parser.add_argument('-o', '--output', help="output file of comparison, default: out.csv")
    args = parser.parse_args()
    do_modified = args.modified
    compare_chan = args.compare
    num_point_low = args.points
    num_iterations = args.number
    same_num = args.same
    in_file = args.input
    out_file = args.output

    #Open file if possible
    if in_file is not None:
        try:
            points = get_points(in_file)
            if len(points) <= 3:
                print("Need more than 3 points")
                exit(1)
            num_point_low = len(points)
            num_iterations = 1
        except:
            print("Error opening or parsing file")
            exit(1)
    else:
        #Generate all points at once, then use a subset of points for each run
        points = generate_random_points(num_point_low * num_iterations)

    #Make output file
    if out_file is not None:
        out_file = open(out_file, 'w')
    else:
        out_file = open("out.csv", 'w')

    if compare_chan:
        res = "Number points, Modified Chan time, Normal Chan time, Faster alg"
    else:
        res = "Number points, Graham time, Chan time, Faster alg"
    print(res)
    out_file.write(res + "\n")

    for i in range(1, num_iterations + 1):
        if same_num:
            points_i = points[num_point_low*(i-1):num_point_low*i]
        else:
            points_i = points[0:num_point_low*i]
        if compare_chan:
            res = time_chan(points_i)
        else:
            res = time_hulls(points_i, do_modified)
        print(res)
        out_file.write(res + "\n")
