'''
Generating Multiplication tables | pg. 82

'''


def multi_table(a):
    for i in range(1, 11):
        print(
            '{} x {} = {}'.format(a, i, a * i)
        )

#
# Changing format of number
#


def multi_table_format(a):
    for i in range(1, 11):
        print(
            '{0:.2f} x {1:.2f} = {2:.2f}'.format(a, i, a * i)
        )


if __name__ == '__main__':
    a = input('Enter a number: ')
    multi_table(float(a))
    multi_table_format(float(a))
