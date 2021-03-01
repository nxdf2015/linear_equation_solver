
from linear_system import Row, LinearSystem
from utilities import parse_arg

(infile,outfile ) = parse_arg()

linear = LinearSystem.from_file(infile)


if linear.solve():
    linear.get_result()
linear.save_result()

