def search(a, b):
    x = 0
    y = []
    while x < len(a):
        if a[x] == b:
            y.append(x)
        x += 1
    return y





def search2(a, b, prefix = ''):
    print '%sa = %s, b = %s' % (prefix, a, b)
    if len(a) > 1:
        x = len(a) / 2
        y = []
        y.extend(search2(a[:x], b, prefix + '    '))
        for z in search2(a[x:], b, prefix + '    '):
            y.append (z + x)
        result = y
    else:
        if len(a) != 0 and a[0] == b:
            result = [0]
        else:
            result = []
    print '%sa = %s, b = %s, result = %s' % (prefix, a, b, result)
    return result
print search2 ([1, 3, 7, 9, 3, 5, 7, 3, 9, 3], 3)