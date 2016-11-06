'''
Factorial | Practice makes perfect.5

'''


# def factorial(x):
#     n = x
#     total = 0
#     while n > 0:
#         total += n * (n - 1)
#         x -= 1
#     return total


# print(factorial(4))

# def factorial(x):
#     if x < 1:
#         return 1  # 0 is equal to 1
#     else:
#         total = x

#         while x > 1:
#             total *= (x - 1)
#             x -= 1
#         return total

# print(factorial(0))


# def factorial(x):
#     product = 1
#     for i in range(x):
#         product = product * (i + 1)
#     return product

# print(factorial(4))


# Recursive function

def factorial(x):
    if x == 1:
        return x
    else:
        return x * factorial(x - 1)

print(factorial(1))
print(factorial(4))
