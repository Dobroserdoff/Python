import sys


def join_hyphenation(h):
    hyphenation = []
    for index in range(len(h)):
        word = h[index]
        if word.endswith('-') and index != len(h) - 1:
            word = word[:-1] + h[index + 1]
            h[index + 1] = ''
        hyphenation.append(word)
    return hyphenation


def remove_empty(j):
    clean = []
    for s in j:
        if s != '' and s != ' ':
            clean.append(s)
    return clean


def string_break(paragraph):
    a = []
    l = 0
    for k in range(len(paragraph)):
        word = paragraph[k]
        new_l = l + len(word)
        if new_l >= 120:
            a.append('\n')
            l = 0
        a.append(word)
        l += len(word) + 1
    a.append('\n')
    return a


def print_paragraph(paragraph, out):
    string = []
    space = ' '
    word_length = 0
    for n in range(len(paragraph)):
        word = paragraph[n]
        if word != '\n':
            word_length += len(word) + 1
            string.append(word)
        else:
            if len(string) == 1:
                free_space = 121 - word_length
                out.write(free_space * space)
                out.write(string[0])
            else:
                if string == paragraph[-len(string)-1: -1]:
                    for i in range(len(string)):
                        out.write(string[i])
                        out.write(space)
                else:
                    free_space = 121 - word_length
                    x = free_space/(len(string) - 1)
                    z = free_space - x * (len(string) - 1)
                    for y in range(len(string)):
                        if y == 0:
                            out.write(string[y])
                            out.write(space)
                        else:
                            if z > 0:
                                out.write(x * space)
                                out.write(space)
                                out.write(string[y])
                                out.write(space)
                                z -= 1
                            else:
                                if y == len(string) - 1:
                                    out.write(x * space)
                                    out.write(string[y])
                                else:
                                    out.write(x * space)
                                    out.write(string[y])
                                    out.write(space)
            out.write('\n')
            word_length = 0
            string = []
    out.write('\n')


def general_main():
    input_file = open('/Users/yuryivanov/downloads/rfc822.txt')
    out = open('output2.txt', 'wt')
    a = []
    b = []
    for line in input_file:
        a.append(line.strip('\n\t\f '))
    for word in a:
        b.append(word.split(' '))
    current_paragraph = []
    for i in range(len(b)):
        current_line = b[i]
        if current_line == ['']:
            if current_paragraph != []:
                current_paragraph = join_hyphenation(current_paragraph)
                current_paragraph = remove_empty(current_paragraph)
                paragraph = string_break(current_paragraph)
                print_paragraph(paragraph, out)
                current_paragraph = []
        else:
            current_paragraph += current_line
    out.close()


def general_test():
    paragraph = ['one', 'thr-','ee', 'four','thr-']
    for a in paragraph:
        print a, id(a)
    print id(paragraph)
    paragraph = join_hyphenation(paragraph)
    print id(paragraph)
    print paragraph



#general_test ()
general_main()







