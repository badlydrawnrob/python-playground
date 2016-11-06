'''
Is prime number | Practice makes perfect.6

'''


# def is_prime(x):
#     if x < 2:
#         print('{} is not a prime number'.format(x))
#         return False
#     elif x == 2 or x == 3:
#         print('{} is a prime number'.format(x))
#         return True
#     else:
#         print('Is {} a prime number?'.format(x))

#         for n in range(2, x):
#             print('{} % {} = {}'.format(x, n, x % n))

#             if x % n == 0:
#                 print('{} is not a prime number'.format(x))
#                 return False
#                 # break required?
#         else:
#             return True


def is_prime(x):

    result = []  # Stores the result
    count = x    # To divide x by

    while count - 1 > 1:
        test = x % (count - 1)  # Calc if x is prime
        count -= 1
        result.append(test)  # Stores the result

        for i in result:  # Check if num is composite
            if i == 0:
                return False
                break  # Break out of the loop if True
    else:
        if x < 2:
            return False
        else:  # if the num is prime
            return True


print(is_prime(2))
print(is_prime(3))
print(is_prime(5))
print(is_prime(7))
print(is_prime(11))
print(is_prime(13))
print(is_prime(17))
print(is_prime(0))
print(is_prime(1))
print(is_prime(4))
print(is_prime(6))
print(is_prime(9))
