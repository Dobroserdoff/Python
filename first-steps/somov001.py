class RangeIter(object):
    def __init__(self, count):
        self.count = count
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        result = self.index
        if result >= self.count:
            raise StopIteration()
        self.index += 1
        return result


class LettersIter(object):
    def __init__(self):
        self.letter = 'A'

    def __iter__(self):
        return self

    def __str__(self):
        return '!!Iterator!!'

    def next(self):
        r = self.letter
        self.letter = chr(ord(self.letter) + 1)
        if r == chr(ord('Z') + 1):
            raise StopIteration()
        return r


class Number(object):
    def __init__(self, n):
        self.n = n

    def __cmp__(self, other):
        if self.n < other.n:
            return -1
        if self.n > other.n:
            return 1
        return 0


class MyException(Exception):
    def __init__(self):
        Exception.__init__(self, "It's mine")

    def __str__(self):
        return 'Not my exception: ' + self.message


try:
    print '1'
    if True:
        raise MyException()
    print '2'
except Exception as e:
    print e


class InfiniteContainer(object):
    def __getitem__(self, item):
        if type(item) is int:
            return item + 13

        if len(item) > 3:
            raise IndexError('WTF? Is that an index? Really???')
        return item + "10"


ic = InfiniteContainer()

print ic[70000]

print ic['abc']
try:
    print ic['abcd']
except IndexError as e:
    print 'Caught ' + str(e)

n1 = Number(6)
n2 = Number(5)

#print id(n1)
#print id(n2)

# >              1
# <             -1
# >=             1 0
# <=            -1 0
# ==               0


if n1 >= n2:  # n1.__cmp__(n2) in [0, 1]
    print '6 > 5'

for element in RangeIter(10):
    print element

letters_iter = LettersIter()
print letters_iter
print str(letters_iter)
print "It's my iter: %s. Isn't it fun?" % letters_iter

letters_list = list(letters_iter)
print letters_list

a = "abrvalg"
b = list(a)
print b

f = open('../addrbook/Book.txt')
print type(f)

fileiter = f.__iter__()
print fileiter.next()

l = list(f)
print l

a = [1, 2, 3]
print type(a)

aiter = a.__iter__()
print aiter.next()

aiter2 = a.__iter__()
print aiter2.next()

for x in a:
    print x

b = list(a)
print b