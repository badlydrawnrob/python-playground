from fractions import Fraction

try:
    a = float(input('Enter a number: '))
except ValueError:
    print(a, 'You entered an invalid number!')

# Using only integers
# - This includes 1.0, 2.0 which Python sees as ints

1.0.is_integer()  # returns true
1.1.is_integer()  # returns false

a = Fraction(input('Enter a fraction: '))

# Seems the variable needs to be setup
# first to allow str(test) to print

test = 0

try:
    test = Fraction(input('Enter a fraction: '))
except ZeroDivisionError:
    print('Sorry,', str(test), 'isn\'t not a function!')

# The same can be done with a complex number,
# but you have to enter it correctly ...

try:
    z = complex(input('Enter a complex number: '))
except ValueError:
    print('Please enter the correct syntax (a+bj)')
