#!/usr/bin/python -e

NOT = [('!0', '1'), ('!1', '0')]
AND = [('0&0', '0'), ('0&1', '0'), ('1&0', '0'), ('1&1', '1')]
OR = [('0|0', '0'), ('0|1', '1'), ('1|0', '1'), ('1|1', '1')]
THEN = [('0:0', '1'), ('0:1', '1'), ('1:0', '0'), ('1:1', '1')]
EQUIV = [('0=0', '1'), ('0=1', '0'), ('1=0', '0'), ('1=1', '1')]


def simplify_operators(exp):
    return exp.replace(' and ', '&').replace(' or ', '|').replace('not ', '!') \
        .replace(' then ', ':').replace(' equiv ', '=').replace(' ', '')


def find_variables(exp):
    return sorted(set(filter(lambda c: 'a' <= c <= 'z', exp)))


def do_replace(exp, replaces):
    need_replace = True
    while need_replace:
        replaced = False
        for replace in replaces:
            new_exp = exp.replace(replace[0], replace[1])
            if len(new_exp) < len(exp):
                replaced = True
                exp = new_exp
        if not replaced:
            need_replace = False
    return exp


def find_closing_bracket(exp, begin):
    c = 0
    for i in range(begin + 1, len(exp)):
        if exp[i] == '(':
            c += 1
        if exp[i] == ')':
            if c == 0:
                return i
            else:
                c -= 1
    raise Exception('Unmatched bracket')


def calc(exp, vars_):
    orig = exp
    for name in vars_:
        exp = exp.replace(name, vars_[name])

    while True:
        begin = exp.find('(')
        if begin == -1:
            break
        end = find_closing_bracket(exp, begin)
        exp = exp[:begin] + calc(exp[begin + 1:end], vars_) + exp[end + 1:]

    while True:
        l = len(exp)
        for replaces in [NOT, AND, OR, THEN, EQUIV]:
            exp = do_replace(exp, replaces)
        if len(exp) == l:
            break

    if len(exp) > 1:
        raise Exception('Not an expression: %s' % orig)
    return exp


def get_all_values(i):
    if i <= 1:
        return [['0'], ['1']]
    small = get_all_values(i - 1)
    return [['0'] + e for e in small] + [['1'] + e for e in small]


def main():
    e = 'not ((b or not b) then (d and not d))'
    simple = simplify_operators(e)
    names = find_variables(simple)
    print ' '.join(names + [' ', e])
    for values in get_all_values(len(names)):
        vars_ = dict(zip(names, values))
        print ' '.join(values + [' ', calc(simple, vars_).center(len(e))])


main()