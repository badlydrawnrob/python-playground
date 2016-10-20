'''
Converting units of measurement | pg. 88

'''


def inches(a):
    print(
        '{0} inches equals roughly {1:.2f} cm'.format(a, (a * 2.54) / 100)
    )


def km(a):
    print(
        '{} miles is exactly {} kilometers'.format(a, (a * 1.609))
    )

inches(25.5)
km(650)


def celsius(a):
    print(
        'The temparature is {}ºf and {}ºC'.format(a, (a - 32) * (5 / 9))
    )


def fahrenheit(a):
    print(
        'The temperature is {0}ºC and {1:.1f}ºf'.format(a, a * (9 / 5) + 32)
    )

f = 98.6
c = 37
celsius(f)
fahrenheit(c)
