'''
Product | Practice makes perfect.13

For example: product([4, 5, 5])
should return 100 (because 4 * 5 * 5 is 100).
'''


def product(products):
    total = products[0]

    for p in products[1:]:
        total *= p

    return total


print(product([1, 4, 229]))
