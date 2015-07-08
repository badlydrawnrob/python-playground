#
# Indexes: Sort
# - List Capabilities and Functions (9)

## sort() method
################

animals = ["cat", "ant", "bat"]
animals.sort()

for animal in animals:
    print animal

#### Q: What is `sort()` doing here?
####	- Explain what it defaults to (alphabetical)
####	- Note that .sort() modifies the list rather than returning a new list.
#### Q: Explain what we're doing in the `for` loop


## sort() v2
#############

# This is a little more complex, and includes a list and an empty list:

start_list = [5, 3, 1, 2, 4]
square_list = []

# Your code here!
for list in start_list:
    list = list**2
    square_list.append(list)

square_list.sort()
print square_list

#### Q: Explain how we create an empty list
#### Q: Explain what we're doing in the `for` loop
# 		- run through each item in `start_list`
# 		- create a new variable and calculate each `start_list` item
#		  by multiplying it: list*list (list to the power 2)
#		- Append each newly created calculation to the empty `square_list`
#### Q: Explain again what `.sort()` does
#### Q: What will `print square_list` return?
