import sys
# -*- coding: UTF-8 -*-

def straight_optimization(a):
    a = str(bin(a)[2:])
    if len(a) < 32 and len(a) > 24:
        while len(a) < 32:
            a = '0' + a
    if len(a) < 24 and len(a) > 16:
        while len(a) < 24:
            a = '0' + a
    if len(a) < 16 and len(a) > 8:
        while len(a) < 16:
            a = '0' + a
    if len(a) < 8:
        while len(a) < 8:
            a = '0' + a
    return(a)

def opposite_optimization(a):
    a = int(str(a), 2)
    a = str(a)
    if len(a) < 32 and len(a) > 24:
        while len(a) < 32:
            a = '0' + a
    if len(a) < 24 and len(a) > 16:
        while len(a) < 24:
            a = '0' + a
    if len(a) < 16 and len(a) > 8:
        while len(a) < 16:
            a = '0' + a
    if len(a) < 8:
        while len(a) < 8:
            a = '0' + a
    return(a)

def main(dec_list):
    out = open('outputfourlist.txt', 'wt')
    for a in dec_list:
        b = straight_optimization(a)
        out.write(b)
    out.close()


def opposite(bin_list):
    out = open('outputfouropposite.txt', 'wt')
    for a in bin_list:
        b = opposite_optimization(a)
        out.write(b)
    out.close()

main([1, 3, 5, 7, 3194967295])
opposite ([1, 11, 101, 111, 10111110011011110101010011111111])