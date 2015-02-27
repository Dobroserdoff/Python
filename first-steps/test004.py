def myrange(xx, yy, zz):
    l = xx
    d = []
    if xx - yy == 0:
        print 'empty list'
    if xx > yy:
        if yy > 0:
            while l >= yy:
                d.append(l)
                l = l - abs(zz)
        if yy < 0:
            while l >= yy:
                d.append(l)
                l = l - abs(zz)
    if xx < yy:
        if yy > 0:
            while l <= yy:
                d.append(l)
                l = l + abs(zz)
        if yy < 0:
            while l <= yy:
                d.append(l)
                l = l + abs(zz)
    return d

print myrange(-30, -10, 2)
