import socket
import sys
# -*- coding: UTF-8 -*-


def main(equation):
    #equation = str(raw_input('Please input an equation '))
    variables = var_count(equation)
    short = simplify(equation)
    str_var = ''
    result_html = []
    for i in variables:
        str_var += i + ' '
        result_html.append(i)
    result = str_var + equation + '\n'
    result_html.append(equation)
    result_html.append('$')
    all_values = values_change(variables)
    for values in all_values:
        simple = var_to_value(short, variables, values)
        final_value = brackets(simple)
        result += out_print(final_value, values)
        for i in out_print(final_value, values).split():
            result_html.append(i)
        result_html.append('$')
    create_html_file(result_html)
    print result


def html_request(equation):
    variables = var_count(equation)
    short = simplify(equation)
    result_html = []
    for i in variables:
        result_html.append(i)
    result_html.append(equation)
    result_html.append('$')
    all_values = values_change(variables)
    for values in all_values:
        simple = var_to_value(short, variables, values)
        final_value = brackets(simple)
        for i in out_print(final_value, values).split():
            result_html.append(i)
        result_html.append('$')
    return result_html


def simplify(equation):
    result = equation.replace('not', '!').replace(' and ', '&').replace(' or ', '|').replace(' then ', ':')\
        .replace(' equal ', '=').replace(' ', '')
    return result


def var_to_value(short, variables, values):
    result = ''
    for i in range(len(short)):
        if short[i] in variables:
            var_index = variables.index(short[i])
            result += values[var_index]
        else:
            result += short[i]
    return result


def create_html_file(inf=None):
    out = open('logicLinearOutput.html', 'w')
    result = create_html(inf)
    out.write(result)


def create_html(inf):
    output = '<!DOCTYPE html>' + '\n' + '<html>' + '\n' + '<head lang="en">' + '\n'
    output += '\t' + '<meta charset="UTF-8">' + '\n' + '\t' + '<title>Logix</title>' + '\n' + '</head>' + '\n'
    output += '<body>' + '\n' + '\t' + '<h1 align="center">Table Of Results</h1>' + '\n'
    output += '\t\t' + '<table width="500" cellspacing="5" cellpadding="15" border="3" align="center">' + '\n'
    output += '\t\t\t' + '<tr>' + '\n'
    for i in range(len(inf)):
        if inf[i] != '$':
            output += '\t\t\t\t' + '<td align="center">' + inf[i] + '</td>' + '\n'
        elif i+1 == len(inf):
            output += '\t\t\t' + '</tr>' + '\n'
        else:
            output += '\t\t\t' + '</tr>' + '\n' + '\t\t\t' + '<tr>' + '\n'
    output += '\t\t' + '</table>' + '\n' + '</body>' + '\n' + '</html>'
    return output


def values_change(variables):
    if len(variables) == 1:
        return [['0'], ['1']]
    else:
        result = []
        short_items = values_change(variables[:-1])
        for short_item in short_items:  # ['1', '0']
            long_item_1 = short_item + ['0']  # ['1', '0'] + ['0'] = ['1', '0', '0']
            long_item_2 = short_item + ['1']  # ['1', '0'] + ['1'] = ['1', '0', '1']
            result.append(long_item_1)
            result.append(long_item_2)
        return result


def out_print(final_value, values):
    str_out = ''
    for j in values:
        str_out += j + ' '
    result = str_out + final_value + '\n'
    return result


def var_count(equation):
    variables = []
    elements = equation.split()
    for i in elements:
        i = i.replace('(', '')
        i = i.replace(')', '')
        if len(i) == 1 and i not in variables:
            variables.append(i)
        elif len(i) == 2 and i[0] == '(' and i[1] not in variables:
            variables.append(i[1])
        elif len(i) == 2 and i[1] == ')'and i[0] not in variables:
            variables.append(i[0])
    return variables


def brackets(simple):
    limit_expression = lowest_brackets(simple, counter=0)
    limit = limit_expression[0]
    expression = limit_expression[1]
    while limit > 0:
        result = lowest_brackets(expression, 0)
        limit = result[0]
        expression = result[1]
    return expression


def lowest_brackets(simple, counter):
    pair_brackets = [0, 0]
    if '(' in simple:
        for i in range(len(simple)):
            if simple[i] == '(':
                pair_brackets[0] = i
                counter += 1
            elif simple[i] == ')':
                pair_brackets[1] = i
                final = lowest_brackets(simple[pair_brackets[0]+1:pair_brackets[1]], counter)
                new_eq = simple[:pair_brackets[0]] + final[1] + simple[pair_brackets[1]+1:]
                final[1] = new_eq
                return final
    else:
        result = [counter, all_operators(simple)]
        return result


def all_operators(simple):
    not_result = not_operator(simple)
    and_result = and_operator(not_result)
    or_result = or_operator(and_result)
    then_result = then_operator(or_result)
    final = equal_operator(then_result)
    return final


def not_operator(simple):
    if '!' in simple:
        result = simple.replace('!0', '1').replace('!1', '0')
    else:
        result = simple
    return result


def and_operator(not_result):
    if '&' in not_result:
        result = not_result.replace('1&1', '1').replace('1&0', '0').replace('0&1', '0').replace('0&0', '0')
    else:
        result = not_result
    return result


def or_operator(and_result):
    if '|' in and_result:
        result = and_result.replace('1|1', '1').replace('1|0', '1').replace('0|1', '1').replace('0|0', '0')
    else:
        result = and_result
    return result


def then_operator(or_result):
    if ':' in or_result:
        result = or_result.replace('1:1', '1').replace('1:0', '0').replace('0:1', '1').replace('0:0', '1')
    else:
        result = or_result
    return result


def equal_operator(then_result):
    if '=' in then_result:
        result = then_result.replace('1=1', '1').replace('1=0', '0').replace('0=1', '0').replace('0=0', '1')
    else:
        result = then_result
    return result

if __name__ == '__main__':
    main(equation)