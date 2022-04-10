# ChanHull
A python implementation of Chan's Convex Hull Algorithm

```
usage: hull.py [-h] [-f]

Show a graphic display of Chan's convex hull algorithm.

optional arguments:
  -h, --help  show help message and exit
  -f, --fast  use fast_chan_hull() instead of chan_hull()
 ```

```
usage: stats.py [-h] [-f] [-p POINTS] [-n NUMBER] [-s]

Test Chan's convex hull algorithm against Graham's.

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            use fast_chan_hull() instead of chan_hull().
  -p POINTS, --points POINTS
                        minimum number of points to use
  -n NUMBER, --number NUMBER
                        number of hulls to compute
  -s, --same            use same number of points for each hull
```
