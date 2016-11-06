#
# When a nonzero integer, `a`
# divides another integer, `b`,
# leaving a remainder 0, a is said to be a factor of b
#


def is_factor(a, b):
    if b % a == 0:
        return True
    else:
        return False

# Is `4` a factor of `1024`?
print(is_factor(4, 1024))
