def find_first(x, a, f):
    return next((i for i in a if f(i) == x), None)
