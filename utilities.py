import argparse

def parse_line(line):
    try:
        return list(map(float,line.split(" ")))
    except ValueError as e:
        return list(map(complex,line.split(" ")))



def get_data(filename="in.txt"):
    with open(filename,"r") as f:
        n,m = list(map(int,f.readline().split(" ")))
        return [parse_line(f.readline()) for _ in range(m)]


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", default="in.txt")
    parser.add_argument("--outfile",default="out.txt")
    arg = parser.parse_args()
    return (arg.infile, arg.outfile)
