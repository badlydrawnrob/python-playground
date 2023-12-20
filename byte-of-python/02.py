i = 5
print(i)
i = i + i
print(i)

s = '''This is a multi-line string.
This is the second line.'''

print(s)

# You can use ; to separate commands
# but it's best avoided
i = 2; print(i)
# better ...
i = 2
print(i)

# Some quick reminders
3 ** 4 # exponent
13 % 3 # modulo

if not True:
    print('this')
else:
    print('that')


if 20 > 10 and 10 < 20:
    print('of course it is')
else:
    print("of course it isn't")


if 10 == 10 or 10 < 8:
    print('one of them is')
    

# Shortcut for assigning variables
a = 2
print(a)
a *= 2
print(a)
a += 1
print(a)