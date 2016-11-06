'''
digit_sum | Practice Makes Perfect.4

'''


# def digit_sum(n):
#     total = 0
#     numbers = str(n)

#     for item in numbers:
#         total += int(item)

#     return total


def digit_sum(n):
    return sum([int(x) for x in str(n)])


def digit_sum_expanded(n):
    # Define empty list, to store each item of string `n` as number.
    # - our list comprehension does the same, without extra variable
    numbers_list = []
    for x in str(n):
        numbers_list.append(int(x))
    # Now define total, adding each int from numbers_list:
    # - `sum(numbers_list)` does exactly the same!
    total = 0
    for number in numbers_list:
        total += number
    return total


def digit_sum_modulo(n):
    s = 0
    while n > 0:
        s += (n % 10)
        n //= 10
    return s


print(digit_sum(1234))
print(digit_sum_expanded(1234))
print(digit_sum_modulo(1234))
