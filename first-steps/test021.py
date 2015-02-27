
def main():
    input_file = open ('output2.txt')
    out = open ('output3.txt', 'wt')
    a = []
    space = ' '
    word_lenght = 0
    for line in input_file:
        if line != '\n':
            a = line.split(' ')
            a = a[:-1]
            for k in range(len(a)):
                word_lenght += len(a[k]) + 1
            free_space = 120 - word_lenght
            x = free_space/len(a) + 1
            if x >= 1:
                z = free_space - x * len(a)
                for y in range(len(a)):
                    if z > 0:
                        out.write(space)
                        z = z - 1
                    out.write(x * space)
                    out.write(a[y])
            else:
                for yy in range(free_space):
                    out.write(space)
                    out.write(a[yy])
            out.write('\n\n')
            word_lenght = 0

    out.close()

main()

