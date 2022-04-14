import matplotlib.pyplot as plt
import argparse
import csv
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a graph comparison of different algorithms')
    parser.add_argument('-i', '--input', dest="filename", required=True, help="input file to graph")
    args = parser.parse_args()
    in_file = args.filename
    try:
        with open(in_file, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            x, y1, y2 = [], [], []
            for row in reader:
                x.append(int(row[headers[0]]))
                y1.append(float(row[headers[1]]))
                y2.append(float(row[headers[2]]))
        plt.plot(x, y1, label=headers[1])
        plt.plot(x, y2, label=headers[2])
        title = (in_file.split(".", 1)[0]).title()
        plt.legend()
        plt.title(title)
        #plt.locator_params(axis='y', nbins=10)
        #plt.locator_params(axis='x', nbins=10)
        plt.xlabel("Number of points")
        plt.ylabel("Time (seconds)")
        plt.savefig(os.path.join(os.curdir, title.lower() + ".pdf"), transparent=True)
    except:
        print("Error opening or parsing file")
        exit(1)
