'''
Create your own loop | Codecademy loops.19

'''

items = ['eggs', 'bread', 'ham']
cost = [3, 2, 4]

for index, item in enumerate(zip(items, cost)):
    if type(item[0]) == str:
        print('{}: {}'.format(index, item[0]))
    else:
        print('{} is not a string'.format(item))
else:
    print('End of the list!')
