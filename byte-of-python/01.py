# Our dumb first program
print("hello world")

# A helper function
help('len')

print('''A multiline string
that goes "on" and 'on'
to a different line
    with a tab''')

age = 20
name = 'Rob'
string = '{0} was {1} years old when he wrote this book'.format(name,age)
string2 = name + ' is ' + str(age) + ' years old'

print(string)
print(string2)
print("he wishes")

# Escaping a character with backslash
print('What\'s your name?')
# Explicit newline character
print("\nFirst line\nSecond line")
# No newline but nice to look at
print("This is the first line \
and the second line")



string1 = 'What\'s your name?'
string2 = "{} is my name \
thanks for asking.".format(name)
string3 = "May as well throw in a \n newline"

print(string1, string2, string3)