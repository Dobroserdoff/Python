import sys
# -*- coding: UTF-8 -*-

def main(dec_list):
    out = open('outputlist.txt', 'wt')
    b = ''
    for a in dec_list:
        b = bin(a)[2:]
        while len(b) < 16:
            b = '0' + b
        out.write(b)
    out.close()


def opposite(bin_list):
    out = open('outputopposite.txt', 'wt')
    for a in bin_list:
        a = int(str(a), 2)
        b = str(a)
        while len(b) < 16:
            b = '0' + b
        out.write(b)
    out.close()



main([1, 2, 3, 4, 5, 65000])
opposite ([1, 10, 11, 100, 101, 1111110111101000])
