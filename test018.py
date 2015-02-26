SUM = 1
MULT = 2
SUB = 3
DIV = 4
POW = 5
UPCHK = 6
OPNAMES = {SUM: 'addition', MULT: 'multiplication', SUB: 'subtraction', DIV: 'division', POW: 'power', UPCHK: 'upyachka'}


def math(a, b, op):
    if op == SUM:
        return a + b
    elif op == MULT:
        return a * b
    elif op == SUB:
        return a - b
    elif op == DIV:
        return a / b
    elif op == POW:
        return a ** b
    elif op == UPCHK:
        if a % 2 == 0 and b % 2 == 0:
            return a + b
        else:
            return a * b
    else:
        print 'Oooops!'


def make_row(k, n, z):
    row = []
    for i in range(1, n + 1):
        row.append(math(i, k, z))
    return row


def make_table(n, z):
    table = []
    for i in range(1, n + 1):
        row = make_row(i, n, z)
        table.append(row)
    return table


def main():
    ops = OPNAMES.keys ()
    x = 0
    while x < len (ops):
        table = make_table(10, ops[x])
        print "Here's our %s table" % OPNAMES[ops[x]]
        print table
        x += 1

main()