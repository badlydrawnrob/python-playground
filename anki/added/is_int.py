'''
Checking if the number is an integer | Practice Makes Perfect.3

'''


def is_int(x):
    if x % 1 == 0:
        return True
    else:
        return False


# def is_int(x):
#     if (x - int(x)) > 0 or (x - int(x)) < 0:
#         return False
#     else:
#         return True


# def is_int(x):
#     if abs(x) - abs(int(x)) > 0:
#         return False
#     else:
#         return True


# def is_int(x):
#     x = float(abs(x))

#     if x.is_integer():
#         return True
#     else:
#         return False


print(is_int(7.5))   # False
print(is_int(-1))    # True
print(is_int(-1.5))  # False
print(is_int(7.0))   # True
