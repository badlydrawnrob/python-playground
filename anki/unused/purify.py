'''
Purify | Practice makes perfect.12

'''


# def purify(args):
#     args = list(args)

#     for i, n in enumerate(args):
#         if n % 2 == 0:
#             remove = args.pop(i)
#             print('{} removed'.format(remove))

#     return args

# print(purify([1, 2, 3, 4, 6, 7]))


def purify(args):
    new_list = []

    for i, n in enumerate(args):
        if n % 2 == 0:
            new_list.append(n)
            print('{} added'.format(n))

    return new_list


print(purify([1, 2, 3, 4, 6, 7]))
