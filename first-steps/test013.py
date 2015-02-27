for x, y in enumerate (['one', 'two','three']):
    print x, y

question = ['name', 'date','sex']
answer = ['yury','01.12.1082', 'male']
jester = ['fuck', 'kiss', 'slap']
for q, a, j in zip(question, answer, jester):
    print 'What is your {0}? Is it {1}? {2} you then!'.format (q, a, j)


for a in reversed(range (1, 10, 2)):
    print a

kings = {'peter':'the great', 'nicky': 'the last'}
for a, b in kings.iteritems():
    print a, b