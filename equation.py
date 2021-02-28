

def get_row():
    return list(map(float, input().split(" ")))

def multiply(row , coeff):
    return list(map(lambda x : coeff * x , row))

def substract(row,row1):
    return list(map(lambda t: t[0] - t[1], list(zip(row,row1))))

rows = [get_row(), get_row()]

coeff = rows [1][0] / rows[0][0]


rows[1] = substract(rows[1] , multiply(rows[0], coeff))

x = rows[1][2] / rows[1][1]

y = (rows[0][2] - rows[0][1] * x )/ rows[0][0]

print(y,x)
