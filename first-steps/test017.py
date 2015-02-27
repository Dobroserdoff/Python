P = '---'
def fib (n, prefix = ''):
    print prefix
   # print '%sn = %s' % (prefix, n)
    if n < 3:
        fb = n
    else:
        fb = fib (n-1, prefix + P) + fib (n-2, prefix + P) + fib (n-3, prefix + P)
    #print '%sn = %s, fb = %s' % (prefix, n, fb)
    return fb
print fib (10)