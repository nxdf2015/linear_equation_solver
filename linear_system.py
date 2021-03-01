from utilities import get_data
from operator import not_


class Row:
    def __init__(self, data=[]):
        self.values = data

    def __iadd__(self, other):
        data = [x + y for x, y in zip(self.values, other.values)]
        return Row(data)

    def __mul__(self, other):
        if type(other) == float:
            data = [v * other for v in self.values]

            return Row(data)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __str__(self):
        return " ".join(list(map(str, self.values)))

    def all_zero(self, begin=0):
        return all(map(not_, self.values[begin:]))

    def no_solution(self):
        return all(map(not_, self.values[:-1])) and self.values[-1]

    def find_not_zero(self, begin):
        print(begin, self.values, [i for i, x in enumerate(self.values[begin:-1], begin) if x])
        return [i for i, x in enumerate(self.values[begin:-1], begin) if x][0]


class NoSolution(Exception):
    pass


class LinearSystem:
    """
    load a linear system  and solve the system

    """

    def __init__(self, rows=[]):
        self.rows = [Row(row) for row in rows]
        self.size = len(rows)
        self.cols = len(rows[0]) - 1
        self.result = [0] * self.size
        self.swaps = []

    @staticmethod
    def from_file(file_name="in.txt"):
        rows = get_data(file_name)
        return LinearSystem(rows)

    def get_column(self, id):
        return [self.rows[i][id] for i in range(self.size)]

    def is_zero_column(self, id):
        return all(map(not_, self.get_column(id)[id:]))

    def find_pivot(self, row_id):
        id = row_id
        while id < self.size:
            if id < self.cols and not self.is_zero_column(id):
                find_id = [i for i, x in enumerate(self.get_column(row_id)[row_id:], row_id) if x][0]
                self.swap_row(row_id, find_id)
                print(f"R{row_id} <-> R{find_id}")
                return True
            elif self.rows[id].all_zero(id):
                id += 1
            elif self.rows[id].no_solution():
                raise NoSolution()
            else:
                find_id = self.rows[id].find_not_zero(min(id, self.cols))
                self.swap_col(row_id, find_id)
                self.swap_row(row_id, id)
                print(f"R{row_id} <-> R{id}")
                return True

        return False

    def solve(self):
        print(self)
        print("Start solving the equation.")
        print("Rows manipulation:")
        for row_id in range(self.size):

            try:
                col_id = min(self.cols, row_id)
                if not self.find_pivot(row_id):
                    continue
            except NoSolution as e:
                self.result = ["No solutions"]
                return False

            c = self.rows[row_id][col_id]
            if not c == 1:
                self.rows[row_id] = self.rows[row_id] * (1 / c)
                print(f"R{row_id} * {1 / c} -> R{row_id}")

            for j in range(row_id + 1, self.size):
                d = self.rows[j][col_id]
                print(f"{- 1 * d} * R{row_id} -> R{j}")
                self.rows[j] += (self.rows[row_id] * (-1. * d))

        return True

    def reorder_value(self):
        for i, j in self.swaps:
            self.result[i], self.result[j] = self.result[j], self.result[i]

    def compute_result(self):
        result = [0] * (self.cols)
        for id_row in range(self.size - 1, -1, -1):

            value = self.rows[id_row][-1]
            for x, v in zip(result, self.rows[id_row][:-1]):
                value -= x * v

            result[id_row] = value / self.rows[id_row][id_row]
        self.result = result
        self.reorder_value()
        print(*self.result, sep=" ")

    def get_result(self):
        self.rows = [row for row in self.rows if not row.all_zero()]
        self.size = len(self.rows)

        if len(self.rows) < self.cols:
            self.result = ["Infinitely many solutions"]

        if len(self.result) == 1:
            print(self.result[0])
        else:
            self.compute_result()

    def save_result(self, namefile="out.txt"):
        print(f"save to {namefile}")
        with open(namefile, "w") as f:
            [f.write(f"{value}\n") for value in self.result]

    def __str__(self):
        return "\n".join((list(map(str, self.rows))))

    def swap_row(self, row_id, find_id):
        temp = self.rows[row_id]
        self.rows[row_id] = self.rows[find_id]
        self.rows[find_id] = temp

    def swap_col(self, col_id, find_id):
        for row in range(self.size):
            temp = self.rows[row][col_id]
            self.rows[row][col_id] = self.rows[row][find_id]
            self.rows[row][find_id] = temp
        self.swaps.append((col_id, find_id))
