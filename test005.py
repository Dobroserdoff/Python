def myrange(xx, yy, zz):
    l = xx
    d = []
    if xx - yy == 0:
        print 'empty list'
    if zz == 0:
        print 'zero step'
    if xx > yy:
        if zz < 0:
            while l > yy:
                d.append(l)
                l = l + zz
        if zz > 0:
                d = []
    if xx < yy:
        if zz > 0:
            while l < yy:
                d.append(l)
                l = l + zz
        if zz < 0:
            d = []
    return d

print range (-20, 10, 2)
print myrange(-20, 10, 2)
