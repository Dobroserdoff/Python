
def print_number(a, base):
    number = []
    summary = 0
    for i in range(len(a)):
        number.append(a[i:i+1])
    for j in range(len(number)):
        if ord(number[j]) >= 48 and ord(number[j]) <=57:
            summary = summary + ((ord(number[j]) - 48) * (base ** (len(number) - j-1)))
        if ord(number[j]) >= 97 and ord(number[j]) <=122:
            summary = summary + ((ord(number[j]) - 87) * (base ** (len(number) - j-1)))
    print summary
    return summary


print_number('3b17', 16)