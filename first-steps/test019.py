def main():
    input_file = open('input.txt')
    a = []
    for line in input_file:
        if line[-1] == '\n':
            line = line[:-1]
            line = line.split(' ')
            a.extend(line)
    a = filter(lambda s: len(s) > 0, a)
    a.sort()

    out = open('output.txt', 'wt')

    y = 1
    i = 1
    b = []
    c = []
    for x in a:
        if y < len(a):
            z = a[y]
            if x[0] == z[0]:
                out.write(x)
                out.write('\n')
                i += 1
            else:
                out.write(x)
                out.write('\n')
                out.write('\n')
                b.append(i)
                c.append(x[0])
                i = 1
        else:
            out.write(x)
            b.append(i)
            c.append(x[0])
        y += 1

    x = 0
    while x < len(c):
        print c[x], b[x], b[x] * 100/len(a)
        x += 1

    out.close()


main()