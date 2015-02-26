
def myf(x):
    a = []
    b = 0
    while b <= x:
        if b % 2 != 0:
            if b % 3 != 0:
                a.append (b)
        b += 1
    return a
print myf(20)




a = True
b = True

if a and b:
    print "a and b"

if a:
    if b:
        print "a and b"

if a or b:
    print "a or b"

if a:
    print "a or b"
elif b:
    print "a or b"