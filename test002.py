x = int(raw_input('Please input an integer '))
if x < 0:
    x = 0
    print 'Negative changed to zero'
elif x == 0:
    print 'Zero'
elif x == 1:
    print 'One'
elif x == 2:
    print 'Two'
else:
    print 'Too Much'