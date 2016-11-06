'''
Sequence (count) | Practice makes perfect.11

'''

# Version 1
###########


def count(sequence, item):
    found = 0
    # Returns True or False:
    item_is_list = isinstance(item, (tuple, list))

    for i in sequence:
        if i == item:
            found += 1
        # use in operator instead of ==
        elif item_is_list and i in item:
            found += 1

    return found


print(count([1, 3, 'one', 4, 5], 'one'))
print(count([1, 2, 3, 1, 4, 1], [1, 2]))



# Version 2
############
# 1. Item must be an int from 1-5
# 2. Sequence items could be:
#   - list (one level deep only)
#   - number
#   - or word
############

# numbers = {
#     'one': 1, '1': 1, '1.0': 1,
#     'two': 2, '2': 2, '2.0': 2
# }


# def count(sequence, item):
#     item = item / 1  # Always use a float
#     found = 0
#     sequence_copy = []
#     is_list = []


#     for i in sequence:
#         elif type(i) == str:
#             if i in numbers:
#                 sequence_copy.append(numbers[i])
#             else:
#                 continue
#         elif type(i) == float:
#             if i.is_integer() == True:
#                 if i == item:
#                     sequence_copy.append(i)
#         elif type(i) == int:
#             if i == item:
#                 sequence_copy.append(i)

#     for n in sequence_copy:
#         found += 1

#     return sequence_copy, found


# print(count([1, 'one', 2, 5, '1.0'], 1))
# print(count([1, 2, 5, 1, 4], 1))
# print(count(['string', 2, 'hello', 1, 'what'], 'hello'))
# print(count(['sup', 'one', 5, '1', 1], 1))
# print(count([[1, 1], 2, 3, [4, 1], 1], 1))
