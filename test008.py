def myrange(x, y, z):
    r = []
    while (z > 0 and x < y) or (z < 0 and x > y):
        r.append(x)
        x += z
    return r

print myrange (10, 20, 2)