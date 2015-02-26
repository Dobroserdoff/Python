
PREFIX = '      '


def calc(a, b, prefix=''):
    print '%sa = %s, b = %s' % (prefix, a, b)

    if a > 1:
        result = 1 + calc(a - 1, b, prefix + PREFIX)
    elif b > 1:
        x = calc(a, b - 1, prefix + PREFIX)
        result = 1 + x
    else:
        print '%ssimply sum' % prefix
        result = a + b

    print '%sa = %s, b = %s, result = %s' % (prefix, a, b, result)

    return result



def main():
   print "calc -> %s" % calc(4, 3)

main()