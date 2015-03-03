class Container(object):
    def __init__(self, my_list):
        self.list = my_list

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        b = Iterator(self)
        return b


class Iterator(object):
    def __init__(self, c):
        self.cont = c
        self.number = 0

    def next(self):
        current_number = self.number
        self.number += 1
        if current_number == len(self.cont):
            raise StopIteration()
        return self.cont.list[current_number]


a = Container(['One', 'Two'])

for element in a:
    print element

print 'Hello'
iter = a.__iter__()
#print iter.next() # One
#print iter.next() # Two
#print iter.next()