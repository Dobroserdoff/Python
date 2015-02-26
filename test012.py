fruits = {'apple' : 321, 'pear' : 456, 'orange' : 789}
fruits ['peach'] = 432
print fruits
print fruits ['apple']
del fruits['pear']
fruits ['banana'] = 123
print fruits.keys ()
a = 'orange' in fruits
print a
print dict ([('kiwi', 436), ('mango', 942)])

print {x: x**2 for x in (2, 4, 6)}
print locals ()