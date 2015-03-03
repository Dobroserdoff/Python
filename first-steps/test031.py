class MyException(Exception):
    def __init__(self):
        Exception.__init__(self, 'IndexError')

def b():
    raise Exception()
    return 1

def a():
    try:
        return b() + 1
    except MyException as e:
        print e
        return 4

print a()