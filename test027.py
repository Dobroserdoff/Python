

def number_to_string(number, base, length=1):
    mirror = []
    final = ''
    while number > 0:
        b = number % base
        c = number / base
        number = c
        mirror.append(b)
    for i in range(len(mirror)):
        if mirror[-i - 1] < 10:
            final = final + (chr(mirror[-i - 1] + 48))
        else:
            final = final + (chr(mirror[-i - 1] + 87))
    while length > len(final):
        final = '0' + final
    return final


print number_to_string(10, 16, 2)