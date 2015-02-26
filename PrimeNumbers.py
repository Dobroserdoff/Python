def prime(l):

    for n in range(2, l):
        for x in range(2, n):
            if n % x == 0:
                print n, 'is not a prime number'
                break
        else:
            print n, 'is a prime number'

print prime(100)