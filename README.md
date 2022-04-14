# ChanHull
A python implementation of Chan's Convex Hull Algorithm

```
usage: hull.py [-h] [-f] [-p POINTS] [-i INPUT]

Show a graphic display of Chan's convex hull algorithm

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            use fast_chan_hull() instead of chan_hull()
  -p POINTS, --points POINTS
                        number of points to use, default: 100
  -i INPUT, --input INPUT
                        input file of points to use instead of randomly generated points
 ```

```
usage: stats.py [-h] [-f] [-c] [-p POINTS] [-n NUMBER] [-s] [-i INPUT]

Test Chan's convex hull algorithm against Graham's

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            use fast_chan_hull() instead of chan_hull()
  -c, --compare         compare fast_chan_hull() to chan_hull() instead of comparing to Grahams
  -p POINTS, --points POINTS
                        minimum number of points to use, default: 10000
  -n NUMBER, --number NUMBER
                        number of hulls to compute, default: 100
  -s, --same            use the same number of points for each hull, default: False
  -i INPUT, --input INPUT
                        input file of points to use instead of randomly generated points
```
```
usage: graph.py [-h] -i FILENAME

Create a graph comparison of convex hull different algorithms

optional arguments:
  -h, --help            show this help message and exit
  -i FILENAME, --input FILENAME
                        input csv file to graph
 ```
