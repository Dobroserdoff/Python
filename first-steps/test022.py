import sys
# -*- coding: UTF-8 -*-

input_file = open('input.txt')
out = open('outputascii.txt', 'wt')
for line in input_file:
    for letter in line:
        a = ord(letter)
        out.write(chr(a))
out.close()

input_file = open('input.txt')
out = open('outputcp1251.txt', 'wt')
for line in input_file:
    for i in range(len(line)):
        letter = line[i]
        a = bin(ord(letter))
        a = a[2:]
        while len(a) < 8:
            a = '0' + a
        if a[:3] == '110':
            next = bin(ord(line[i + 1]))
            b = a[3:] + next[4:]
            c = int(b, 2)
            if c > 1040 and c < 1119:
                c = c - 848
                out.write(chr(c))
        if a[:1] == '0':
            b = int(a[1:], 2)
            out.write(chr(b))
out.close()

input_file = open('input.txt')
out = open('outputucsii.txt', 'wt')
b = []
for line in input_file:
    for i in range(len(line)):
        letter = line[i]
        a = bin(ord(letter))
        a = a[2:]
        while len(a) < 8:
            a = '0' + a
        if a[:1] == '0':
            b.append('00000000')
            b.append(a)
        if a[:3] == '110':
            next = bin(ord(line[i + 1]))
            a = a[3:] + next[4:]
            while len(a) < 16:
                a = '0' + a
            b.append(a[:8])
            b.append(a[8:])
    for x in b:
        out.write(chr(int(x, 2)))
    b = []
out.close()
