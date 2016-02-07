#
# Dictionary lists 02
# - Python lists and dictionaries 11/14


menu = {} # Empty dictionary

#### Q: How to create an empty dictionary?

# The length len() of a dictionary is the number of key-value pairs it has.
# Each pair counts only once, even if the value is a list.
# (That's right: you can put lists inside dictionaries!)

#### Q: What is the length of a dictionary? (I think I've added this already)



menu = {} # 1
menu['Chicken Alfredo'] = 14.50 # 2
print menu['Chicken Alfredo'] # 3

menu['Lasagne'] = 10
menu['Pizza pepperoni'] = 8.45
menu['Risotto funghi'] = 7.50

print "There are " + str(len(menu)) + " items on the menu." # 4, 5
print menu # 6


#### Q1: What is this?
#### Q2: What is this doing? (Adding a new key-value pair)
#### Q3: What will this print out?
#### Q4: How do you combine a string with a variable (or whatever)
#### Q5: What is `str()` doing to `len()` and what is `len()` doing to `menu`?
#### Q6: What will `menu` print out?