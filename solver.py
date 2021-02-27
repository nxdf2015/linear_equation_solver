 



def parse_arg():
    return  list(map(float,input().split(" ")))

def solve(a,b):
    return b / a


print(solve(* parse_arg()))
