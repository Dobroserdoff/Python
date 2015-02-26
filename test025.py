import sys
# -*- coding: UTF-8 -*-

def write_byte(f, byte):
    f.write(chr(byte))

def read_byte(f):
    x = f.read(1)
    y = ord(x)

def main(dec_list):
    out = open('outputlist.txt', 'wt')
    for a in dec_list:
        b = []
        x = bin(a)[2:]
        while len(x) < 16:
            x = '0' + x
        minor = x[8:]
        major = x[:8]
        print int(major, 2)
        print int(minor, 2)
        b.append(chr(int(major, 2)))
        b.append(chr(int(minor, 2)))
        for x in b:
            out.write(x)
        b = []
    out.close()


main([1, 2, 3, 4, 5, 15, 255, 256, 65000])