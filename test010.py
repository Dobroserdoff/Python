def add(x, y):
    return x * y
seq = range(8)
seq2 = range(2, 10)
print reduce(add, seq, 0)