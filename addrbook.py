#!/usr/bin/python
import sys
# -*- coding: UTF-8 -*-

def main():
    print_list = []
    output_list = read_name('book.txt')
    out = open('book.txt', 'wt')
    print sys.argv
    if sys.argv[1] == 'add':
        output_list.append(add_name(sys.argv[2:]))
    if sys.argv[1] == 'second_name':
        output_list = second_name(output_list, sys.argv[2:-1], sys.argv[-1])
    if sys.argv[1] == 'date':
        output_list = birthday(output_list, sys.argv[2:-1], sys.argv[-1])
    if sys.argv[1] == 'first_column':
        for a in output_list:
            print_list.append(list(a))
        print_list = first_column(print_list, sys.argv[2])
        for x in string_to_print(print_list):
                print x
        print_list = []
    if sys.argv[1] == 'del':
        output_list = del_name(output_list, sys.argv[2:])
    if sys.argv[1] == 'print':
        for a in output_list:
            print_list.append(list(a))
        if sys.argv[-1] == 'print':
            print_list.sort(key=lambda x: x[2])
            for x in string_to_print(print_list):
                print x
        else:
            input_list = print_search(print_list, sys.argv[2:])
            for x in string_to_print(input_list):
                print x
        print_list = []
    if sys.argv[1] == 'set_phone':
        output_list = set_phone(output_list, sys.argv[2:-1], sys.argv[-1])
    print output_list
    for i in output_list:
        if i != []:
            for j in i:
                out.write(j)
                out.write('$')
            out.write('\n')

def first_column(input_list, column):
    x = ''
    if column == 'name':
        input_list.sort(key=lambda x: x[0])
    elif column == 'second_name':
        input_list.sort(key=lambda x: x[1])
        for i in range(len(input_list)):
            x = input_list[i][1]
            input_list[i][1] = ''
            input_list[i].insert(0, x)
    elif column == 'surname':
        input_list.sort(key=lambda x: x[2])
        for i in range(len(input_list)):
            x = input_list[i][2]
            input_list[i][2] = ''
            input_list[i].insert(0, x)
    elif column == 'phone':
        input_list.sort(key=lambda x: x[3])
        for i in range(len(input_list)):
            x = input_list[i][3]
            input_list[i][3] = ''
            input_list[i].insert(0, x)
    elif column == 'date':
        input_list.sort(key=lambda x: x[4])
        for i in range(len(input_list)):
            x = input_list[i][4]
            input_list[i][4] = ''
            input_list[i].insert(0, x)
    return input_list

def string_to_print(input_list):
    output_list = []
    for x in input_list:
        string = ''
        for y in x:
            if y != '':
                string += y + ' '
        output_list.append(string[:-1])
    return output_list


def read_name(input):
    output_list = []
    name = []
    string = ''
    input_file = open(input)
    if input_file != '':
        for i in input_file:
            for j in i:
                if j != '$' and j != '\n':
                    string += j
                elif j == '$':
                    name.append((string))
                    string = ''
            output_list.append(name)
            name = []
    return output_list

def add_name(input):
    output_list = [input[0], '', input[1], '', '']
    return output_list

def set_phone(input_list, name, phone):
    bingo = match(input_list, name)
    if len(bingo) > 1:
        print 'Please specify a person to change phone number'
    else:
        if phone != '0':
            input_list[bingo[0]][3] = phone
        else:
            input_list[bingo[0]][3] = ''
    return input_list

def print_search(input_list, name):
    name_to_print = []
    for i in match(input_list, name):
        name_to_print.append(input_list[i])
    return name_to_print

def del_name(input_list, name):
    bingo = match(input_list, name)
    if len(bingo) > 1:
        print 'Please specify a person to delete'
    else:
        input_list[bingo[0]] = []
    return input_list

def birthday(input_list, name, date):
    bingo = match(input_list, name)
    if len(bingo) > 1:
        print 'Please specify a person to change date of birth'
    else:
        if date != '0':
            input_list[bingo[0]][4] = date
        else:
            input_list[bingo[0]][4] = ''
    return input_list

def second_name(input_list, name, sec_name):
    bingo = match(input_list, name)
    if len(bingo) > 1:
        print 'Please specify a person to change the second name'
    else:
        if sec_name != '0':
            input_list[bingo[0]][1] = sec_name
        else:
            input_list[bingo[0]][1] = ''
    return input_list

def match(input_list, name):
    b = []
    if len(name) > 1:
       for a in range(len(input_list)):
            if input_list[a][0] == name[0] and input_list[a][2] == name[1]:
                b.append(a)
    else:
        for a in range(len(input_list)):
            for j in input_list[a]:
                if j == name[0]:
                    b.append(a)
    return b

#first_column([['Tom', 'Slayer', 'Araya', '666', '24.53.2564'], ['Tom', 'RATM', 'Morello', '12', '12.12.1912'], ['Chino', 'Deftones', 'Moreno', '94', '95.05.1031'], ['Trent', 'NIN', 'Reznor', '54', '32.32.1932'], ['Aaron', 'ISIS', 'Turner', '32', '24.24.9243']], 'second_name')
#add_name('Tom')
#read_name('book.txt')
#string_to_print([['Tom', 'Slayer', 'Araya', '13', '54.24.2942'], ['Tom', 'RATM', 'Morello', '34', '13.13.1913'], ['Chino', 'Deftones', 'Moreno', '92', '24.53.2435'], ['Trent', 'NIN', 'Reznor', '54', '43.53.6523']])
main()