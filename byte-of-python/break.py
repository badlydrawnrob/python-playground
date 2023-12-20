# Breaking out of a while loop

while True:
    s = input('Enter something: ')
    if s == 'quit' or s == 'q':
        break
    print('Length of string is', len(s))