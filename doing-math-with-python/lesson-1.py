# Floor #
#########

# Everything is a float in Python 3
# - To return an integer, use floor()
# - A simple way to do this is '//'
positive = 4 // 4

# Be aware of negative numbers
# - They use floor, so a lower number than you'd expect
negative = -3 // 2

print(str(positive))  # 1
print(str(negative))  # -2

# Modulo #
##########

# 2 goes into 9 four times (2*4=8) leaving 1 remainder

modulo = 9 % 2
print(modulo)

# Exponent #
###############

# To the power of (2)
# Or 2^2 written.

bigDeal = 2 ** 10
print(bigDeal)

# Negative exponent #
#####################
# See here: http://bit.ly/1QUNBqn

# An easier way to think about this is:
# 1. Separate out into an exponent,
# 2. Then take the reciprical (divide exponent by 1)
#    - So, 10 ÷ 10 ÷ 10 becomes 1 / 10 ** 3

smallDeal = 1 / 10 ** 3
print(smallDeal)
