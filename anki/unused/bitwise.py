'''
Bitwise | Introduction to bitwise operators

'''

print(5 >> 4)  # Right Shift
print(5 << 1)  # Left Shift
print(8 & 5)   # Bitwise AND
print(9 | 4)   # Bitwise OR
print(12 ^ 42) # Bitwise XOR
print(~88)     # Bitwise NOT


# Numbers
# =======

# 8's bit  4's bit  2's bit  1's bit
#    1        0        1       0
#    8    +   0    +   2   +   0  = 10

print(0b1),    # 1
print(0b10),   # 2
print(0b11),   # 3
print(0b100),  # 4
print(0b101),  # 5
print(0b110),  # 6
print(0b111)   # 7
print("******")
print(0b1 + 0b11)
print(0b11 * 0b11)


# The bits go up like so
# ======================
# | 2**0  | = 1    |
# | 2**1  | = 2    |
# | 2**2  | = 4    |
# | 2**3  | = 8    |
# | 2**4  | = 16   |
# | 2**5  | = 32   |
# | 2**6  | = 64   |
# | 2**7  | = 128  |
# | 2**8  | = 256  |
# | 2**9  | = 512  |
# | 2**10 | = 1024 |

a = 0b11101110
mask = 0b00010001
desired = a ^ mask
print(bin(desired))

#                     < 1
#
#               0 b 1 0 1
# 0 b 1 0 0 0 0 0 0 1 0
# - - - - - - - - - - - -
#    10 9 8 7 6 5 4 3 2 1
