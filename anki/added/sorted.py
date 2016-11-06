'''
Median sorted() | Practice makes perfect.15

'''


def median(args):
    new_list = sorted(args)
    print('{} converted to {}'.format(args, new_list))
    length_of_list = len(new_list)
    # Using floor gives a whole number,
    # as well as rounding down, so 7 / 2 = 3.5 becomes '3'
    # - This gives us the middle index for new_list when odd.
    half = (length_of_list - 1) // 2

    if length_of_list == 0:
        return 0
    elif length_of_list % 2 == 0:
        print('{} and {}'.format(new_list[half], new_list[half + 1]))
        return (new_list[half] + new_list[half + 1]) / 2
    else:
        return new_list[half]


print(median([1, 5, 3, 4, 2]))
print(median([1, 5, 4, 2]))
print(median([1, 5, 4, 2, 1, 5, 4, 2]))
print(median([4, 5, 5, 4]))
print(median([1]))
print(median([]))
