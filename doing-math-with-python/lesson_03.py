from fractions import Fraction

f = Fraction(3, 4)
i = 1
fi = f + i

print(f)
print(fi)

# Using Fraction for negative exponent
smallDeal = 1 / 10 ** 3
print(smallDeal)

# You need to use a float to return properly
fractionDeal = Fraction(1, 10) ** 3.0
print(fractionDeal)

#
# Complex numbers
#

a = 2 + 3j
type(a)

# Real, Imaginary, Conjugate

z = 2 + 3j
print(z.real)
print(z.imag)

print(z.conjugate())

# Calculate the magnitude of a complex number:
# Using exponents like this

(z.real ** 2 + z.imag ** 2) ** 0.5
