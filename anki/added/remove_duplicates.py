'''
Remove duplicates | Practice makes perfect.14

'''


def remove_duplicates(args):
    new_list = []

    for i in args:
        if i not in new_list:
            print(i, 'is a duplicate')
            new_list.append(i)

    return new_list


print(remove_duplicates([1, 3, 4, 1, 1, 6, 7, 8, 1]))
