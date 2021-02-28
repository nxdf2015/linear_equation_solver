
from utilities import get_data

class Row:
    def __init__(self,data=[]):
        self.values = data

    def __iadd__(self, other):
        data = [ x + y for x,y in zip(self.values , other.values)]
        return Row(data)

    def __mul__(self, other):
        if type(other) == float:
            data = [ v * other for v in self.values]

            return Row(data)

    def __getitem__(self, key):
        return self.values[key]

    def __str__(self):
        return " ".join(list(map(str, self.values)))





class LinearSystem:
    """
    load a linear system  and solve the system

    """
    def __init__(self,rows=[]):
        self.rows = [ Row(row) for row in rows]
        self.size = len(rows)
        self.result = [0] * self.size

    @staticmethod
    def from_file(file_name="in.txt"):

        rows = get_data(file_name)
        return LinearSystem(rows)



    def solve(self):

        for row_id in range(self.size):
           c =  self.rows[row_id][row_id]
           self.rows[row_id] = self.rows[row_id] * (1/c)
           print(f"r{row_id} = r{row_id} * { 1 / c  }")
           print(self)
           print()
           for j in range(row_id + 1,self.size):
            d = self.rows[j][row_id]
            print(f"r{j} = r{j} + { - 1 * d } * r{ row_id}")
            self.rows[j] += (self.rows[row_id] * (-1. * d ))
           print(self)


        result = [0] * self.size
        for id_row in range(self.size - 1, -1,-1):

                value = self.rows[id_row][-1]
                for x,v in zip(result, self.rows[id_row][:-1]):
                    value -= x * v
                result[id_row] = value / self.rows[id_row][id_row]
        self.result = result
        print(f"the solution is {self.result}")


    def save_result(self,namefile="out.txt"):
        with open(namefile,"w") as f:
            [ f.write(f"{value}\n") for value in self.result]



    def __str__(self):
        return "\n".join((list(map(str,self.rows))))


