import sys
# -*- coding: UTF-8 -*-


def write_list(dec_list, file_name):
    out = open(file_name, 'wt')
    for a in dec_list:
        b = []
        c = []
        x = bin(a)[2:]
        while len(x) < 32:
            x = '0' + x
        second_minor = x[24:32]
        first_minor = x[16:24]
        first_major = x[0:8]
        second_major = x[8:16]
        b.append(chr(int(first_major, 2)))
        b.append(chr(int(second_major, 2)))
        b.append(chr(int(first_minor, 2)))
        b.append(chr(int(second_minor, 2)))
        for i in b:
            out.write(i)
        b = []
    out.close()


def decode_number(a):
    res = 0
    for i in range(len(a)):
        res = res * 256 + a[i]
    #return a[3] + (a[2] + (a[1] + a[0] * 256) * 256) * 256
    return res

def read_list(file_name):
    a = []
    y = 0
    decim = []
    input_file = open(file_name)
    full_string = input_file.read()
    for i in range(len(full_string)):
        #print hex(ord(full_string[i]))[2:]
        a.append(ord(full_string[i]))
        if i == 3 + 4 * y and i != 0:
            decim.append(decode_number(a))
            a = []
            y += 1
    print decim
    return decim


def main():
    decim_list = [1, 2, 3, 4, 5, 15, 255, 256, 65000, 150000, 1000000000]
    print decim_list
    write_list(decim_list, 'outputfourlist.txt')
    decim_list2 = read_list('outputfourlist.txt')
    if decim_list2 != decim_list:
        print '!!11!!1 адин Адин!!11 Упячка!!11'
    else:
        print 'Малаца!'


main()
#read_list('outputfourlist.txt')
#write_list([1, 2, 3, 4, 5, 15, 255, 256, 65000, 150000], 'outputfourlist.txt')