a = 3
b = 3.5
c = '3'

print(type(a))
print(type(b))
print(type(c))

# Changing numbers
numberOne = int(2.8)
numberTwo = float(10)


def is_float(x):
    if isinstance(x, float):
        return x
    else:
        return 'Definitely not a float'

print('----')
print(is_float(numberOne))
print(is_float(numberTwo))
