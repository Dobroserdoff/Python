def even(a):
    for a in range (2, a):
        if a % 2 == 0:
            print a, 'even'
            continue
        else:
            print a, 'not even close'
print even 50